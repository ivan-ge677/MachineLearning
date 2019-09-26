from numpy import *
from math import exp
import os
import matplotlib.pyplot as plt

##加载数据
def loadDataSet(filename):
    numFeat=len(open(filename).readline().split('\t'))-1
    dataMat=[];labelMat=[]
    fr=open(filename)
    for line in fr:
        lineArr=[]
        curline=line.strip().split('\t')
        dataMat.append([float(val) for val in curline[0:numFeat]])
        labelMat.append(float(curline[-1]))
    return dataMat,labelMat

##标准线性回归
def standRegres(xArr,yArr):
    xMat=mat(xArr);yMat=mat(yArr).T
    xTx=xMat.T*xMat
    if linalg.det(xTx)==0:
        print('This matrix is singular,cannoot do inverse')
        return 
    ws=xTx.I*(xMat.T*yMat)
    ## ws=linalg.solve(xTx,xMat.T*yMat)
    fig=plt.figure(1)
    ax1=plt.subplot(221)
    ax1.scatter(xMat[:,1].flatten().A[0],yMat[:,0].flatten().A[0],s=10)
    xCopy=xMat.copy()
    #xCopy.sort(0)  排序的目的是为了在画图的时候不会出现数据点次序混乱
    yHat=xCopy*ws
    ax1.plot(xCopy[:,1],yHat)
    corr=corrcoef(yHat.T,yMat.T) #相关系数
    #print(corr)
    return ws 

##局部加权线性回归
def lwlr(testPoint,xArr,yArr,k=1.0):
    xMat=mat(xArr);yMat=mat(yArr).T
    m=shape(xMat)[0]
    weights=mat(eye((m)))
    for j in range(m):
        diffMat=testPoint-xMat[j,:]
        weights[j,j]=exp(diffMat*diffMat.T/(-2.0*k**2))
    xTx=xMat.T*(weights*xMat)
    if linalg.det(xTx)==0.0:
        print("This matrix is singular, cannot do inverse")
        return 
    ws=xTx.I*(xMat.T*(weights*yMat))
    return testPoint * ws

def lwlrTest(testArr,xArr,yArr,k=1.0):
    xMat=mat(xArr);yMat=mat(yArr).T
    m=shape(testArr)[0]
    yHat=zeros(m)
    for i in range(m):
        yHat[i]=lwlr(testArr[i],xArr,yArr,k)
    ind=array(testArr)[:,1].argsort(0)
    xSort=array(testArr)[ind,1]
    ax2=plt.subplot(222)
    ax2.scatter(xMat[:,1].flatten().A[0],yMat[:,0].flatten().A[0],s=10)
    ax2.plot(xSort,yHat[ind],c='red')
    return yHat

##当数据特征比样本点还多的时候就需要缩减系数

#岭回归
#对特征进行标准化处理
def ridgeRegres(xMat,yMat,lam=0.2):
    xTx=xMat.T*xMat
    denom=xTx+eye(shape(xMat)[1])*lam
    if linalg.det(denom)==0:
        print('This matrix is singular')
        return
    ws=denom.I*(xMat.T*yMat)
    return ws

def ridgeTest(xArr,yArr):
    xMat=mat(xArr);yMat=mat(yArr).T
    yMean=mean(yMat,0)
    yMat=yMat-yMean
    xMeans=mean(xMat,0)
    xVar=var(xMat,0)
    xMat=(xMat-xMeans)/xVar
    numTestPts=30
    wMat=zeros((numTestPts,shape(xMat)[1]))
    for i in range(numTestPts):
        ws=ridgeRegres(xMat,yMat,exp(i-10))
        wMat[i,:]=ws.T
    ax3=plt.subplot(223)
    ax3.plot(wMat)
    return wMat

#计算预测误差
def rssError(yArr,yHatArr):
    return((yArr-yHatArr)**2).sum()
##标准化
def regularize(xMat):
    inMat=xMat.copy()  ##列表是一种数据结构，调用函数可以改变数据结构，也就是函数内部改变列表的话，外部也会被改变。
    inMeans=mean(inMat,0)
    inVar=var(inMat,0)
    inMat=(inMat-inMeans)/inVar
    return inMat

##前向逐步回归
def stageWise(xArr,yArr,eps=0.01,numIt=100):
    xMat=mat(xArr);yMat=mat(yArr).T
    yMean=mean(yMat,0)
    yMat=yMat-yMean
    xMat=regularize(xMat)
    m,n=shape(xMat)
    returnMat=zeros((numIt,n))
    ws=zeros((n,1));wsTest=ws.copy();wsMax=ws.copy()
    for i in range(numIt):
        lowestError=inf;
        for j in range(n):
            for sign in [-1,1]:
                wsTest=ws.copy()
                wsTest[j]+=eps*sign
                yTest=xMat*wsTest
                rssE=rssError(yMat.A,yTest.A)
                if rssE<lowestError:
                    lowestError=rssE
                    wsMax=wsTest
        ws=wsMax.copy()
        returnMat[i,:]=ws.T
    ax4=plt.subplot(224)
    ax4.plot(returnMat)
    return returnMat



def show():  #最后在显示图像
    plt.show()




if __name__ == "__main__":
    os.chdir('C:/Users/think/Documents/学习/python程序/.vscode/AiLearning-master/AiLearning-master/data/8.Regression')

    xArr,yArr=loadDataSet('data.txt')
    ws=standRegres(xArr,yArr)
    yHat=lwlrTest(xArr,xArr,yArr,0.01)
    abX,abY=loadDataSet('abalone.txt')
    ridgeTest(abX,abY)
    stageWise(abX,abY,0.005,1000)




    show()
