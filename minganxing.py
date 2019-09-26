# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 19:02:03 2019

@author: think
"""
from numpy import *
import os

def distEclud(vecA,vecB):
    return sqrt(sum(pow(array((vecA-vecB).tolist()[0]),2)))

def minganxing(center,dataMat,testdata,redg,distMeas=distEclud):
    topfea=4
    meanVals=mean(dataMat,axis=0) #求每列平均值
    sigma=sqrt(sum(power((dataMat-meanVals),2),axis=0)/(len(dataMat)-1))
    meanRemoved=(testdata-meanVals)/sigma #正态分布标准化
    
    lowDDataMat=meanRemoved*redg  #数据集乘特征向量得到降维的结果，行数不变，列数变少
    for i in range(len(lowDDataMat)):
        sse=inf;cla=-1;err=0
        for c in range(len(center)):
            distJI = distMeas(array(center)[c,:],lowDDataMat[i,:]) 
            if distJI<sse:
                sse=distJI
                cla=c
        if cla!=2:
            err+=1
    return err/len(testdata)



def chuli(da,clu):
    for i in clu:
        da[i][1:4]*=1

    return da
        
        
    
if __name__=="__main__":
    data111=chuli(gongkuang,clu02)
    errr=minganxing(cen0,gongkuang[:,1:11],data111[1:100,1:11],redg)

            
            