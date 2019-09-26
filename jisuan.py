# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 16:58:18 2019

@author: think
"""
from numpy import *
import os
import pickle

def jisuan(jilu,list1):
    datad=[];daisudu=[];xingsudu=[]
    daistart=0;darend=0;xingstart=0;xingend=0
    jiasu=[];jiansu=[]
    for data in list1:
        datad.extend(jilu[data])
    datad.extend(array([[0.0,0.0,0.0,0.0]]))
    datad=array(datad)
    for j in range(len(datad)):  
        if datad[j,2]!=datad[max(j-1,0),2]:
            if datad[j,2]==1:
                #if j-daistart>5:
                daiend=j-1
                xingstart=j
                daisudu.extend(datad[daistart:daiend,0].tolist())
                daistart=max(daistart,j-180)
                    
            else:
                #if j-xingstart>5 and daiend>daistart and datad[min(j+5,len(datad)-1),0]<10:
                xingend=j-1
                dataa=datad[daistart:xingend,:]
                length=xingend-daistart
#                jiasu=datad[nonzero(datad[:,3]==1)[0],1]
#                jiansu=datad[nonzero(datad[:,3]==-1)[0],1] 
#                if length<25 or sum(dataa[:,0])<30 or len(jiasu)==0 or len(jiansu)==0:
#                    daistart=j
#                    continue
                xingsudu.extend(datad[xingstart:xingend,0].tolist())
                daistart=j
            
                    
    jiasu=datad[nonzero(datad[:,3]==1)[0],1]
    jiansu=datad[nonzero(datad[:,3]==-1)[0],1]    
    length=len(datad)
    gong=[]
    gong.append(mean(datad[:,0]))
    gong.append(mean(xingsudu))
    gong.append(max(datad[:,0]))
    gong.append(mean(jiasu))
    gong.append(mean(jiansu))
    gong.append(len(jiasu)/length)
    gong.append(len(jiansu)/length)
    gong.append(len(daisudu)/length)
    gong.append(std(datad[:,0]))
    gong.append(std(datad[:,1]))
    gong.append(sum(datad[:,0])/3.6)
    gong.append(length)
    return datad[:,0],gong


def jisuangong(data):
    datad=zeros((len(data),4))
    daisudu=[];xingsudu=[]
    daistart=0;darend=0;xingstart=0;xingend=0
    jiasu=[];jiansu=[]
    for i,var in enumerate(data):
        datad[i,0]=var
        if i!=0:
            datad[i,1]=(var-datad[i-1,0])/3.6
        if var>0:
            datad[i,2]=1
        if datad[i,1]>0.1:
            datad[i,3]=1
        elif datad[i,1]<-0.1:
            datad[i,3]=-1

    for j in range(len(datad)):  
        if datad[j,2]!=datad[max(j-1,0),2]:
            if datad[j,2]==1:
                #if j-daistart>5:
                daiend=j-1
                xingstart=j
                daisudu.extend(datad[daistart:daiend,0].tolist())
                daistart=max(daistart,j-180)
                    
            else:
                #if j-xingstart>5 and daiend>daistart and datad[min(j+5,len(datad)-1),0]<10:
                xingend=j-1
                dataa=datad[daistart:xingend,:]
                length=xingend-daistart
#                jiasu=datad[nonzero(datad[:,3]==1)[0],1]
#                jiansu=datad[nonzero(datad[:,3]==-1)[0],1] 
#                if length<25 or sum(dataa[:,0])<30 or len(jiasu)==0 or len(jiansu)==0:
#                    daistart=j
#                    continue
                xingsudu.extend(datad[xingstart:xingend,0].tolist())
                daistart=j
            
                    
    jiasu=datad[nonzero(datad[:,3]==1)[0],1]
    jiansu=datad[nonzero(datad[:,3]==-1)[0],1]    
    length=len(datad)
    gong=[]
    gong.append(mean(datad[:,0]))
    gong.append(mean(xingsudu))
    gong.append(max(datad[:,0]))
    gong.append(mean(jiasu))
    gong.append(mean(jiansu))
    gong.append(len(jiasu)/length)
    gong.append(len(jiansu)/length)
    gong.append(len(daisudu)/length)
    gong.append(std(datad[:,0]))
    gong.append(std(datad[:,1]))
    gong.append(sum(datad[:,0])/3.6)
    gong.append(length)
    return datad[:,0],gong

def plotplot(d,i=1):
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(d)
    plt.xlabel('Time:s')
    plt.ylabel('Velocity:km/h')
    
    plt.savefig('dd%i'%i,dpi=300)
    
if __name__=="__main__":
    os.chdir('C:/Users/think/Documents/学习/python程序/Ailearning')
    f0 = open('sc', 'rb')
    f1 = open('gongkuang','rb')
    f2=open('jilu','rb')
    f3=open('clu','rb')
# 将文件中的变量加载到当前工作区
    sc0,sc1,sc2 = pickle.load(f0)
    gongkuang=pickle.load(f1)
    jilu=pickle.load(f2)
    clu=pickle.load(f3)
    ddate1,gong1=jisuan(jilu,sc0)
    ddate2,gong2=jisuan(jilu,sc1)
    ddate3,gong3=jisuan(jilu,sc2)
    plotplot(ddate1,1)
    plotplot(ddate2,2)
    plotplot(ddate3,3)
    
    clu01=nonzero(clu==0)[0]
    clu02=nonzero(clu==1)[0]
    clu03=nonzero(clu==2)[0]
    
    date1,zong1=jisuan(jilu,clu01)
    date2,zong2=jisuan(jilu,clu02)
    date3,zong3=jisuan(jilu,clu03)
    
    a=list(range(len(jilu)))
    zongzong=jisuan(jilu,a)
    
    datee1,xuan1=jisuan(jilu,[1920,880])
    datee2,xuan2=jisuan(jilu,[2042,2296,2279])
    datee3,xuan3=jisuan(jilu,[1355,1900,272])
    
    datazong,xuanzong=jisuan(jilu,[1920,880,1355,1900,272,2042,2296,2279])
    plotplot(datazong,123)
    
#import xlrd
#shu3=[]
#data = xlrd.open_workbook('NEDC标准循环工况.xls') # 打开xls文件
#table = data.sheets()[0] # 打开第一张表
#nrows = table.nrows      # 获取表的行数
#for i in range(nrows): # 循环逐行打印
#    if i==0:
#        continue
#    shu3.extend([table.row_values(i)[1]])
#    
#biaozhun0=jisuangong(shu0)
#biaozhun1=jisuangong(shu1)
#biaozhun2=jisuangong(shu2)
#biaozhun3=jisuangong(shu3)

    
    
    
    
    
    
    
    
    