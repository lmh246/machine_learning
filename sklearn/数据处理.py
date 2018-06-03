from sklearn import preprocessing
import numpy as np
if __name__ == '__main__':
    X = np.array([[1.,-1.,2.],
                  [2.,0.,0.],
                  [0.,1.,-1.]])
    X_mean = X.mean(axis=0) #计算列的平均值
    X_std = X.std(axis=0)   #计算列的方差
    X1 = (X-X_mean)/X_std
    X_scale = preprocessing.scale(X)
    print("公式计算：",X1)
    print("模块计算：",X_scale)

    X = np.array([[1.,-1.,2.],
                  [2.,0.,0.],
                  [0.,1.,-1.]])
    X_norm = preprocessing.normalize(X)
    print("正则化：\n",X_norm)