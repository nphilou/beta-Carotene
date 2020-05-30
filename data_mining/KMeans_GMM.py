import itertools
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pylab
from scipy import linalg
from sklearn.cluster import KMeans
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.cluster import homogeneity_score
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

NUM_COLORS = 4
cmap = 'cool'
colors = (pylab.get_cmap(cmap)(1. * i / NUM_COLORS) for i in range(NUM_COLORS))
color_iter = itertools.cycle(colors)

nrows = 3
ncols = 1
figsize = (8, 10)
n_components = 5  # for SVD

s = 5
s_centroid = 50


def plot_settings(title):
    plt.xticks(())
    plt.yticks(())
    plt.title(title)


def plot_kmeans(x, y, centers, index, title):
    plt.subplot(nrows, ncols, index)
    plt.scatter(x[:, 0], x[:, 1], c=y, s=s, cmap=cmap)

    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=s_centroid, alpha=0.5)
    plot_settings(title)


def plot_gmm(x, y, means, covariances, index, title):
    splot = plt.subplot(nrows, ncols, index)
    for i, (mean, covar, color) in enumerate(zip(
            means, covariances, color_iter)):

        v, w = linalg.eigh(covar)
        v = 2. * np.sqrt(2.) * np.sqrt(v)
        u = w[0] / linalg.norm(w[0])

        if not np.any(y == i):
            continue
        plt.scatter(x[y == i, 0], x[y == i, 1], s, color=color)

        angle = np.arctan(u[1] / u[0])
        angle = 180. * angle / np.pi
        ell = mpl.patches.Ellipse(mean, v[0], v[1], 180. + angle, color=color)
        ell.set_clip_box(splot.bbox)
        ell.set_alpha(0.5)
        splot.add_artist(ell)

    plot_settings(title)


if __name__ == '__main__':
    categories = ['sci.electronics', 'rec.sport.baseball']
    n = categories.__len__()

    dataset = fetch_20newsgroups(subset='all', categories=categories, shuffle=True)

    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(dataset.data)

    svd = TruncatedSVD(n_components=n_components, n_iter=100, random_state=42)
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)

    svdftn = lsa.fit_transform(vectors)

    X_train, X_test, y_train, y_test = train_test_split(svdftn, dataset.target, test_size=0.2, random_state=42)

    plt.figure(figsize=figsize)

    # K means
    kmeans = KMeans(n_clusters=n).fit(X_train)
    y_kmeans = kmeans.predict(X_train)
    plot_kmeans(X_train, y_kmeans, kmeans.cluster_centers_, 1, "K means")

    # GMM
    gmm = GaussianMixture(n_components=n, verbose=2).fit(X_train)
    y_gmm = gmm.predict(X_train)
    plot_gmm(X_train, y_gmm, gmm.means_, gmm.covariances_, 2, 'Gaussian Mixture')

    # y_train
    plt.subplot(nrows, ncols, 3)
    plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=s, cmap=cmap)
    plot_settings("Y train")

    plt.show()

    print("Train homogeneity score")
    print("KMeans: %.3f" % homogeneity_score(y_kmeans, y_train))
    print("GMM: %.3f" % homogeneity_score(y_gmm, y_train))
    print("")

    print("Test homogeneity score")
    print("KMeans: %.3f" % homogeneity_score(kmeans.predict(X_test), y_test))
    print("GMM: %.3f" % homogeneity_score(gmm.predict(X_test), y_test))

    print("Top terms per cluster:")

    original_space_centroids = svd.inverse_transform(kmeans.cluster_centers_)
    order_centroids = original_space_centroids.argsort()[:, ::-1]

    terms = vectorizer.get_feature_names()
    for i in range(4):
        print("Cluster %d:" % i, end='')
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind], end='')
        print()
