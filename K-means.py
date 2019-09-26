from numpy import *
from math import sqrt
import os


def loadDataSet(fileName):
    dataMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        curLine=line.strip().split('\t')
        fltLine=list(map(float,curLine))
        dataMat.append(fltLine)
    return dataMat



def distEclud(vecA,vecB):
    return sqrt(sum(pow(vecA-vecB,2)))

def randCent(dataSet,k):
    n=shape(dataSet)[1]
    centroids=mat(zeros((k,n)))
    for j in range(n):
        minJ=min(dataSet[:,j])
        rangeJ=float(max(dataSet[:,j])-minJ)
        centroids[:,j]=minJ+rangeJ*random.rand(k,1)
    return centroids


##普通K均值算法

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]    # 行数，即数据个数
    clusterAssment = mat(zeros((m, 2)))    # 创建一个与 dataSet 行数一样，但是有两列的矩阵，用来保存簇分配结果
    centroids = createCent(dataSet, k)    # 创建质心，随机k个质心
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):    # 循环每一个数据点并分配到最近的质心中去
            minDist = inf; minIndex = -1
            for j in range(k):
                distJI = distMeas(array(centroids)[j,:],array(dataSet)[i,:])    # 计算数据点到质心的距离
                if distJI < minDist:    # 如果距离比 minDist（最小距离）还小，更新 minDist（最小距离）和最小质心的 index（索引）
                    minDist = distJI; minIndex = j
            if clusterAssment[i, 0] != minIndex:    # 簇分配结果改变
                clusterChanged = True    # 簇改变
            clusterAssment[i, :] = minIndex,minDist**2    # 更新簇分配结果为最小质心的 index（索引），minDist（最小距离）的平方
        for cent in range(k): # 更新质心
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A==cent)[0]] # 获取该簇中的所有点
            centroids[cent,:] = mean(ptsInClust, axis=0) # 将质心修改为簇中所有点的平均值，mean 就是求平均值的
    return centroids, clusterAssment

##二分K均值算法
def biKmeans(dataSet,k,distMeas=distEclud):
    m=shape(dataSet)[0]
    clusterAssment=mat(zeros((m,2)))
    centroid=mean(dataSet,axis=0).tolist()
    centroid0=centroid[0]
    cenList=[centroid0]
    for j in range(m):
        clusterAssment[j,1]=distMeas(array(centroid0),array(dataSet)[j,:])**2
    while (len(cenList)<k):
        lowestSSE=inf
        for i in range(len(cenList)):
            ptsInCurrCluster=dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]
            centroidMat,splitClustAss=kMeans(ptsInCurrCluster,2,distMeas)
            sseSplit=sum(splitClustAss[:,1])
            sseNotSplit=sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
            if (sseSplit+sseNotSplit)<lowestSSE:
                bestCentToSplit=i
                bestNewCents=array(centroidMat)
                bestClustAss=splitClustAss.copy()
                lowestSSE=sseSplit+sseNotSplit
        bestClustAss[nonzero(bestClustAss[:,0].A==1)[0],0]=len(cenList)
        bestClustAss[nonzero(bestClustAss[:,0].A==0)[0],0]=bestCentToSplit
        cenList[bestCentToSplit]=bestNewCents[0,:]
        cenList.append(bestNewCents[1,:])
        clusterAssment[nonzero(clusterAssment[:,0].A==bestCentToSplit)[0],:]=bestClustAss
    return cenList,clusterAssment



if __name__ == "__main__":
    os.chdir('C:/Users/think/Documents/学习/python程序/Ailearning/AiLearning-master/AiLearning-master/data/10.KMeans')
    datMat=mat(loadDataSet('testSet2.txt'))
    cen,clu=biKmeans(datMat,3)
    print(cen)

    


