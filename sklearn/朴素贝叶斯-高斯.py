# 引入模块
from sklearn import datasets,naive_bayes
from sklearn.model_selection import train_test_split
if __name__ == '__main__':
    data = datasets.load_iris()
    iris_x = data.data
    iris_y = data.target
    # 划分数据
    X_train,X_test,y_train,y_test = train_test_split(iris_x,iris_y,test_size=0.3)
    # 初始化高斯贝叶斯对象
    gnb = naive_bayes.GaussianNB()
    # 进行训练
    gnb.fit(X_train,y_train)
    # 预测
    res = gnb.predict(X_test)
    print(gnb.score(X_test,y_test))


    #一些属性
    print("class_prior_: \n",gnb.class_prior_)
    print("class_count_: \n", gnb.class_count_)
    print("sigma_ :  \n",gnb.sigma_)