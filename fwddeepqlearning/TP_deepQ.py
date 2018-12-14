#!/usr/bin/env python
# coding: utf-8

# # TP apprentissage par renforcement
# 
# Yann Chevaleyre

# ## Test de l'installation
# 
# Exécutez (et comprenez) le code ci-dessous

import matplotlib.pyplot as plt
import math
import numpy as np
import gym

env = gym.make('CartPole-v0')


def simulation():
    for i_episode in range(3):
        observation = env.reset()
        reward = 0
        for t in range(20):
            # affichage graphique de l'environnement
            env.render()

            if math.degrees(observation[2]) < 2:
                action = 1
            else:
                action = 0

            # tirage d'une action au hasard entre {0,1}
            # action = np.random.randint(2)
            # cet action est faite, et on recupere
            # le prochain etat et la recompense
            observation, reward, done, info = env.step(action)

            if done:
                print("Episode finished after {} timesteps".format(t + 1))
                break


# Cet environnement `Cart-Pole` consiste à déplacer un chariot pour faire tenir en équilibre une poutre.
# Plus précisément:
# * Il y a deux actions : gauche et droite (représentées par 0 et 1)
# * L'observation reçue (c'est à dire l'état) est un tableau numpy comprenant 4 variables: la position du chariot,
# la velocite, l'angle a la verticale et la position du haut de la poutre
# * L'épisode se termine lorsque l'angle de la poutre à la verticale dépasse 12 degré
# * Les récompenses recues sont égales à 1 sauf si l'angle dépasse 12 degrés.
# 
# Pour afficher plus d'informations sur cet environnement, tapez `env.env?`

# ** Exercice** : dans le code précédent, l'action est choisie au hasard. Modifiez ce code pour que l'action choisie
# soit "va a droite" si l'angle de la poutre est inferieur a 2 degres, et "va a gauche" sinon.

# ## Première partie: Implémentation du Q-Learning Tabulaire
# 
# dans cette partie, vous devrez discrétiser l'espace d'état, et implémenter l'algorithme du Q-learning sur le
# tableau Q(s,a)
# 
# Pour commencer, voici un rappel de l'algorithme du Q-Learning:

# ![qlearning_image.png](attachment:qlearning_image.png)

# On va donc devoir discrétiser l'espace d'états.
# Pour cela, on cree une fonction `discretise(x)`, puis une fonction `observation_vers_etat` qui renvoie un état
# (nombre entre 0 et N-1) en fonction de l'observation. Lisez le code ci-dessous.

# nval est le pas de discretisation par variable


nval = 5  # nombre de valeur discretes qu'une variable peut prendre
N = nval ** 4  # taille de l'espace d'etat


def discretise(x, mini, maxi):
    # discretise x
    # renvoie un entier entre 0 et nval-1
    if x < mini:  x = mini
    if x > maxi:  x = maxi
    return int(np.floor((x - mini) * nval / (maxi - mini + 0.0001)))


def observation_vers_etat(observation):
    pos = discretise(observation[0], mini=-1, maxi=1)
    vel = discretise(observation[1], mini=-1, maxi=1)
    angle = discretise(observation[2], mini=-1, maxi=1)
    pos2 = discretise(observation[3], mini=-1, maxi=1)
    return pos + vel * nval + angle * nval * nval + pos2 * nval * nval * nval


# Maintenant, on peut donc récupérer à partir d'une observation le numéro de l'état associé:


observation = env.reset()
s = observation_vers_etat(observation)
print("le numero de l'etat de depart est le :", s)

env.close()


# ** Exercice **:
# * Creez un tableau numpy `Q` de dimension `N,2` initialisé aléatoirement. Ce tableau sera utilise dans
# l'algorithme du q-learning
# * Implémentez l'algorithme du Q-Learning. Ensuite, ajustez les paramètres de l'algorithme pour qu'il
# converge correctement


def q_array(Q, N):
    for i_episode in range(50):
        observation = env.reset()
        reward = 0
        for t in range(N):
            # affichage graphique de l'environnement
            # env.render()

            if (math.degrees(observation[2]) < 2):
                action = 1
            else:
                action = 0

            # tirage d'une action au hasard entre {0,1}
            # action = np.random.randint(2)
            # cet action est faite, et on recupere
            # le prochain etat et la recompense
            observation, reward, done, info = env.step(action)

            if done:
                print("Episode finished after {} timesteps".format(t + 1))
                break

            print(observation_vers_etat(observation))

            Q[observation_vers_etat(observation)][action] += reward


def ql_tabulaire(M, e, a=0.001, y=1, T=100):
    q = np.random.rand(N, 2)

    print(q.shape)

    nb_timesteps_episode = []

    nb_timesteps = 0
    for i_episode in range(M):
        observation = env.reset()
        reward = 0
        for t in range(T):
            state = observation_vers_etat(observation)

            if np.random.random() > e:
                action = np.random.randint(2)
            else:
                action = np.argmax(q[state])

            # tirage d'une action au hasard entre {0,1}
            # action = np.random.randint(2)
            # cet action est faite, et on recupere
            # le prochain etat et la recompense
            observation, reward, done, info = env.step(action)

            next_state = observation_vers_etat(observation)

            if done:
                q[state][action] = q[state][action] + a * reward
            else:
                #print(q[next_state])
                #print(q[state][action])
                #print(q[next_state] - q[state][action])
                q[state][action] = q[state][action] + a * (reward + y * np.argmax(q[next_state] - q[state][action]))

            if done:
                # print("Episode finished after {} timesteps".format(t + 1))
                nb_timesteps += t + 1
                # print(nb_timesteps)
                break

        if i_episode % 100 == 0:
            nb_timesteps_episode.append(nb_timesteps/100)
            nb_timesteps = 0

    print(nb_timesteps_episode)
    plt.plot(nb_timesteps_episode)
    plt.show()


ql_tabulaire(10000, 0.1, a=0.001, y=1, T=100)

# ## Seconde partie: Implémentation du Q-Learning avec approximation de fonction
# 
# dans cette partie, vous devrez d'abord créer un représentation de chaque état, avant d'implémenter le deep-q-learning
# 
# **Exercice**: 
# * Creez une fonction `K(x)` qui renvoie `1/(1+x**2)`
# * Créez un fonction qui transforme l'observation o en une représentation $\psi(o)$, en utilisant la fonction `K`,
# comme vu en cours
# * Implémentez l'algorithme du Q-learning avec approximation de fonction (deep q-learning) 
# * **Bonus**: Implémentez l' *Experience-replay*, et comparez-le a l'algorithme de base (l'algorithme est donné
# ci-dessous)

# ![deepRL-experience-replay.png](attachment:deepRL-experience-replay.png)


def k(x):
    return 1 / (1 + x ** 2)

