#引入模块
from sklearn import datasets,tree
from sklearn.model_selection import train_test_split
import graphviz
if __name__ == '__main__':
    #引入数据
    iris = datasets.load_iris()
    iris_x = iris.data
    iris_y = iris.target
    iris_label = iris.feature_names
    #划分数据
    X_train,X_test,y_train,y_test = train_test_split(iris_x,iris_y,test_size=0.3)
    #初始化决策树对象
    DecTree = tree.DecisionTreeClassifier()
    #进行训练
    DecTree.fit(X_train,y_train)
    #进行预测
    res = DecTree.predict(X_test)
    print(DecTree.score(X_test,y_test))



    #一些类的属性
    # print("Classes_: \n",DecTree.classes_)
    # print("feature_importances_: \n",DecTree.feature_importances_)
    # print("max_features_: \n",DecTree.max_features_)
    # print("n_classes_: \n",DecTree.n_classes_)
    # print("n_features_: \n",DecTree.n_features_)
    # print("n_outputs_: \n",DecTree.n_outputs_)
    # print("tree_",DecTree.tree_)
    # print(DecTree.decision_path(X_test))
    # print("get_para: \n",DecTree.get_params())
    # print("log_prota: \n",DecTree.predict_log_proba(X_test))
    # print("proba: \n",DecTree.predict_proba(X_test))
    # print("score： \n",DecTree.score(X_test,y_test))


    #决策树可视化
    # dot_data = tree.export_graphviz(DecTree,out_file=None,
    #                                 feature_names=iris.feature_names,
    #                                 class_names=iris.target_names,
    #                                 filled=True,rounded=True,
    #                                 special_characters=True)
    # graph = graphviz.Source(dot_data)
    # graph.render("iris")


