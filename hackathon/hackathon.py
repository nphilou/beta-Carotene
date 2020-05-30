import math

import pandas as pd
from keras import Sequential
from keras.applications.resnet50 import ResNet50
from keras.layers import Dense, Input, Flatten, Dropout, MaxPooling2D, Conv2D, LSTM, GRU
from sklearn import svm
from sklearn.cluster import KMeans
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score, classification_report, homogeneity_score
import keras
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import matplotlib.pyplot as plt
from xgboost import XGBClassifier


def moyenne_mobile(X, interval=3):
    # interval=3
    # X=data_train

    X_time = X.iloc[:, 2:]
    X_res = np.zeros(X_time.shape)

    for i in range(interval - 1, 240):
        val = np.sum(X_time.iloc[:, i - interval:i], axis=1)

        X_res[:, i] = val / interval

    X_res = X_res[:, interval:]
    return X_res


def useless(data, pred):
    data = moyenne_mobile(data, 20)

    # data = data.iloc[:, :2]
    for i in range(200, 220):
        if pred.values[i] == 0:
            plt.plot(data[i, 2:], color='green', linewidth=0.2)
        else:
            plt.plot(data[i, 2:], color='red', linewidth=0.2)

    plt.show()

    # model = QuadraticDiscriminantAnalysis()
    # model = svm.SVC(C=100, gamma='scale', degree=5)

    # model = Sequential()
    # model.add(LSTM(10, input_shape=input_shape))
    # model.add(Dense(1, activation='sigmoid'))
    # model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


class Classifier_FCN:
    def __init__(self, output_directory, input_shape, nb_classes, verbose=False):
        self.output_directory = output_directory
        self.model = self.build_model(input_shape, nb_classes)
        if (verbose == True):
            self.model.summary()
        self.verbose = verbose

    def build_model(self, input_shape, nb_classes):
        input_layer = keras.layers.Input(input_shape)

        conv1 = keras.layers.Conv1D(filters=128, kernel_size=8, padding='same')(input_layer)
        conv1 = keras.layers.normalization.BatchNormalization()(conv1)
        conv1 = keras.layers.Activation(activation='relu')(conv1)

        conv2 = keras.layers.Conv1D(filters=256, kernel_size=5, padding='same')(conv1)
        conv2 = keras.layers.normalization.BatchNormalization()(conv2)
        conv2 = keras.layers.Activation('relu')(conv2)

        conv3 = keras.layers.Conv1D(128, kernel_size=3, padding='same')(conv2)
        conv3 = keras.layers.normalization.BatchNormalization()(conv3)
        conv3 = keras.layers.Activation('relu')(conv3)

        gap_layer = keras.layers.pooling.GlobalAveragePooling1D()(conv3)

        output_layer = keras.layers.Dense(nb_classes, activation='softmax')(gap_layer)

        model = keras.models.Model(inputs=input_layer, outputs=output_layer)

        model.compile(loss='binary_crossentropy', optimizer=keras.optimizers.Adam(),
                      metrics=['accuracy'])

        reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.5, patience=50,
                                                      min_lr=0.0001)



        return model

    def fit(self, x_train, y_train, x_val, y_val):
        # x_val and y_val are only used to monitor the test loss and NOT for training
        batch_size = 16
        nb_epochs = 2000

        mini_batch_size = int(min(x_train.shape[0] / 10, batch_size))


        hist = self.model.fit(x_train, y_train, batch_size=mini_batch_size, epochs=nb_epochs,
                              verbose=self.verbose, validation_data=(x_val, y_val), callbacks=self.callbacks)


        y_pred = model.predict(x_val)

        # convert the predicted from binary to integer
        y_pred = np.argmax(y_pred, axis=1)



if __name__ == '__main__':
    #base = "/home/philippe/code/beta-Carotene/"
    base = ""
    data = pd.read_csv(base + "hackathon/Hackathon_Sujet_1_data/sp-explanatory-train.csv")
    pred = pd.read_csv(base + "hackathon/Hackathon_Sujet_1_data/sp-response-train.csv")
    datatest = pd.read_csv(base + "hackathon/Hackathon_Sujet_1_data/sp-explanatory-test.csv", header=None)

    # print(data.head(2))

    # useless(data, pred)
    datamean = []

    # data = data.iloc[:, 2:].diff(6, axis=1)
    for i in range(data.shape[0]):
        rolling_mean = data.iloc[i, 2:].rolling(window=14).mean()
        datamean.append(rolling_mean)

    plt.plot(data.iloc[0, 2:], color='red', linewidth=0.2)
    plt.plot(datamean[0], "g", label="Rolling mean trend", linewidth=0.2)
    plt.show()

    datamean = np.asarray(data)

    # normalize the dataset
    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    datatest = scaler.fit_transform(datatest)

    print(data.shape)

    x_train, x_test, y_train, y_test = train_test_split(data, pred, test_size=0.1, random_state=42)

    # model = RandomForestClassifier(n_jobs=-1, random_state=42, max_depth=15)
    # model = MLPClassifier((30, 40, 30), max_iter=1000, random_state=51)

    model = Classifier_FCN("", (x_train.shape[0], 1), 2)
    model.fit(x_train, np.ravel(y_train), x_test, y_test)

    preds = model.predict(x_test)
    print(f1_score(y_test, preds))
    print(confusion_matrix(preds, y_test))

    test = model.predict(datatest)

    np.savetxt(r'submit_test.txt', test, fmt='%d')


    #print(classification_report(y_test, preds, digits=3))
