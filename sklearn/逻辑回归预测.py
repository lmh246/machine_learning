from sklearn.model_selection import train_test_split
from sklearn import datasets,linear_model
from sklearn import metrics
from sklearn import preprocessing
if __name__ == '__main__':
    data = datasets.load_iris()
    iris_x = data.data
    iris_y = data.target
    #划分数据
    X_train,X_test,y_train,y_test = train_test_split(iris_x,iris_y,test_size=0.3)
    #初始化对象
    logistic = linear_model.LogisticRegression()
    #训练数据
    logistic.fit(X_train,y_train)
    #预测数据
    res = logistic.predict(X_test)
    print(res)
    print("正确率: ",logistic.score(X_test,y_test))
    print(metrics.classification_report(y_test, res))
    print(metrics.confusion_matrix(y_test, res))


