#引入模块
from sklearn import neighbors,datasets
from sklearn.model_selection import train_test_split
#随机划分数据的模块
if __name__ == '__main__':
    #引入iris数据
    iris = datasets.load_iris()
    iris_X = iris.data
    iris_y = iris.target
    #划分数据集
    X_train,X_test,y_train,y_test = train_test_split(iris_X,iris_y,test_size=0.3)
    #初始化一个对象
    knn = neighbors.KNeighborsClassifier()
    #进行训练
    knn.fit(X_train,y_train)
    print(knn.get_params(deep=True))
    print("keigh",knn.kneighbors())
    #进行预测
    knnRes = knn.predict(X_test)
    print("正确结果：",y_test)
    print("预测结果：",knnRes)
    print(knn.predict_proba(X_test))
    length = int(len(y_test))
    count = 0
    for index in range(length):
        if(y_test[index] == knnRes[index]):
            count = count + 1
    print("正确率是：",count/length)
