from numpy import *
import os

def loadDataSet(fileName):
    fr=open(fileName)
    dataArr=[]
    for line in fr.readlines():
        data=line.strip().split('\t')
        stringArr=[]
        stringArr=[float(var) for var in data]
        dataArr.append(stringArr)
    return mat(list(dataArr))


def pca(dataMat,topfea=999):
    meanVals=mean(dataMat,axis=0) #求每列平均值
    meanRemoved=dataMat-meanVals #去平均值
    covMat=cov(meanRemoved,rowvar=0) #求协方差矩阵（对称非负定矩阵）
    eigVals,eigVects=linalg.eig(mat(covMat)) #求协方差矩阵的特征值与特征向量
    eigValInd=argsort(eigVals) #返回特征值从小到大的索引值
    eigValInd=eigValInd[:-(topfea+1):-1] #倒着取topfea个值
    redEigVects=eigVects[:,eigValInd] #利用索引去除最大的topfea个特征值对应的特征向量
    lowDDataMat=meanRemoved*redEigVects  #数据集乘特征向量得到降维的结果，行数不变，列数变少
    reconMat=(lowDDataMat*redEigVects.T)+meanVals  #降维结果✖特征向量的转置，再加上平均值得到重构矩阵
    return lowDDataMat,reconMat


if __name__ == "__main__":
    os.chdir('C:/Users/think/Documents/学习/python程序/Ailearning/AiLearning-master/AiLearning-master/data/13.PCA')
    mydata=loadDataSet('testSet.txt')
    lowdata,reconmat=pca(mydata,1)
    
