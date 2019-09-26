import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import os
import pandas as pd

def plotPic(filename,ch,standard,cedian):
    data=[]
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14) 
    font1 = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=8) 

    with open(filename) as f:
        for line in f.readlines():
            li=line.strip().split()
            data.append([float(var) for var in li])  
    fig=plt.figure(1)
    fig.clf()
    ax=plt.subplot(111)
    dataArr=np.array(data)
    xdata=list(range(1,len(data)+1))
    ydata=list(np.abs(dataArr[:,4]))
    ydatan=list(np.abs(dataArr[:,3]))
    ydatarms=list(dataArr[:,6])
    ax.bar(xdata,ydata)
    ax.bar(xdata,ydatan,bottom=0)
    plt.title('测点%s  曲线加速度统计图'%cedian,fontproperties=font)
    plt.xlabel('样本编号',fontproperties=font)
    plt.ylabel('加速度m/s^2',fontproperties=font)
    ydata.extend(ydatan)
    means=np.mean(ydata)
    vars=np.std(ydata)
    guji=means+vars*3
    ax.hlines(y=guji,xmin=0,xmax=len(data)+1,colors="r",linestyles="--")
    plt.text(len(data)-10,guji*1.05,'最大估计值： %s'%round(guji,3),FontProperties=font1)
    ax.hlines(y=standard,xmin=0,xmax=len(data)+1,colors="b",linestyles="-.")
    plt.text(len(data)-5,standard*0.9,'限度：%s'%standard,FontProperties=font1)
    plt.savefig(r'ch%s.png'%ch,dpi=100,bbox_inches='tight')
    fig2=plt.figure(2)
    fig2.clf()
    ax2=plt.subplot(111)
    ax2.bar(xdata,ydatarms)
    plt.title('测点%s  曲线加速度RMS统计图'%cedian,fontproperties=font)
    plt.xlabel('样本编号',fontproperties=font)
    plt.ylabel('加速度m/s^2',fontproperties=font)
    rmsmeans=np.mean(ydatarms)
    ax2.hlines(y=rmsmeans,xmin=0,xmax=len(data)+1,colors='r',linestyles='--')
    plt.text(len(data)-5,rmsmeans*1.05,'RMS平均值： %s'%round(rmsmeans,3),FontProperties=font1)


    plt.savefig(r'RMS_ch%s.png'%ch,dpi=100,bbox_inches='tight')
    return dataArr[:,[4,3,6]]

def saveExcel(data,speed):
    data=np.array(data)
    goujiaheng=data[0:4]
    chetiheng=data[4:8]
    goujiahengpd=pd.DataFrame({"B1Y-MAX":goujiaheng[:,0],
    "B1Y-MIN":goujiaheng[0,:,1],
    "B2Y-MAX":goujiaheng[1,:,0],
    "B2Y-MIN":goujiaheng[1,:,1],
    "B3Y-MAX":goujiaheng[2,:,0],
    "B3Y-MIN":goujiaheng[2,:,1],
    "B4Y-MAX":goujiaheng[3,:,0],
    "B4Y-MIN":goujiaheng[3,:,1]},
    columns=['B1Y-MAX','B1Y-MIN','B2Y-MAX','B2Y-MIN','B3Y-MAX','B3Y-MIN','B4Y-MAX','B4Y-MIN'])
    chetihengpd=pd.DataFrame({"C7Y-MAX":chetiheng[0,:,0],
    "C7Y-MIN":chetiheng[0,:,1],
    "C8Y-MAX":chetiheng[1,:,0],
    "C8Y-MIN":chetiheng[1,:,1],
    "C9Y-MAX":chetiheng[2,:,0],
    "C9Y-MIN":chetiheng[2,:,1],
    "C10Y-MAX":chetiheng[3,:,0],
    "C10Y-MIN":chetiheng[3,:,1]},
    columns=['C7Y-MAX','C7Y-MIN','C8Y-MAX','C8Y-MIN','C9Y-MAX','C9Y-MIN','C10Y-MAX','C10Y-MIN'])     

    goujiahengrms=pd.DataFrame({"B1Y":goujiaheng[0,:,2],
    "B2Y":goujiaheng[1,:,2],
    "B3Y":goujiaheng[2,:,2],
    "B4Y":goujiaheng[2,:,2]},
    columns=['B1Y','B2Y','B3Y','B4Y'])

    chetihengrms=pd.DataFrame({"C7Y":chetiheng[0,:,2],
    "C8Y":chetiheng[1,:,2],
    "C9Y":chetiheng[2,:,2],
    "C10Y":chetiheng[2,:,2]},
    columns=['C7Y','C8Y','C9Y','C10Y'])

    goujiahengpd.index = goujiahengpd.index + 1
    chetihengpd.index = chetihengpd.index + 1

    goujiahengrms.index = goujiahengrms.index + 1
    chetihengrms.index = chetihengrms.index + 1


    writer=pd.ExcelWriter('speed%s.xlsx'%speed)	
    goujiahengpd.to_excel(writer,'goujiaheng')
    chetihengpd.to_excel(writer,'chetiheng')

    goujiahengrms.to_excel(writer,'goujiahengrms')
    chetihengrms.to_excel(writer,'chetihengrms')


    writer.save()
    writer.close()






if __name__ == "__main__":
    os.chdir('C:/Users/think/Desktop/xianggangaw0/0')
    ft=[1,2]
    ch=[22,24,26,28,14,16,18,20]
    cedian=['B1Y','B2Y','B3Y','B4Y','C7Y','C8Y','C9Y','C10Y']
    standard=[10.84,10.84,10.84,10.84,2.8,2.8,2.8,2.8]
    dataArr=[]
    for i in ft:
        for j in range(4):
            chh=(i-1)*4+j
            fileName='0611-2_uic518_ft%s_ch%s_rst.txt'%(i,ch[chh])
            dataArr.append(plotPic(fileName,ch[chh],standard[chh],cedian[chh]))
    saveExcel(dataArr,'曲线')