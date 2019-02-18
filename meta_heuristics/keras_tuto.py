from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.losses import categorical_crossentropy, binary_crossentropy
import numpy as np
from keras.optimizers import SGD

if __name__ == '__main__':
    model = Sequential()
    model.add(Dense(units=64, input_shape=(2,), activation='tanh'))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.summary()

    sgd = SGD(lr=0.1)
    model.compile(loss=binary_crossentropy,
                  optimizer=sgd)

    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    Y = np.array([0, 1, 1, 0])

    s = 1000

    a = np.random.randint(2, size=s)
    b = np.random.randint(2, size=s)
    c = a ^ b

    print(X)
    print(Y)
    print(X.shape)

    #for i in range(s):
    #    X = np.append(X, [[a[i], b[i]]], axis=0)
    #    Y = np.append(Y, c[i])

    print(X)
    print(Y)

    print(X.shape)

    model.fit(X, Y, epochs=1000, batch_size=1)


