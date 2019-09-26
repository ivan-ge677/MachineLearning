from numpy import exp,arange
from numpy import mat,shape,ones,array
import matplotlib.pyplot as plt
import os
import random


def loadDataSet():
    dataMat=[];labelMat=[]
    fr=open('testSet.txt')
    for line in fr.readlines():
        lineArr=line.strip().split()
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))
#梯度上升优化算法
def gradAscent(dataMatIn,classLabels):
    ##转化为矩阵，方便下面计算
    dataMatrix=mat(dataMatIn)
    labelMat=mat(classLabels).transpose()
    m,n=shape(dataMatrix)
    alpha=0.001
    maxCycles=500
    weights=ones((n,1))
    for k in range(maxCycles):
        h=sigmoid(dataMatrix*weights)
        error=labelMat-h
        weights=weights+alpha*dataMatrix.transpose()*error  ##有数学运算
    return weights

##画出决策边界
def plotBestFit(weights):
    dataMat,labelMat=loadDataSet()
    dataArr=array(dataMat)
    n=shape(dataArr)[0]
    xcord1=[];ycord1=[];xcord2=[];ycord2=[]
    for i in range(n):
        if int(labelMat[i])==1:
            xcord1.append(dataArr[i,1])
            ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1])
            ycord2.append(dataArr[i,2])
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(xcord1,ycord1,s=30,c='red',marker='s')
    ax.scatter(xcord2,ycord2,s=30,c='green')
    x=arange(-3.0,3.0,0.1)
    #print(shape(x))
    y=(-weights[0]-weights[1]*x)/weights[2]  ##使用sigmoid函数时，0.5时边界，不使用的时候0是边界
    #print(shape(y))
    ax.plot(x,y.transpose())
    plt.xlabel('X1');plt.ylabel('X2')
    plt.show()

##改进的随机梯度上升算法
def stocGradAscent1(dataMatrix,classLabels,numIter=150):
    m,n=shape(dataMatrix)
    dataMatrix=array(dataMatrix)  ##list不能直接×一个数，array可以
    weights=ones(n)
    for j in range(numIter):
        dataIndex=list(range(m))##这里用list
        for i in range(m):
            ##alpha在每次计算都调整可以减少结果的高频波动。
            alpha=4/(1.0+j+i)+0.01
            randIndex=int(random.uniform(0,len(dataIndex)))
            h=sigmoid(sum(dataMatrix[randIndex]*weights))
            error=classLabels[randIndex]-h
            weights=weights+alpha*error*dataMatrix[randIndex]
            del(dataIndex[randIndex])    ##range类型不能del，要改为list
    return weights

if __name__ == "__main__":
    os.chdir('C:/Users/think/Documents/学习/python程序/.vscode/AiLearning-master/AiLearning-master/data/5.Logistic')
    mydata,mylabel=loadDataSet()
    #weights=gradAscent(mydata,mylabel)
    weights=stocGradAscent1(mydata,mylabel)
    plotBestFit(weights)