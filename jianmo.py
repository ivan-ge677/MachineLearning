# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:36:59 2019

@author: ivan
"""
from numpy import *
#from math import sqrt
import os
from sklearn import metrics
from scipy.stats import pearsonr
from sklearn import cluster
import pickle

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
    sigma=sqrt(sum(power((dataMat-meanVals),2),axis=0)/(len(dataMat)-1))
    meanRemoved=(dataMat-meanVals)/sigma #正态分布标准化
    covMat=cov(meanRemoved,rowvar=0) #求协方差矩阵（对称非负定矩阵）
    eigVals,eigVects=linalg.eig(mat(covMat)) #求协方差矩阵的特征值与特征向量
    eigValInd=argsort(eigVals) #返回特征值从小到大的索引值
    sorteigVals=sorted(eigVals,reverse=True)
    eigValInd=eigValInd[:-(topfea+1):-1] #倒着取topfea个值
    redEigVects=eigVects[:,eigValInd] #利用索引去除最大的topfea个特征值对应的特征向量
    print('原特征与新特征的相关性矩阵：', redEigVects)
    lowDDataMat=meanRemoved*redEigVects  #数据集乘特征向量得到降维的结果，行数不变，列数变少
    reconMat=(lowDDataMat*redEigVects.T)+meanVals  #降维结果✖特征向量的转置，再加上平均值得到重构矩阵
    return sorteigVals,lowDDataMat,reconMat,redEigVects



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

def randdCent(dataSet,k):
    centroids=[]
    r=random.rand(k,1)*len(dataSet)
    for i in range(k):
        centroids.append( dataSet[int(floor(r[i]))].tolist()[0])
    centroids=mat(centroids)
    return centroids


##普通K均值算法

def kMeans(dataSet, k, distMeas=distEclud, createCent=randdCent):
    m = shape(dataSet)[0]    # 行数，即数据个数
    clusterAssment = mat(zeros((m, 2)))    # 创建一个与 dataSet 行数一样，但是有两列的矩阵，用来保存簇分配结果
    centroids = createCent(dataSet, k)    # 创建质心，随机k个质心
    clusterChanged = True
    iter0=0
    while clusterChanged:
        clusterChanged = True
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
        iter0+=1
        if iter0==500:
            break
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
    return array(cenList),clusterAssment

#根据皮尔逊系数，选出每一簇的代表短行程
def goujian1(dataMat,cluster,k,n=20):
    center=[]
    for i in range(k):
        mean0=mean(dataMat[nonzero(cluster==i)[0],:],axis=0)
        center.append(mean0)
    corr=[]
    for i,val in enumerate(cluster):
        corr.append([i,pearsonr(array(dataMat)[i],array(center)[int(val)][0])[0],int(val)])
    sortcorr=sorted(corr,key=lambda k:k[1],reverse=False)
    sortcorr=array(sortcorr)
    sortcorr0=sortcorr[nonzero(sortcorr[:,2]==0)[0][:n],:]
    sortcorr1=sortcorr[nonzero(sortcorr[:,2]==1)[0][:n],:]
    sortcorr2=sortcorr[nonzero(sortcorr[:,2]==2)[0][:n],:]
    print('第一簇的前n个序号',sortcorr0)
    print('第二簇的前n个序号',sortcorr1)
    print('第三簇的前n个序号',sortcorr2)
    return sortcorr0[:,0],sortcorr1[:,0],sortcorr2[:,0]


def goujian(dataMat,cluster,k,center,n=20):
    
    corr=[]
    for i,val in enumerate(cluster):
        corr.append([i,pearsonr(array(dataMat)[i],array(center)[int(val)])[0],int(val)])
    sortcorr=sorted(corr,key=lambda k:k[1],reverse=True)
    sortcorr=array(sortcorr)
    sortcorr0=sortcorr[nonzero(sortcorr[:,2]==0)[0][:n],:]
    sortcorr1=sortcorr[nonzero(sortcorr[:,2]==1)[0][:n],:]
    sortcorr2=sortcorr[nonzero(sortcorr[:,2]==2)[0][:n],:]
    print('第一簇的前n个序号',sortcorr0)
    print('第二簇的前n个序号',sortcorr1)
    print('第三簇的前n个序号',sortcorr2)
    return sortcorr0[:,0],sortcorr1[:,0],sortcorr2[:,0]
    
def baocun(filename,var):
    import pickle
# 以二进制写模式打开目标文件
    f = open(filename, 'wb')
# 将变量存储到目标文件中区
    pickle.dump(var, f)
# 关闭文件
    f.close()
# 删除变量
    del var       
        



if __name__ == "__main__":

    #os.chdir('C:/Users/think/Documents/学习/python程序/Ailearning/AiLearning-master/AiLearning-master/data/13.PCA')
    #mydata=loadDataSet('testSet.txt')
    f0 = open('gongkuang', 'rb')
# 将文件中的变量加载到当前工作区
    gongkuang = pickle.load(f0)
    sorteigVals,lowdata,reconmat,redg=pca(gongkuang[:,1:],4)
    print('*******************PCA完成计算**************************')
    print('特征值列表为:',sorteigVals)
    #os.chdir('C:/Users/think/Documents/学习/python程序/Ailearning/AiLearning-master/AiLearning-master/data/10.KMeans')
    #lowdata=loadDataSet('testSet2.txt')
    k=3
    print('kmeans开始')
    kmeans = cluster.KMeans(n_clusters=k,max_iter=1000)
    kmeans.fit(lowdata)
    clu=kmeans.labels_
    print('****')
    cen0,clu0=kMeans(lowdata,k)
    print('kmeans结束')
    score0=metrics.calinski_harabaz_score(lowdata, clu0[:,0])
    score00=metrics.silhouette_score(lowdata, clu0[:,0], metric='euclidean')
    #score00=davies_bouldin_score(lowdata, clu0[:,0])
    #print('Calinski-Harabaz 指数:',score0,'Davies-Bouldin Index指数：',score00,'簇间距离和',sum(clu0[:,1]))
    print('Calinski-Harabaz 指数:',score0,'簇间距离和',sum(clu0[:,1]),'silhouette:',score00)
    #print('二分法kmeans开始')
    #cen1,clu1=biKmeans(lowdata,k)
    #print('二分法kmeans结束')
    #score1=metrics.calinski_harabaz_score(lowdata, clu1[:,0])
    #score11=metrics.davies_bouldin_score(lowdata, clu0[:,0])
    #print('Calinski-Harabaz 指数:',score1,'Davies-Bouldin Index指数：',score11,'簇间距离和',sum(clu1[:,1])) 
    #print('Calinski-Harabaz 指数:',score1,'簇间距离和',sum(clu1[:,1])) 
    #print('各簇中心点的位置',cen1)
    baocun('clu',clu0[:,0])
    sc0,sc1,sc2=goujian(gongkuang[:,1:11],clu0[:,0],3,center,10)
    baocun('sc',[sc0,sc1,sc2])
#    
    
    
    
    
    
    
    




