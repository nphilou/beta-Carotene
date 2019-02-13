import math

import numpy as np
import random

Dx = 5
Dy = 5
Empty = 0
White = 1
Black = 2
Left = 0
Front = 1
Right = 2


class Board(object):
    def __init__(self):
        self.turn = White
        self.h = 0
        self.board = np.zeros((Dx, Dy))
        for i in range(0, 2):
            for j in range(0, Dy):
                self.board[i, j] = White
        for i in range(Dx - 2, Dx):
            for j in range(0, Dy):
                self.board[i, j] = Black

        self.hashtable = init_zobrist()
        self.ash()

    def legalMoves(self, color):
        moves = []
        for i in range(0, Dx):
            for j in range(0, Dy):
                if self.board[i][j] == color:
                    for k in [-1, 0, 1]:
                        for l in [-1, 0, 1]:
                            m = Move(color, i, j, i + k, j + l)
                            if m.valid(self):
                                moves.append(m)

        return moves

    @staticmethod
    def adversary(color):
        if color == White:
            return Black
        else:
            return White

    def won(self, color):
        if self.legalMoves(self.adversary(color)).__len__() == 0:
            return True

    def execute(self, move):
        # if move.valid(self):
        self.board[move.x1][move.y1] = Empty
        self.board[move.x2][move.y2] = move.color

    # else:
    #    print("Unvalid move")

    def __str__(self):
        return self.board

    def ash(self):
        for i in range(5):  # loop over the board positions
            for j in range(5):
                if self.board[i, j] != Empty:
                    # index 0 for White, 1 for Black
                    k = int(self.board[i, j] - 1)
                    # print(self.hashtable[i, j, k])
                    self.h = self.h ^ self.hashtable[i, j, k]
                # else:
                #    print("empty")

    def play(self, move):
        col = int(self.board[move.x2, move.y2])
        if col != Empty:
            # not empty destination -> remove hash from board
            self.h = self.h ^ self.hashtable[move.x2, move.y2, col - 1]

        # print(self.board)
        # print(move)

        # print(self.h)
        # print(self.hashtable)
        # print(self.hashtable[move.x2, move.y2, move.color - 1])

        # move with eating
        self.h = self.h ^ self.hashtable[move.x2, move.y2, move.color - 1]
        self.h = self.h ^ self.hashtable[move.x1, move.y1, move.color - 1]

        self.execute(move)

        if move.color == White:
            self.turn = Black
        else:
            self.turn = White

    def descent(self, tt):
        # Board with hash h isn't in tt
        if self.h not in tt:
            print(str(self.h) + " is not in TT")
            # v, prior = self.getOutputNetwork(self.turn) -> evaluate(board, player)
            value, prior = 0, 75 * [0.0]
            v = [75 * [0], 75 * [0.0], value, prior]
            # [nb_playouts, mean, value, prior]
            tt[self.h] = v
            return value
        elif self.won(White):
            print("White won")
            exit(0)
            return 1.0
        elif self.won(Black):
            print("Black won")
            return 0.0
        else:
            print(self.h)
            s = tt[self.h]
            # print(s)
            l = self.listeCoupsPossibles()  # Legal moves of current player
            if len(l) == 0:
                if self.turn == White:
                    return 0.0
                return 1.0

            best_move = l[0]
            best_score = -1000000.0
            sum_playouts = 0

            for m in l:
                move_index = m.code()
                sum_playouts += s[0][move_index]

            print("sum_playouts = " + str(sum_playouts))

            for m in l:
                move_index = m.code()
                # print(move_index)
                # print(s[1][move_index])  # mean
                # print(s[0][move_index])  # nb_playouts
                # print(s[3][move_index])  # prior

                if s[0][move_index] != 0:
                    puct = (s[1][move_index] / s[0][move_index]) + 0.3 * s[3][move_index] * math.sqrt(sum_playouts) / \
                           s[0][move_index]
                else:
                    puct = 0

                # print("puct = " + str(puct))
                if puct > best_score:
                    best_score = puct
                    best_move = m

            print(best_move)
            self.play(best_move)
            print(self.board)
            value = self.descent(tt)

            move_index = best_move.code()
            s[0][move_index] = s[0][move_index] + 1
            s[1][move_index] = s[1][move_index] + value
            return value

    def PUCT(self, tt, nb_playouts=800):
        print(self.h)
        b = Board()
        for i in range(nb_playouts):
            b.copy(self)
            print("Playout number : " + str(i))
            print("Copy hash = " + str(b.h))
            b.descent(tt)

        print(tt)
        s = tt[self.h]
        coups = self.listeCoupsPossibles()
        best = coups[0]
        best_score = -10000000.0
        for m in coups:
            code = m.code()
            if s[0][code] > best_score:
                best_score = s[0][code]
                best = m
        return best

    def listeCoupsPossibles(self):
        return self.legalMoves(self.turn)

    def copy(self, origin):
        self.turn = origin.turn
        self.h = 0
        self.board = np.zeros((Dx, Dy))
        for i in range(0, Dx):
            for j in range(0, Dy):
                self.board[i, j] = origin.board[i, j]

        self.hashtable = origin.hashtable
        self.ash()


