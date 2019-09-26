import os
from math import log
import operator

##计算香农熵
##对dataSet的最后一列（标签）分类
def calcShannonEnt(dataSet):
    num=len(dataSet)
    labelCounts={}
    for feaVec in dataSet:
        label=feaVec[-1]
        if label not in labelCounts.keys():
            labelCounts[label]=0
        labelCounts[label]+=1
    shannonEnt=0.0
    for key in labelCounts:
        prob=labelCounts[key]/num
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

##手动创建数据与属性标签
def createDataSet():
    dataSet=[[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels=['no surfacing','flippers']
    return dataSet,labels

##为了度量数据集的无序程度，需要划分数据集来度量划分数据集的熵
##并把已判断的属性数据删掉
def splitDataSet(dataSet,axis,value):
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFeat=featVec[0:axis]
            reducedFeat.extend(featVec[axis+1:])
            retDataSet.append(reducedFeat)
    return retDataSet

##通过计算信息增益来判断当前节点哪个属性更有效
def chooseBestFeatureToSplit(dataSet):
    numFeatures=len(dataSet[0])-1 ##属性数量
    baseEntropy=calcShannonEnt(dataSet)  ##数据集原来的熵
    bestInfoGain=0.0
    bestFeature=-1
    for i in range(numFeatures):   ##对每一个属性计算信息增益，并保留最大的
        featList=[example[i] for example in dataSet]
        uniqueVals=set(featList)  ##先生成列表在生成集合是去重的最好办法
        newEntropy=0.0
        for value in uniqueVals:    ##在每个属性中计算每种取值下的概率与信息熵
            subDataSet=splitDataSet(dataSet,i,value)  
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy+=prob*calcShannonEnt(subDataSet)
        infoGain=baseEntropy-newEntropy
        if infoGain>bestInfoGain:
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature

##当所有属性都使用之后还有类标签依然不是唯一的，就对所有叶子节点多数表决
def majorityCnt(classList):  ##classlist是叶子节点的所有类标签
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True) 
    ##这种字典排序很重要,返回值是一个列表，列表每一项都是元组，第一位是key，第二位是value
    print(sortedClassCount)
    return sortedClassCount[0][0]  

def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]
    if classList.count(classList[0])==len(classList):   ##类别完全相同的话就停止划分
        return classList[0]
    if len(dataSet[0])==1:   ##遍历完所有特征返回出现次数最多的
        return majorityCnt(classList)
    bestFeat=chooseBestFeatureToSplit(dataSet)
    bestFeatLabel=labels[bestFeat]
    myTree={bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues=[example[bestFeat] for example in dataSet]  ##标签所含的所有属性
    uniqueVals=set(featValues)
    for value in uniqueVals:
        subLabels=labels[:]  ##这里复制了类标签，因为python语言中函数参数是列表的时候，参数是按照引用方式传递的？？？
        myTree[bestFeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

def classify(inputTree,featLabels,testVec):
    firstStr=list(inputTree.keys())[0]  ##字典的keys属性类型为dict_keys，可iterable，但是不能indexing。
    secondDict=inputTree[firstStr]
    featIndex=featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex]==key:
            if type(secondDict[key]).__name__=='dict':
                classLabel=classify(secondDict[key],featLabels,testVec)
            else: 
                classLabel=secondDict[key]
    return classLabel


    

    

if __name__ == "__main__":
    mydata,labels=createDataSet()
    labelss=labels[:]  ##labels在createTree中改变了，list做函数参数的时候就会直接再次引用已改变的list，所以这里新建了labelss
    myTree=createTree(mydata,labels)
    print(myTree)
    result=classify(myTree,labelss,[1,0])
    print(result)