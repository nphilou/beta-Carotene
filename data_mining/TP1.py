import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.losses import categorical_crossentropy
from keras.utils import to_categorical

cancer = load_breast_cancer()
print(cancer['data'].shape)

X = cancer['data']
y = cancer['target']

X_train, X_test, y_train, y_test = train_test_split(X, y)
scaler = StandardScaler()

scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

mlp = MLPClassifier(hidden_layer_sizes=(50, 50, 50), max_iter=2000)

mlp.fit(X_train, y_train)

predictions = mlp.predict(X_test)

print(confusion_matrix(y_test, predictions))

print(classification_report(y_test, predictions))

# MNIST

(x_train, y_train), (x_test, y_test) = mnist.load_data()
print("MNIST Loading : OK")

x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

# some_digit = x_train[36000]
# some_digit_image = some_digit.reshape(28, 28)

# plt.imshow(some_digit_image, cmap=matplotlib.cm.binary, interpolation="nearest")
# plt.show()

y_train_5 = (y_train == 5)
y_test_5 = (y_test == 5)

y_train = to_categorical(y_train_5, 2)
y_test = to_categorical(y_test_5, 2)

model = Sequential()
model.add(Dense(20, input_shape=(784,), kernel_initializer='uniform', activation='relu'))
model.add(Dense(20, kernel_initializer='uniform', activation='relu'))
model.add(Dense(2, kernel_initializer='uniform', activation='softmax'))

model.summary()

model.compile(loss=categorical_crossentropy,
              optimizer='adam',
              metrics=['accuracy'])

hist = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=100, batch_size=256, shuffle=True,
                 verbose=2)

score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# Test loss: 0.06656138199758682
# Test accuracy: 0.9925