class Move:
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
                # Diagonal
                if self.direction() in [Left, Right]:
                    return True
                return False
            elif board.board[self.x2][self.y2] == Empty:
                if self.direction() in [Left, Front, Right]:
                    return True
                return False
            else:
                return False

        elif self.color == Black:
            if self.x2 != self.x1 - 1:
                return False
            if board.board[self.x2][self.y2] == White:
                # Diagonal
                if self.direction() in [Left, Right]:
                    return True
                return False
            elif board.board[self.x2][self.y2] == Empty:
                if self.direction() in [Left, Front, Right]:
                    return True
                return False
            else:
                return False

    def __repr__(self):
        return "" + str(self.color) + " from " + "[" + str(self.x1) + ", " + str(self.y1) + "] to " + \
               "[" + str(self.x2) + ", " + str(self.y2) + "]\n"

    def direction(self):
        if self.y2 == self.y1 - 1:
            return Left
        if self.y2 == self.y1 + 1:
            return Right
        elif self.y2 == self.y1:
            return Front
        else:
            return -1

    def flat_index(self):
        return self.x1 * Dx + self.y1

    def code(self):
        return self.flat_index() * 3 + self.direction()


def random_play():
    board = Board()

    white_moves = board.legalMoves(White)
    black_moves = board.legalMoves(Black)

    stop = (white_moves.__len__() == 0 or black_moves.__len__() == 0)
    while not stop:
        print(board.board)
        white_move = np.random.choice(white_moves)
        print(white_move)
        board.execute(white_move)

        print(board.board)
        black_moves = board.legalMoves(Black)
        if black_moves.__len__() == 0:
            stop = True
            winner = White
            break

        black_move = np.random.choice(black_moves)
        print(black_move)
        board.execute(black_move)
        print(board.board)

        white_moves = board.legalMoves(White)
        if white_moves.__len__() == 0:
            stop = True
            winner = Black

    return winner


def random_bitstring():
    return random.randint(0, 2 ** 10 - 1)


def init_zobrist():
    # fill a table of random numbers/bitstrings
    table = np.zeros((5, 5, 2), dtype=int)

    for i in range(5):  # loop over the x
        for j in range(5):  # loop over the y
            for k in range(2):  # loop over the pieces
                table[i, j, k] = random_bitstring()

    return table


def evaluation(board):
    pass


def PUCT(board, player):
    moves = board.legalMoves(player)

    # TODO
    if board.is_terminal():
        return evaluation(board)


if __name__ == '__main__':
    board = Board()
    #
    # white_moves = board.legalMoves(White)
    # black_moves = board.legalMoves(Black)
    #
    # print(board.board)
    # print(board.h)
    # white_move = np.random.choice(white_moves)
    # print(white_move)
    # board.play(white_move)
    # print(board.h)
    # print(board.board)

    # tt1 = [[0] * 4] * (2 ** 10 - 1)
    tt1 = {}

    # print(tt1)

    board.PUCT(tt=tt1, nb_playouts=100)

    # m = Move(White, 1, 0, 2, 0)
    # print(m.code())

    # print("The winner is : " + str(random_play()))
