# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 16:07:55 2019

@author: think
"""

# 载入模块
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
 
# 创建 3D 图形对象
fig = plt.figure()
ax = Axes3D(fig)
 
# 生成数据并绘图
x = [0, 1, 2, 3, 4, 5, 6]
for i in x:
  y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  z = abs(np.random.normal(1, 10, 10))
  ax.bar(y, z, i, zdir='y', color=['r', 'g', 'b', 'y'])
plt.show()


sort=sorted(clu0,key=lambda k:k[:,1])
sortindex=clu0[:,1].argsort()

laji=[]
for i in range(len(clu0)):
    la=[i,clu0[i,0],clu0[i,1]]
    laji.append(la)
    
laji=array(laji)  
sort=sorted(laji,key=lambda k:k[2])
sort=array(sort)

v1=[]
for i in clu01:
    v1.extend(jilu[i][:,0])
v2=[]
for i in clu02:
    v2.extend(jilu[i][:,0])
v3=[]
for i in clu03:
    v3.extend(jilu[i][:,0])
    
savetxt("V11.txt",array(v1))
savetxt("V12.txt",array(v2))
savetxt("V13.txt",array(v3))
    
    
    