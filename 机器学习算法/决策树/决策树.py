import math
from collections import Counter
"""
计算根节点的熵

首先定义传入的训练数据类型为（a1,a1,a3,...an,y）其中a代表那个样本的属性，y代表分类的结果

定义的变量：
    dataLen: 样本个数
    label: 分类结果及其每个结果出现的次数，已字典的形式
    shannonEnt: 根节点的熵
"""
def calshannonEnt(data):
    dataLen = len(data)
    label = {}
    #遍历每一条样本，找出结果
    for dataItem in data:
        #取出每一条样本的结果,并判断是否在label中
        currentResult = dataItem[-1]
        if currentResult not in label.keys():
            label[currentResult] = 0
        label[currentResult] += 1

    #求根节点的熵
    shannonEnt = 0.0
    for key in label:
        resultPercent = float(label[key])/dataLen
        shannonEnt -= resultPercent * math.log(resultPercent,2)
    return shannonEnt

"""
按照给定的特征的值，来划分数据

返回值：样本中的特征值与给定的特征的特征值相等的样本，并且去掉该特征

定义的变量：
data: 数据集
index: 特征在每一个样本的下标
value: 特征值
"""
def splitData(data, index, value):
    returnData = []
    for dataItem in data:
        reduceData = []
        if(dataItem[index] == value):
            #利用列表截断，来获取每条样本特征前后的属性，并利用extend方法进行拼接
            reduceData = dataItem[:index]
            reduceData.extend(dataItem[index+1:])
            returnData.append(reduceData)
    return returnData

"""
选择最好的数据集划分方式

判断条件是信息增益

返回值：特征的下标

定义的变量：
featureLen：属性的个数
baseEnt：根节点的熵
featureList：保存属性的所有子属性
gainEnt：信息增益
bestEnt：最好的信息增益
bestFeature：最好的特征，即信息增益最大的熵
"""
def chooseBestFeature(data):
    featureLen = len(data[0])-1
    baseEnt = calshannonEnt(data)
    bestEnt = 0.0
    bestFeature = -1
    featureEnt = 0.0
    #遍历样本每个属性
    for i in range(featureLen):
        featureList = [Item[i] for Item in data]
        #对属性列表去重
        featureSet = set(featureList)
        #循环遍历每个属性的子属性
        for value in featureSet:
            reduceData = splitData(data,i,value)
            print("特征 {0} 的子特征 {1} 包含的样本：{2}".format(i, value, reduceData))
            #计算每个子属性占所有样本的百分比
            percent = float(len(reduceData))/len(data)
            #计算每个子属性的熵
            featureItemEnt = calshannonEnt(reduceData)
            print('子特征分类下的样本占总样本 {0} ，其熵为{1}'.format(percent, featureItemEnt))
            #计算属性的熵
            featureEnt = featureEnt + percent * featureItemEnt
        #计算属性的信息增益
        gainEnt = baseEnt - featureEnt
        print("原始熵 = {0}, 特征的熵 = {1}, 信息增益 = {2}".format(baseEnt, featureEnt, gainEnt))
        if(gainEnt > bestEnt):
            bestEnt = gainEnt
            bestFeature = i
    return bestFeature

"""
定义生成树
如果只有一个类别，就直接返回结果

如果每个样本只有一列，就返回出现次数最多的结果

一般情况：
先找出所有属性的最好特征
然后找出最好特征的子属性，并在每一个子属性下找到剩余特征中最好的特征，重复步骤
"""
def createTree(data,labels):
    classList = [example[-1] for example in data]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(data[0]) == 1:
        result_counts = Counter(classList)
        return result_counts.most_common(1)[0][0]
    bestFeature = chooseBestFeature(data)
    bestLabel = labels[bestFeature]
    myTree = {bestLabel:{}}
    featValues = [example[bestFeature] for example in data]
    uniqueValues = set(featValues)
    for value in uniqueValues:
        subLabels = labels[bestFeature + 1:]
        myTree[bestLabel][value] = createTree(splitData(data,bestFeature,value),subLabels)
    print(myTree)
    return myTree

"""
利用决策树来进行分类，思路：
首先找出决策树的根节点的特征在所有属性中的位置
然后找出根特征所有的子集
找出测试用例该特征所属的子集
把该子集做成新的决策树
"""
def classify(inputTree,featLabels,test):
    rootFeature = list(inputTree.keys())[0]
    #找到该特征下的所有子集
    rootItems = inputTree[rootFeature]
    #找到根特征在每一条样本中所处的位置
    rootIndex = featLabels.index(rootFeature)
    #找到该测试样本该特征的值
    rootKey = test[rootIndex]
    #获取该特征具体值下所有的子集
    reduceItem = rootItems[rootKey]
    print('+++',rootFeature,'---',rootItems,'<<<',rootKey,'...',reduceItem)

    #判断有没有结束
    if isinstance(reduceItem,dict):
        result = classify(reduceItem,featLabels,test)
    else:
        result = reduceItem
    return result

if __name__ == '__main__':
    data = [
        [1, 0, 'no'],
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [0, 1, 'no'],
        [0, 1, 'no']
    ]
    labels = ['no surfacing', 'flippers']
    inputTree = createTree(data, labels)
    classify(inputTree, labels, [0, 0])

