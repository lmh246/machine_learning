from sklearn.model_selection import train_test_split
from sklearn import datasets,svm
if __name__ == '__main__':
    data = datasets.load_iris()
    iris_x = data.data
    iris_y = data.target
    #划分数据
    X_train,X_test,y_train,y_test = train_test_split(iris_x,iris_y,test_size=0.3)
    #初始化svm对象
    sv = svm.SVC(C=1,kernel='rbf',gamma='auto',decision_function_shape='ovr')
    #训练数据
    sv.fit(X_train,y_train)
    #预测数据
    res = sv.predict(X_test)
    print("预测结果：",res)
    print("正确率： ",sv.score(X_test,y_test))
