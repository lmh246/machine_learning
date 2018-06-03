from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn.model_selection import train_test_split
if __name__ == '__main__':
    iris = datasets.load_iris()
    X_train,X_test,y_train,y_test = train_test_split(iris.data,iris.target,test_size=0.3)
    Kmean = KMeans(n_clusters=3,random_state=0)
    s = Kmean.fit(X_train)
    res = Kmean.predict(X_test)
    print("正确率：",Kmean.score(X_test,y_test))
    print("簇的中心\n",s.cluster_centers_)
    print("每个样本所属的簇：\n",s.labels_)
    print("评估簇的个数是否合适：\n",s.inertia_)
