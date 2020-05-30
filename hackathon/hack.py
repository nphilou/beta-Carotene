import numpy as np
import matplotlib.pyplot as plt
from keras.layers import LSTM, Dense, GRU, Activation
from keras.models import Sequential
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd

N = 480
dt = 1 / (252 * 8 * 60)
S_0 = s_inf = 100
sigma = S_0 / 10


def datum():
    theta = np.random.uniform(0.01, 100)
    data = np.zeros(N)
    data[0] = S_0
    for j in range(1, N):
        data[j] = data[j - 1] + theta * (s_inf - data[j - 1]) * dt + sigma * np.sqrt(dt) * np.random.normal(0, 1)

    serie = pd.Series(data)
    delta = serie.diff(1)

    seriel = serie.iloc[0:479]
    etheta = np.mean(delta / seriel)
    data2 = []

    for i in range(0, 47):
        data2.append(data[(i + 1) * 10] - data[i * 10])

    rho = pd.Series(data2).autocorr(2)

    return np.array([rho, etheta]), theta


def generator(batch_size=32):
    while True:
        # Select files (paths/indices) for the batch
        batch_input = []
        batch_output = []

        # Read in each input, perform preprocessing and get labels
        for i in range(batch_size):
            x, y = datum()

            batch_input += [x]
            batch_output += [y]
        # Return a tuple of (input,output) to feed the network
        batch_x = np.array(batch_input)
        batch_y = np.array(batch_output)

        scaler = MinMaxScaler(feature_range=(0, 1))
        batch_x = scaler.fit_transform(batch_x)

        batch_x = np.expand_dims(batch_x, axis=0)

        yield batch_x, batch_y


if __name__ == '__main__':
    # Design model
    (data_0, theta) = datum()

    print(data_0.shape)

    # new_generator = generator()
    # print(next(new_generator))

    #model = Sequential()
    #model.add(LSTM(1, activation='relu', input_shape=(2, 1)))
    #model.add(Dense(1, activation='softmax'))

    model = Sequential([
        Dense(1, input_shape=(2, 1), activation='softmax'),
    ])

    model.compile(loss='mse', optimizer='adam')

    # Train model on dataset
    model.fit_generator(generator=generator(32), validation_data=generator(32), validation_steps=10,
                        samples_per_epoch=32, nb_epoch=10)
