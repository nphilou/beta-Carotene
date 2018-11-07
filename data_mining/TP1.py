import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer, fetch_mldata
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from keras.datasets import mnist


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

some_digit = X[36000]
some_digit_image = some_digit.reshape(28, 28)

plt.imshow(some_digit_image, cmap=matplotlib.cm.binary, interpolation="nearest")