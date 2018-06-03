
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn import preprocessing,datasets
if __name__ == '__main__':
    iris = datasets.load_breast_cancer()
    X = iris.data
    X = preprocessing.normalize(X)
    y = iris.target
    k_range = list(range(1,31))
    param_grid = dict(n_neighbors = k_range)
    knn = KNeighborsClassifier(n_neighbors=5)
    grid = GridSearchCV(knn,param_grid,cv=10,scoring="accuracy")
    grid.fit(X,y)
    grid_mean_score = grid.cv_results_["mean_test_score"]
    plt.plot(k_range,grid_mean_score)
    plt.xlabel('Value of K for KNN')
    plt.ylabel('Cross-Validated Accuracy')
    plt.show()
    print(grid.best_score_)
    print(grid.best_params_)
