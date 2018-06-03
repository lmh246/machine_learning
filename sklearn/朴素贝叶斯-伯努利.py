# 引入模块
from sklearn import datasets,naive_bayes
from sklearn.model_selection import train_test_split
if __name__ == '__main__':
    data = datasets.load_iris()
    iris_x = data.data
    iris_y = data.target
    # 划分数据
    X_train,X_test,y_train,y_test = train_test_split(iris_x,iris_y,test_size=0.3)
    # 初始化多项式贝叶斯对象
    bnb = naive_bayes.BernoulliNB()
    # 进行训练
    bnb.fit(X_train,y_train)
    # 预测
    res = bnb.predict(X_test)
    print("预测结果：\n",res)

    print(bnb.score(X_test,y_test))


    # #一些属性
    # print("class_log_prior_ : \n",mnb.class_log_prior_)
    # print("intercept_ : \n", mnb.intercept_)
    # print("feature_log_prob_ :  \n",mnb.feature_log_prob_)
    # print("coef_ : \n",mnb.coef_)
    # print("class_count_ :  \n",mnb.class_count_)
    # print("feature_count_ : \n",mnb.feature_count_)