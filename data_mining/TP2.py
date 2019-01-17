import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np


def rui(r, u):
    return r.iloc[u,][r.iloc[u,] != 0].index


def yyt(y, resui, k=100):
    res = np.zeros((k, k))

    print(y.shape)
    print(y[0].shape)

    for u_p in resui:
        res += np.dot(y[:, u_p], y[:, u_p].T)

    return res


def alterning_least_square(X_train, k=100, max_iter=100):
    n = len(X_train)
    m = len(set(data['item_id']))

    X = np.random.randn(k, n)
    Y = np.random.randn(k, m)

    print("size")
    print(Y.shape)

    print(yyt(resui=rui(X_train, 1), y=Y))

    for step in range(max_iter):
        for u in range(n):
            X = 0


if __name__ == '__main__':
    data = pd.read_table('ml-100K/u.data', names=['user_id', 'item_id', 'rating', 'timestamp'])
    print(data.head())

    R = pd.pivot_table(data, values='rating', index=['user_id'], columns=['item_id'], fill_value=0)
    # print(R.head())

    X_train, X_test = train_test_split(R, test_size=0.2, random_state=42)

    print(X_train.head())

    # print(rui(X_train, 1))

    alterning_least_square(X_train, k=100, max_iter=100)
