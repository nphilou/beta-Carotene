# Catégorisation de textes

#### 1

L'algorithme EM est un algorithme itératif d'estimation paramétrique, les deux
étapes principales sont l'estimation (étape E) de données inconnues à partir de
lois de probabilités connues et paramètres calculés à l'étape M précédente.
L'étape M consiste à modifier les paramètres suivant les données générées afin
de maximiser la vraisemblance.

Cet algorithme peut être décrit par le pseudocode suivant :

```
Soient theta les paramètres d'une fonction de probabilité P
Soient N le nombre d'individus
Soient M le nombre de clusters
Y matrice N, M des y_nm

i = 1
eps = 1e-3
Initialiser theta(i) aléatoirement
convergence = Faux
Tant que (convergence != Vrai):
    # Etape E
    Pour (n, m) allant de (1, 1) à (N, M):
        # calcul des probabilités P(z=m | x) que l'individu n appartiennent au cluster m sachant theta(i)
        y_nm = estimeClusterIndividus(theta(i))
    FinPour
        
    # Etape M
    # calcul des paramètres, soit theta(i+1) tels que la vraisemblance est maximisée
    theta(i+1) = estimeParametresMaxVraisemblance(Y)

    # Critère d'arrêt
    Si |theta(i) - theta(i+1)| < eps:
        convergence = Vrai
    FinSi

    i = i+1
FinTantQue

y_nm = estimeClusterIndividus(theta(i))
Retourner theta(i)
```

#### 3

Dans le code fourni, nous avons utilisé *TfidfVectorizer* avec le paramètre **stop_words='english'** afin de ne pas 
tenir compte des mots vides tels que [i, me, my, myself, we] fournis par la librairie *NLTK*.

De plus, nous avons appliqué une lemmatisation avec l'outil *SnowballStemmer* de la librairie *NLTK* également.

#### 4

Pour cette étape, nous avons choisi de garder 10 composants pour limiter le problème du *curse of dimensionality* qui 
empêcherait de faire des clusters pertinents mais également limiter le risque de perte d'information

Une normalisation est appliquée sur la matrice obtenue.

#### 5

En considérant 4 clusters, on parvient à obtenir une homogénéité de **0.64** sur l'ensemble X_train et **0.61** sur 
X_test

#### 6

Avant d'appliquer l'algorithme EM, nous avons choisi de vérifier la distribution des données. 

TODO : décrire les histo

Elle semblent suivrent un mélange de fonctions de probabilité gaussiennes, ce qui rend donc pertinent l'utilisation de 
l'algorithme EM et plus particulièrement la fonction *GaussianMixture* qui permet de déterminer les paramètres 
(moyenne, covariance) des 4 fonctions.