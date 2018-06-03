import random
import math
from decimal import Decimal
from collections import Counter
""""
读取文件
使用自助法选取样本与，测试集
"""
def readData():
    data = []
    #iris
    #label = ['sepal length','sepal width','petal length','petal width']
    #wine
    #label = ['Alcohol','Malic acid','Ash','Alcalinity of ash','Magnesium','Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins','Color intensity','Hue','OD280/OD315 of diluted wines','Proline']
    #redWine
    #label = ["fixed acidity","volatile acidity","citric acid","residual sugar","chlorides","free sulfur dioxide","total sulfur dioxide","density","pH","sulphates","alcohol"]
    #献血
    #label = ["R","F","M","T"]
    #breastTissue
    #label = ["I0","PA500","HFS","DA","AREA","A/DA","MAX IP","DR","P"]
    #harberman
    #label = ["Age","Patient's year","positive axillary nodes detected"]
    #seeds
    label = ["area A","perimeter P","compactness C = 4*pi*A/P^2","length of kernel","width of kernel","asymmetry coefficient","length of kernel groove"]
    dataSet = []
    dataTest = []
    with open('../haberman.data','r') as f:
        for line in f.readlines():
            line = line.strip(' ').strip('\n').split(',')
            #针对redWine，whiteWine
            #line = line.strip(' ').strip('\n').split(';')
            # 针对红酒数据
            # line.append(line[0])
            # del (line[0])
            #breastTissue
            #line = line.strip(' ').strip('\n').split('\t')
            lineBefore = line[:len(line)-1]
            lineBefore = [float(x) for x in lineBefore]
            line = line[-1]
            lineBefore.append(line)
            data.append(lineBefore)
    length = int(len(data)*(2/3))
    for i in range(length):
        index = random.randint(0,100)
        dataSet.append(data[index])

    dataReduce = [item for item in data if item not in dataSet]
    dataTest = dataReduce[:len(dataReduce)-1]
    return dataSet,dataReduce,dataTest,label

