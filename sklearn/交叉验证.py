from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

if __name__ == '__main__':
    iris = load_iris()
    X = iris.data
    y = iris.target
    k_range = list(range(1,31))
    param_grid = dict(n_neighbours = k_range)
    print(param_grid)
    k_scores = []
    for k in k_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(knn, X, y, cv=10, scoring="accuracy")
        k_scores.append(scores.mean())
    plt.plot(k_range,k_scores)
    plt.xlabel("Value of K for Knn")
    plt.ylabel("Cross-validated Accuracy")
    plt.show()


