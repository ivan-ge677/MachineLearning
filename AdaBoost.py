##元算法就是对其它算法进行组合的一种方式，AdaBoost就是一种最流行的元算法
##本示例先建立一个单层决策树，将AdaBoost算法应用在单层决策树之上。

from numpy import mat,array,ones,zeros,shape,inf,multiply,sign,exp
import os
from math import log
import matplotlib.pyplot as plt
#导入马疝病数据
def loadDataSet(filename):
    numfeat=len(open(filename).readline().split('\t'))   ##注意使用f=open()之后，先用一个f.realine,再用f.readlines就会从第二行还是读了
    dataMat=[];labelMat=[]
    f=open(filename)
    for line in f:
        lineArr=line.strip().split('\t')
        #data=[]
        # for i in range(numfeat-1):
        #     data.append(float(lineArr[i]))
        # dataMat.append(data)
        dataMat.append([float(val) for val in lineArr[0:numfeat-1]])
        labelMat.append(float(lineArr[-1]))
    f.close()
    return dataMat,labelMat

#单层决策树生成函数
def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):
    retArray=ones((shape(dataMatrix)[0],1))
    if threshIneq=='lt':
        retArray[dataMatrix[:,dimen]<=threshVal]=-1.0
    else:
        retArray[dataMatrix[:,dimen]>threshVal]=-1.0
    return retArray

def buildStump(dataArr,classLabels,D):
    dataMatrix=mat(dataArr);labelMatrix=mat(classLabels).T
    m,n=shape(dataMatrix)
    numSteps=10.0;bestStump={}
    bestClassEst=mat(zeros((m,1)));minError=inf
    for i in range(n):
        rangeMin=dataMatrix[:,i].min();rangeMax=dataMatrix[:,i].max()
        stepSize=(rangeMax-rangeMin)/numSteps
        for j in range(-1,int(numSteps)+1):  ##从-1开始的目的就是为了下面在计算threshVal时存在全符合和全不符合的情况
            for inequal in ['lt','gt']:
                threshVal=(rangeMin+float(j)*stepSize)
                predictedVals=stumpClassify(dataMatrix,i,threshVal,inequal)
                errArr=mat(ones((m,1)))
                errArr[predictedVals==labelMatrix]=0
                weightedError=D.T*errArr #矩阵计算，变成一个数值
                if weightedError<minError:
                    minError=weightedError
                    bestClassEst=predictedVals.copy()
                    ##bestStunp存放着所有跟最优决策树有关的信息
                    bestStump['dim']=i
                    bestStump['thresh']=threshVal
                    bestStump['ineq']=inequal
    return bestStump,minError,bestClassEst

##基于单层决策树的AdaBoost训练过程
def adaBoostTrainDS(dataArr,classLabels,numIt=40):
    weakClassArr=[]
    m=shape(dataArr)[0]
    D=mat(ones((m,1))/m)
    aggClassEst=mat(zeros((m,1)))
    for i in range(numIt):
        bestStump,error,classEst=buildStump(dataArr,classLabels,D)
        alpha=float(0.5*log((1.0-error)/max(error,1e-16)))##这里使用max是为了防止下溢出
        bestStump['alpha']=alpha ##在bestStump中加入alpha信息
        weakClassArr.append(bestStump)
        expon=multiply(-1*alpha*mat(classLabels).T,classEst)  ##判断是够判断正确，正确时取-alpha，错误时取alpha
        D=multiply(D,exp(expon))
        D=D/D.sum()  ##为了保证D的总和为1
        aggClassEst+=alpha*classEst  ##最终决策就是各个决策树的预测结果加上alpha系数之后的结果
        aggErrors=multiply(sign(aggClassEst)!=mat(classLabels).T,ones((m,1)))   #计算最终决策是否正确
        errorRate=aggErrors.sum()/m
        if errorRate==0.0:   #当错误率为0时，中断迭代
            break
    print(' training total error:',errorRate)
    return weakClassArr,aggClassEst

##基于AdaBoost的分类
def adaClassify(dataToclass,classifierArr):
    dataMatrix=mat(dataToclass)
    m=shape(dataMatrix)[0]
    aggClassEst=mat(zeros((m,1)))
    for i in range(len(classifierArr)):
        classEst=stumpClassify(dataMatrix,classifierArr[i]['dim'],classifierArr[i]['thresh'],classifierArr[i]['ineq'])
        aggClassEst+=classifierArr[i]['alpha']*classEst
    return sign(aggClassEst)


##额外模块
##非均衡问题
##Roc曲线的绘制与AUC计算函数
def plotROC(predStrengths,classLabels):
    cur=(1.0,1.0)  ##光标位置
    ysum=0.0  #计算AUC的值
    numPosClas=sum(array(classLabels)==1.0) #通过数组过滤的方式计算正例的数目
    yStep=1/float(numPosClas)
    xStep=1/float(len(classLabels)-numPosClas)
    sortedIndicies=predStrengths.argsort() ##返回一个数组array，从小到大排序后的索引
    fig=plt.figure()
    fig.clf()
    ax=plt.subplot(111)
    for index in sortedIndicies.tolist()[0]: #tolist转化为列表用于迭代循环
        if classLabels[index]==1.0:
            delX=0.0;delY=yStep
        else:
            delX=xStep;delY=0.0
            ysum+=cur[1]*xStep
        ax.plot([cur[0],cur[0]-delX],[cur[1],cur[1]-delY],c='b')
        cur=(cur[0]-delX,cur[1]-delY)
    ax.plot([0,1],[0,1],'b--')
    plt.xlabel('False Positive Rate');plt.ylabel('True Position Rate')
    plt.title('ROC curve for AdaBoost Horse Colic Detection System')
    print('the Area Under the Curve is :',ysum)
    plt.show()

    


if __name__ == "__main__":
    os.chdir('C:/Users/think/Documents/学习/python程序/.vscode/AiLearning-master/AiLearning-master/data/7.AdaBoost')
    dataArr,labelArr=loadDataSet('horseColicTraining2.txt')
    classifierArr,aggclassEst=adaBoostTrainDS(dataArr,labelArr,10)
    testArr,testlabelArr=loadDataSet('horseColicTest2.txt')
    print(shape(testArr))
    prediction10=adaClassify(testArr,classifierArr)
    errorArr=mat(ones((67,1)))
    errorsum=errorArr[prediction10!=mat(testlabelArr).T].sum()
    print('testing error :',errorsum/67)
    print('------------------------------------------------------------------')
    plotROC(aggclassEst.T,labelArr)