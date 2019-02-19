import math

import numpy as np
import random
from sys import stdin, stdout, stderr

Dx = 5
Dy = 5
SizePolicy = 3 * Dx * Dy

Empty = 0
White = 1
Black = 2

stringColor = ["Empty", "White", "Black"]

hashTable = []

for k in range(3):
    l = []
    for i in range(Dx):
        l1 = []
        for j in range(Dy):
            l1.append(int(random.random() * (2 ** 64)))
        l.append(l1)
    hashTable.append(l)


class Board(object):
    def __init__(self):
        self.turn = White
        self.h = 0
        self.board = np.zeros((Dx, Dy), dtype=int)
        for i in range(0, 2):
            for j in range(0, Dy):
                self.board[i][j] = White
        for i in range(Dx - 2, Dx):
            for j in range(0, Dy):
                self.board[i][j] = Black

    def copy(self, b):
        self.turn = b.turn
        self.h = b.h
        for i in range(0, Dx):
            for j in range(0, Dy):
                self.board[i][j] = b.board[i][j]

    def legalMoves(self):
        moves = []
        for i in range(0, Dx):
            for j in range(0, Dy):
                if self.board[i][j] == self.turn:
                    for k in [-1, 0, 1]:
                        for l in [-1, 0, 1]:
                            m = Move(self.turn, i, j, i + k, j + l)
                            if m.valid(self):
                                moves.append(m)
        return moves

    def print(self):
        for i in range(Dx):
            stdout.write('|')
            for j in range(Dy):
                if self.board[i][j] == White:
                    stdout.write('w')
                if self.board[i][j] == Black:
                    stdout.write('b')
                if self.board[i][j] == Empty:
                    stdout.write(' ')
                stdout.write('|')
            stdout.write('\n')

    def printMoves(self, moves):
        for i in range(0, len(moves)):
            print(moves[i])

    def play(self, move):
        col = int(self.board[move.x2][move.y2])
        if col != Empty:
            self.h = self.h ^ hashTable[col][move.x2][move.y2]
        self.h = self.h ^ hashTable[move.color][move.x2][move.y2]
        self.h = self.h ^ hashTable[move.color][move.x1][move.y1]
        self.board[move.x2][move.y2] = move.color
        self.board[move.x1][move.y1] = Empty

        if (move.color == White):
            self.turn = Black
        else:
            self.turn = White

    def won(self, color):
        if (color == White):
            for i in range(0, Dy):
                if (self.board[Dx - 1][i] == White):
                    return True
        else:
            for i in range(0, Dy):
                if (self.board[0][i] == Black):
                    return True
        return False

    def playout(self):
        l = self.legalMoves()
        while len(l) > 0 and not self.won(White) and not self.won(Black):
            indice = int(random.random() * len(l))
            m = l[indice]
            self.play(m)
            l = self.legalMoves()
        if len(l) == 0:
            if self.turn == Black:
                return 1.0
            else:
                return 0.0
        if self.won(White):
            return 1.0
        else:
            return 0.0

    def flat(self, n):
        l = self.legalMoves()
        best = l[0]
        best_score = n + 1
        if self.turn == White:
            best_score = -1.0
        b = Board()
        for m in l:
            sum = 0
            for i in range(n):
                b.copy(self)
                b.play(m)
                r = b.playout()
                sum = sum + r
            if (self.turn == White and sum > best_score) or (self.turn == Black and sum < best_score):
                best_score = sum
                best = m
        return best

    def to_matrix(self):
        bitmap = np.zeros((3, Dx, Dy), dtype=int)

        for i in range(Dx):
            for j in range(Dy):
                bitmap[self.board[i][j]][i][j] = 1

        return bitmap

    def getOutputNetwork(self):
        if self.turn == White:
            return (SizePolicy + 1) * [1.0]
        else:
            return (SizePolicy + 1) * [1.0]

    def descent(self, TT):
        if self.h not in TT:
            output = self.getOutputNetwork()
            l = []
            l.append(SizePolicy * [0])
            l.append(SizePolicy * [0.0])
            l.append(output)
            TT[self.h] = l
            return output[Dx * Dy]
        elif self.won(White):
            return 1.0
        elif self.won(Black):
            return 0.0
        else:
            s = TT[self.h]
            turn = self.turn
            l = self.legalMoves()
            if len(l) == 0:
                if turn == White:
                    return 0.0
                return 1.0

            best = l[0]
            best_score = -1000000000.0
            sum_playouts = 0
            sum_scores = 0.0

            for m in l:
                i = m.code()
                sum_playouts = sum_playouts + s[0][i]
                sum_scores = sum_scores + s[1][i]

            mean = 0.0
            if sum_playouts > 0:
                mean = sum_scores / sum_playouts

            for m in l:
                i = m.code()
                mu = mean

                if s[0][i] > 0:
                    mu = s[1][i] / s[0][i]

                if turn == Black:
                    mu = 1.0 - mu

                puct = mu + 0.3 * s[2][i] * math.sqrt(sum_playouts) / (1.0 + s[0][i])

                if puct > best_score:
                    best_score = puct
                    best = m

            self.play(best)
            v = self.descent(TT)

            i = best.code()
            s[0][i] = s[0][i] + 1
            s[1][i] = s[1][i] + v
            return v

    def PUCT(self, TT, nb_playouts=800):
        b = Board()
        for i in range(nb_playouts):
            b.copy(self)
            b.descent(TT)
        s = TT[self.h]
        l = self.legalMoves()
        best = l[0]
        best_score = -1000000000.0
        for m in l:
            i = m.code()
            if s[0][i] > best_score:
                best_score = s[0][i]
                best = m
        return best


class Move(object):
    def __init__(self, color, x1, y1, x2, y2):
        self.color = color
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def valid(self, board):
        if self.x2 >= Dx or self.y2 >= Dy or self.x2 < 0 or self.y2 < 0:
            return False
        if self.color == White:
            if self.x2 != self.x1 + 1:
                return False
            if board.board[self.x2][self.y2] == Black:
                if self.y2 == self.y1 + 1 or self.y2 == self.y1 - 1:
                    return True
                return False
            elif board.board[self.x2][self.y2] == Empty:
                if self.y2 == self.y1 + 1 or self.y2 == self.y1 - 1 or self.y2 == self.y1:
                    return True
                return False
        elif self.color == Black:
            if self.x2 != self.x1 - 1:
                return False
            if board.board[self.x2][self.y2] == White:
                if self.y2 == self.y1 + 1 or self.y2 == self.y1 - 1:
                    return True
                return False
            elif board.board[self.x2][self.y2] == Empty:
                if self.y2 == self.y1 + 1 or self.y2 == self.y1 - 1 or self.y2 == self.y1:
                    return True
                return False
        return False

    def __str__(self):
        return stringColor[self.color] + '/' + str(self.x1) + '/' + str(self.y1) + '/' + str(self.x2) + '/' + str(
            self.y2)

    def code(self):
        direction = 1
        if self.y2 > self.y1:
            direction = 0
        if self.y2 < self.y1:
            direction = 2
        return 3 * (Dx * self.x1 + self.y1) + direction


if __name__ == '__main__':
    # m = b.flat(100)  # < MCTS
    # print(m)
    b = Board()
    print(b.to_matrix())

    # l = b.legalMoves()
    # b.printMoves(l)
    # r = b.playout()
    # print(r)
    # b = Board()
    # m = b.flat(100)
    # print(m)
    # m = b.PUCT({})
    # print(m)