"""
计算熵
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
        resultPercent = float(Decimal(str(label[key]))/Decimal(str(dataLen)))
        shannonEnt -= resultPercent * math.log(resultPercent,2)
    return shannonEnt

"""
划分数据
"""
def splitData(data, index, sign, value):
    returnData = []
    if sign == "<":
        for dataItem in data:
            reduceData = []
            if(float(dataItem[index]) <= float(value)):
            #利用列表截断，来获取每条样本特征前后的属性，并利用extend方法进行拼接
                reduceData = dataItem[:index]
                reduceData.extend(dataItem[index+1:])
                returnData.append(reduceData)
    if sign == ">":
        for dataItem in data:
            reduceData = []
            if(float(dataItem[index]) > float(value)):
            #利用列表截断，来获取每条样本特征前后的属性，并利用extend方法进行拼接
                reduceData = dataItem[:index]
                reduceData.extend(dataItem[index+1:])
                returnData.append(reduceData)
    return returnData

"""
选取最好的特征
"""
def chooseBestFeature(data,label):
    featureLen = len(data[0])-1 #属性个数
    #print("属性个数：{}，标签个数：{}".format(featureLen,len(label)))
    baseEnt = calshannonEnt(data) #根节点的熵
    bestFeature = 0
    featureEnt = 0.0
    FeatureDict = {}
    #初始化字典,字典保存每个属性的划分点的数值，信息增益，信息增益率
    for i in range(featureLen):
        FeatureDict[label[i]] = {}
        FeatureDict[label[i]]["T"] = ""
        FeatureDict[label[i]]["Ent"] = 0.0
        FeatureDict[label[i]]["GainRatio"] = 0.0
    #遍历样本每个属性
    for i in range(featureLen):
        featureList = [Item[i] for Item in data]
        featureSet = featureList[:]
        #print(len(featureSet))
        #处理连续值
        #将属性值从小到大进行排序
        featureSet.sort()
        #print(featureSet)
        #计算候选划分点
        houxuanT = [float((Decimal(str(featureSet[i]))+Decimal(str(featureSet[i+1]))))/2.0 for i in range(len(featureSet)-1)]
        #print("属性{0}的候选点有{1}".format(label[i],houxuanT))
        #将样本D基于t划分为两部分
        bestT = 0.0 #候选点t的值
        bestTEnt = 0.0 #候选点t的信息增益
        BestGainRatio = 0.0 #候选点t的信息增益率
        Iv = 0.0
        for value in houxuanT:
            if (value >= featureSet[-1]):
                continue
            Tpos = [] #大于t
            Tneg = [] #小于等于t
            for item in data:
                if item[i] <= value:
                    Tneg.append(item)
                elif item[i] > value:
                    Tpos.append(item)
            TposEnt = calshannonEnt(Tpos)
            TnegEnt = calshannonEnt(Tneg)
            TposPer = len(Tpos)/len(data)
            TnegPer = len(Tneg)/len(data)
            #print("候选点：{}，TposEnt:{},TposPer:{},TnegEnt:{},TnegPer:{}".format(value,TposEnt,TposPer,TnegEnt,TnegPer))
            GainFeatureEntOfT = float(Decimal(str(baseEnt)) - Decimal(str(TposPer*TposEnt)) - Decimal(str(TnegPer*TnegEnt)))
            Iv = -(TposPer * math.log(TposPer,2) + TnegPer * math.log(TnegPer,2))
            GainRatio = float(Decimal(str(GainFeatureEntOfT))/Decimal(str(Iv)))
            #print("划分点 {0} 的信息增益是 {1},信息增益率是{2}".format(value,GainFeatureEntOfT,GainRatio))
            if GainFeatureEntOfT > bestTEnt:
                bestTEnt = GainFeatureEntOfT
                bestT = value
                BestGainRatio = GainRatio

        #print("属性{0}的划分点为{1}，其信息增益为{2}，信息增益率为{3}\n".format(label[i],bestT,bestTEnt,BestGainRatio))
        FeatureDict[label[i]]["Ent"] = bestTEnt
        FeatureDict[label[i]]["T"] = bestT
        FeatureDict[label[i]]["GainRatio"] = BestGainRatio
    #计算所有属性的平均增益
    sum = 0.0
    for value in FeatureDict.values():
        sum = sum + value["Ent"]
    averageEnt = sum/featureLen
    #找出属性增益高于平均增益的属性
    FeatureHighDict = {k:v for k,v in FeatureDict.items() if v["Ent"] >= averageEnt}
    #选择高于平均水平的属性的信息增益率
    BestFeatureName = ''
    BestFeatureSplit = 0.0
    BestRatio = 0.0
    for key in FeatureHighDict.keys():
        if(FeatureHighDict[key]["GainRatio"]>BestRatio):
            BestFeatureName = key
            BestFeatureSplit = FeatureHighDict[key]["T"]
    #找出属性的下标
    for i in range(len(label)):
        if(label[i] == BestFeatureName):
            bestFeature = i
    print("信息增益率最大的属性{0}的划分点为{1},属性在列表中的位置为{2}".format(BestFeatureName,BestFeatureSplit,bestFeature))
    return bestFeature,BestFeatureName,BestFeatureSplit

"""
定义生成树
"""
def createTree(data,labels):
    value = []
    classList = [example[-1] for example in data] #找出所有决策结果
    #如果只有一个类别，就返回结果
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(data[0]) == 1: #如果只有一列，返回出现结果最多的类别
        result_counts = Counter(classList)
        return result_counts.most_common(1)[0][0]
    bestFeature,BestFeatureName,BestFeatureSplit = chooseBestFeature(data,labels)
    #featureDic.extend([BestFeatureName,BestFeatureSplit])
    bestLabel = labels[bestFeature]
    myTree = {bestLabel:{}}
    #找出出去最优属性的属性列表
    del(labels[bestFeature])
    #print("剩余标签：",subLabels)
    left = "<"+str(BestFeatureSplit)
    right = ">"+str(BestFeatureSplit)
    value = [left,right]
    for x in value:
        subLabels = labels[:]
        sign = x[0]
        splitDataSet = splitData(data,bestFeature,sign,BestFeatureSplit)
        myTree[bestLabel][x] = createTree(splitDataSet,subLabels)
    #print(myTree)
    return myTree
"""
判断测试用例
"""
def classify(myTree,labels,dataTest):
    rootFeature = list(myTree.keys())[0]#根节点，判断属性
    # 找到该特征下的所有子集
    rootItems = myTree[rootFeature]
    # 找到根特征在每一条属性标签中所处的位置
    rootIndex = labels.index(rootFeature)
    # 找到该测试样本该特征的值
    rootKey = dataTest[rootIndex]
    # 获取该特征具体值下所有的子集
    rootItemsKey = float(list(rootItems.keys())[0][1:])
    global featureLabelOnce
    if rootKey<=rootItemsKey:
        featureLabelOnce = '<' + str(rootItemsKey)
    elif rootKey>rootItemsKey:
        featureLabelOnce = '>' + str(rootItemsKey)
    reduce = rootItems[featureLabelOnce]
    # 判断有没有结束
    if isinstance(reduce, dict):
        result = classify(reduce, labels, dataTest)
    else:
        result = reduce
    return result





if __name__ == '__main__':
    dataSet,dataReduce, dataTest, label = readData()
    print(dataSet)
    inputTree = createTree(dataSet,label)
    print(inputTree)
    #iris
    #label = ['sepal length','sepal width','petal length','petal width']
    #wine
    #label = ['Alcohol','Malic acid','Ash','Alcalinity of ash','Magnesium','Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins','Color intensity','Hue','OD280/OD315 of diluted wines','Proline']
    #redWine
    #label = ["fixed acidity","volatile acidity","citric acid","residual sugar","chlorides","free sulfur dioxide","total sulfur dioxide","density","pH","sulphates","alcohol"]
    #献血
    #label = ["R","F","M","T"]
    #breastTissue
    #label = ["I0","PA500","HFS","DA","AREA","A/DA","MAX IP","DR","P"]
    #harberman
    #label = ["Age","Patient's year","positive axillary nodes detected"]
    #seeds
    label = ["area A","perimeter P","compactness C = 4*pi*A/P^2","length of kernel","width of kernel","asymmetry coefficient","length of kernel groove"]
    count = 0
    for item in dataTest:
        result = classify(inputTree, label, item)
        Trueresult = item[-1]
        if(result == Trueresult):
            count = count + 1
    TruePer = round(count/len(dataTest),4)
    print('正确率为{}%'.format(TruePer*100))



