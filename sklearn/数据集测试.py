import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV,train_test_split,cross_val_score
import time

#定义Knn算法：
def Knn(Xval,yVal):
    from sklearn.neighbors import KNeighborsClassifier
    start = time.clock()
    X = Xval
    X = preprocessing.normalize(X)
    y = yVal
    k_range = list(range(1, 31))
    param_grid = dict(n_neighbors=k_range)
    knn = KNeighborsClassifier(n_neighbors=5)
    grid = GridSearchCV(knn, param_grid, cv=10, scoring="accuracy")
    grid.fit(X, y)
    end = time.clock()
    print("Knn执行时间",end-start)
    return grid.best_score_,grid.best_params_

#定义决策树算法
def jueceshu(Xval,yVal):
    from sklearn import tree
    start = time.clock()
    X = Xval
    y = yVal
    depth_range = list(range(1,10))
    param_grid = dict(max_depth=depth_range)
    Dectree = tree.DecisionTreeClassifier(max_depth=5)
    grid = GridSearchCV(Dectree,param_grid,cv=10,scoring="accuracy")
    grid.fit(X,y)
    end = time.clock()
    print("决策树执行时间：",end-start)
    return grid.best_score_, grid.best_params_

#定义朴素贝叶斯算法
def Gbayes(Xval,yVal):
    from sklearn import naive_bayes
    start = time.clock()
    X = Xval
    y = yVal
    # 初始化高斯贝叶斯对象
    gnb = naive_bayes.GaussianNB()
    scores = cross_val_score(gnb,X,y,cv=10,scoring="accuracy")
    end = time.clock()
    print("朴素贝叶斯执行时间：",end-start)
    return scores.mean()

#定义Svm算法
def svmSvc(Xval,yVal):
    from sklearn import svm
    start = time.clock()
    X = Xval
    y = yVal
    param_grid = {'kernel':('linear','rbf'),'C':[1,10]}
    svc = svm.SVC()
    grid = GridSearchCV(svc,param_grid,cv=10,scoring="accuracy")
    grid.fit(X,y)
    end = time.clock()
    print("Svm执行时间：",end-start)
    return grid.best_score_, grid.best_params_

#定义逻辑回归函数
def Logis(Xval,yVal):
    from sklearn import linear_model
    start = time.clock()
    X = Xval
    y = yVal
    LogiClass = linear_model.LogisticRegression()
    scores = cross_val_score(LogiClass, X, y, cv=10, scoring="accuracy")
    end = time.clock()
    print("逻辑回归执行时间：",end-start)
    return scores.mean()

#读取文件
def readData(url):
    X = []
    y = []
    with open(url, 'r') as f:
        data = f.readlines()  # txt中所有字符串读入data
        for line in data:
            #odom = line.strip('').strip('\n').split("\t") # 将单个数据分隔开存好
            odom = line.strip('').strip('\n').split(",")  # 将单个数据分隔开存好
            numbers_float = [float(x) for x in odom[:len(odom)-1] if x is not '']  # 转化为浮点数
            X.append(numbers_float)
            y.append(odom[-1])
    print(X)
    print(y)
    return X,y


if __name__ == '__main__':
    score = []
    #dataName = datasets.load_iris()
    #dataName = datasets.load_breast_cancer()
    #dataName = datasets.load_wine()
    # X = dataName.data
    # y = dataName.target
    #X,y = readData("./seeds.txt")
    X,y = readData("cmc.data")
    #Knn
    Knn_score,Knn_param = Knn(X,y)
    score.append(round(Knn_score,4))
    #决策树
    jueceshu_score, jueceshu_param = jueceshu(X,y)
    score.append(round(jueceshu_score, 4))
    #贝叶斯
    Gbayes_score = Gbayes(X,y)
    score.append(round(Gbayes_score, 4))
    #Svm
    Svm_score,Svm_param = svmSvc(X,y)
    score.append(round(Svm_score,4))
    #逻辑回归
    Logis_score = Logis(X,y)
    score.append(round(Logis_score,4))
    arr = np.array(score)
    result = pd.DataFrame(arr,index=["Knn算法","决策树算法","朴素贝叶斯算法","Svm算法","逻辑回归算法"],columns=["正确率"])
    print(result)




