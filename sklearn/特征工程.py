from sklearn import datasets,preprocessing
if __name__ == '__main__':
    data = datasets.load_iris()
    iris_x = data.data
    iris_y = data.target
    print("原始数据：\n",iris_x)
    print("标准化：\n",preprocessing.StandardScaler().fit_transform(iris_x))
    print("区间放缩法：\n",preprocessing.MinMaxScaler().fit_transform(iris_x))
    print("二值化： \n",preprocessing.Binarizer(threshold=3).fit_transform(iris_x))
    print("哑编码： \n",preprocessing.OneHotEncoder().fit_transform(iris_y.reshape(-1,1)))

    from numpy import vstack, array, nan
    print("填充缺失值：\n",preprocessing.Imputer().fit_transform(vstack((array([nan, nan, nan, nan]), iris_x))))

    print("多项式变化：\n",preprocessing.PolynomialFeatures().fit_transform(iris_x))

    from numpy import log1p
    print("自定义转换函数：\n",preprocessing.FunctionTransformer(log1p).fit_transform(iris_x))

    from sklearn.feature_selection import VarianceThreshold
    print("方差选择法：\n",VarianceThreshold(threshold=3).fit_transform(iris_x))



    from sklearn.feature_selection import SelectKBest,chi2
    print("卡方检验：\n",SelectKBest(chi2,k=2).fit_transform(iris_x,iris_y))

    from sklearn.feature_selection import RFE
    from sklearn.linear_model import LogisticRegression
    # 参数estimator为基模型
    # 参数n_features_to_select为选择的特征个数
    print("递归特征消除法：\n",RFE(estimator=LogisticRegression(), n_features_to_select=2).fit_transform(iris_x,iris_y))


    from sklearn.feature_selection import SelectFromModel
    from sklearn.linear_model import LogisticRegression
    print("基于惩罚项的特征选择：\n",SelectFromModel(LogisticRegression(penalty="l1",C=0.1)).fit_transform(iris_x,iris_y))

    from sklearn.feature_selection import SelectFromModel
    from sklearn.ensemble import GradientBoostingClassifier
    print("基于树模型特征选择：\n",SelectFromModel(GradientBoostingClassifier()).fit_transform(iris_x,iris_y))