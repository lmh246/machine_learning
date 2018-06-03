from decimal import Decimal
from collections import Counter
import random
import math
"""
读取文件
返回属性，类别
"""
def readData():
    data = []
    dataSet = []
    dataTest = []
    with open('../seeds_dataset.txt','r') as f:
        for line in f.readlines():
            #line = line.strip(' ').strip('\n').split(',')
            # 针对redWine，whiteWine
            #line = line.strip(' ').strip('\n').split(';')
            #针对红酒数据
            # line.append(line[0])
            # del(line[0])
            # breastTissue
            #line = line.strip(' ').strip('\n').split('\t')
            #seeds
            line = line.strip(" ").strip('\n').split('\t')
            line = [float(x) for x in line if x is not '']
            lineBefore = line[:len(line) - 1]
            lineBefore = [float(x) for x in lineBefore]
            line = line[-1]
            lineBefore.append(line)
            data.append(lineBefore)
    length = len(data)
    lengthSel = int(len(data) * (2 / 3))
    randomdata = range(length)
    randomlist = random.sample(randomdata,lengthSel)
    for i in randomlist:
        dataSet.append(data[i])
    for i in range(length):
        if i not in randomlist:
            dataTest.append(data[i])
    return dataSet,dataTest

"""
数据归一化

"""
def autoNorm(data):
    length = len(data[0]) #计算属性个数
    for i in range(length):
        FeatureValue = [item[i] for item in data] #保存一个属性的所有值
        minval = min(FeatureValue) #计算属性的最小值
        maxVal = max(FeatureValue) #计算属性的最大值
        ranges = float(Decimal(str(maxVal)) - Decimal(str(minval))) #计算极差
        for item in data:
           item[i] = float(Decimal(str((item[i] - minval)))/Decimal(str(ranges)))
    return data

"""
计算距离
传入4个参数，测试样本，训练样本，标签，k值
"""
def classify(testDemo,dataSet,label,k):
    lengthFeature = len(dataSet[0]) #获取属性个数
    lengthTrain = len(dataSet) #获取训练样本个数
    dataDic = {} #存放测试样本与每个训练样本的值
    #计算距离度量
    for index in range(lengthTrain):#取出每个训练样本的下标
        result = 0.0
        for i in range(lengthFeature):
            x = (dataSet[index][i] - testDemo[i])**2
            result = result + x
        dataDic[index] = math.sqrt(result)
    #对字典按照值进行排序
    dataDic = sorted(dataDic.items(),key=lambda item: item[1])
    #取前k个值
    dataFinal = [dataDic[i] for i in range(k)]
    #获取前K的值的标签
    dataLabel = []
    for items in dataFinal:
        item = label[items[0]]
        dataLabel.append(item[-1])
    result_counts = Counter(dataLabel)
    return result_counts.most_common(1)[0][0]

if __name__ == '__main__':
    label = []
    dataSet1,dataTest1 = readData()
    #处理数据。去掉类别
    dataSet2 = [item[:len(dataSet1[0])-1] for item in dataSet1]
    dataTest2 = [item[:len(dataSet1[0])-1] for item in dataTest1]
    dataSet = autoNorm(dataSet2)
    dataTest = autoNorm(dataTest2)
    print(dataSet1)
    print(dataTest1)
    print("训练样本个数：",len(dataSet))
    print("测试样本个数",len(dataTest))
    lengthTest = len(dataTest)
    count = 0
    for index in range(lengthTest):
        TrueResult = dataTest1[index][-1]
        result = classify(dataTest[index],dataSet,dataSet1,7)
        if(result==TrueResult):
            count = count+1

    print("判断正确个数",count)
    TruePer = round(count/lengthTest,3)

    print("准确率为{}%".format(TruePer*100))