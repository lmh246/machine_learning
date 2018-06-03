import math
from decimal import Decimal
import random
from collections import Counter
"""
读取文件
返回属性，类别
"""
def readData():
    data = []
    dataLable = []
    with open('../seeds_dataset.txt','r') as f:
        for line in f.readlines():
            # seeds
            line = line.strip(" ").strip('\n').split('\t')
            line = [float(x) for x in line if x is not '']
            # 针对redWine，whiteWine
            #line = line.strip(' ').strip('\n').split(';')
            #line = line.strip(' ').strip('\n').split(',')
            # 针对红酒数据
            # line.append(line[0])
            # del (line[0])
            # line = line.strip(' ').strip('\n').split('\t')
            dataLable .append(line[:len(line)])
            lineBefore = line[:len(line) - 1]
            lineBefore = [float(x) for x in lineBefore]
            data.append(lineBefore)
    return data,dataLable

"""
计算两个样本的距离
选用欧氏距离
"""
def calDistance(sample,test):
    length = len(data[0]) #计算每个样本属性个数
    sum = 0
    for index in range(length):
        subtraction = float(Decimal(str(test[index]))-Decimal(str(sample[index])))
        sum = sum + subtraction**2
    result = math.sqrt(sum)
    return result

"""
随机选取样本集中K个样本作为初始值
"""
def SelectK(data,k):
    length = len(data)
    kList = []
    randomdata = range(length)
    kList = random.sample(randomdata, k)
    kValue = [data[i] for i in kList]
    return kValue

"""
求均值向量
"""
def means(dataSet,data):
    length = len(dataSet[data[0]])
    dataLen = len(data)
    newVec = []
    for i in range(length):
        result = 0
        for index in range(dataLen):
            result = result + dataSet[data[index]][i]
        newVec.append(result/dataLen)
    return newVec
"""
比较列表
"""
def compareList(list1,list2):
    count = 0
    if len(list1)==len(list2):
        for i in range(len(list1)):
            if list1[i] == list2[i]:
                count = count + 1
        if count == len(list1):
            return 1
        else:
            return 0
    else:
        return 0


"""
K-means函数体
"""
def kMeans(data,k):
    dataLen = len(data) #计算数据个数
    centroids = SelectK(data,k) #s随机选取k个样本
    clusterChanged = True #判断集群是否变化，初始值为True
    count = 1 #计算循环次数
    while clusterChanged:
        #print("旧的质点为",centroids)
        clusterAssment = [list() for i in range(k)]  # 存放分类
        clusterChanged = False
        closeIndex = 0 #存放与当前样本距离最近的质点的下标
        for index in range(dataLen):
            distance = 10000000 #存放当前样本与质点的距离
            for i in range(k):
                distanceOrign = calDistance(centroids[i],data[index])
                if distanceOrign < distance:
                    distance = distanceOrign
                    closeIndex = i
            clusterAssment[closeIndex].append(index) #将样本下标存入最近的质点
        print("第{}次迭代".format(count))
        for i in range(k):
            print("第{}个分类有{}个样本".format(i,len(clusterAssment[i])))
        for i in range(k):
            newVec = means(data,clusterAssment[i])
            value = compareList(centroids[i],newVec)
            if value == 0:
               clusterChanged = True
               centroids[i] = newVec
        #print("新的选取的质点为",centroids)
        count = count + 1
    return clusterAssment,centroids


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






if __name__ == '__main__':
    k = 3
    Meanslabel = []
    data,dataLable = readData()
    data = autoNorm(data)
    clusterAssment, centroids = kMeans(data,k)
    #判断每一类的类别
    for i in range(k):
        lable = []
        for index in clusterAssment[i]:
            lable.append(dataLable[index][-1])
        result_counts = Counter(lable)
        Meanslabel.append(result_counts.most_common(1)[0][0])
    print("最终聚类的结果")
    for i in range(k):
        print("第{}类有{}个样本，他的类别是{}".format(i+1,len(clusterAssment[i]),Meanslabel[i]))

    print("原始数据为")
    huizong = {}
    for item in dataLable:
        current = item[-1]
        if current not in huizong.keys():
            huizong[current] = 0
        huizong[current] += 1
    print(huizong)

