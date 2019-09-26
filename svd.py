from numpy import *
import os

#相似度计算函数
def cosSim(inA,inB):
    num=float(inA.T*inB)
    denom=linalg.norm(inA)*linalg.norm(inB)
    return 0.5+0.5*(num/denom)

def loadExData3():
    # 利用SVD提高推荐效果，菜肴矩阵
    return[[2, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],[0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0],[3, 3, 4, 0, 3, 0, 0, 2, 2, 0, 0],[5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0],[4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 5],[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4],[0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0],[0, 0, 0, 3, 0, 0, 0, 0, 4, 5, 0],[1, 1, 2, 1, 1, 2, 1, 0, 4, 5, 0]]


def standEst(dataMat,user,simMeas,item):
    n=shape(dataMat)[1]
    simTotal=0.0;ratSImTotal=0.0
    for j in range(n):
        userRating=dataMat[user,j]
        if userRating==0:continue
        overLap=nonzero(logical_and(dataMat[:,item].A>0,dataMat[:,j].A>0))[0]
        if len(overLap)==0:
            similarity=0
        else:
            similarity=simMeas(dataMat[overLap,item],dataMat[overLap,j])
        simTotal+=similarity
        ratSImTotal+=similarity*userRating
    if simTotal==0:
        return 0
    else:
        return ratSImTotal/simTotal
##降维来推荐系统
def svdEst(dataMat, user, simMeas, item):
    """svdEst(计算某用户未评分物品中，以对该物品和其他物品评分的用户的物品相似度，然后进行综合评分)

    Args:
        dataMat         训练数据集
        user            用户编号
        simMeas         相似度计算方法
        item            未评分的物品编号
    Returns:
        ratSimTotal/simTotal     评分（0～5之间的值）
    """
    # 物品数目
    n = shape(dataMat)[1]
    # 对数据集进行SVD分解
    simTotal = 0.0
    ratSimTotal = 0.0
    # 奇异值分解
    # 在SVD分解之后，我们只利用包含了90%能量值的奇异值，这些奇异值会以NumPy数组的形式得以保存
    U, Sigma, VT = linalg.svd(dataMat)

    # # 分析 Sigma 的长度取值
    # analyse_data(Sigma, 20)

    # 如果要进行矩阵运算，就必须要用这些奇异值构建出一个对角矩阵
    Sig4 = mat(eye(4) * Sigma[: 4])
    # 利用U矩阵将物品转换到低维空间中，构建转换后的物品(物品+4个主要的特征)
    xformedItems = dataMat.T * U[:, :4] * Sig4.I
    # 对于给定的用户，for循环在用户对应行的元素上进行遍历，
    # 这和standEst()函数中的for循环的目的一样，只不过这里的相似度计算时在低维空间下进行的。
    for j in range(n):
        userRating = dataMat[user, j]
        if userRating == 0 or j == item:
            continue
        # 相似度的计算方法也会作为一个参数传递给该函数
        similarity = simMeas(xformedItems[item, :].T, xformedItems[j, :].T)
        # 对相似度不断累加求和
        simTotal += similarity
        # 对相似度及对应评分值的乘积求和
        ratSimTotal += similarity * userRating
    if simTotal == 0:
        return 0
    else:
        # 计算估计评分
        return ratSimTotal/simTotal


def recommand(dataMat,user,N=3,simMeas=cosSim,estMethod=standEst):
    unratedItems=nonzero(dataMat[user,:].A==0)[1]
    if len(unratedItems)==0:
        return 'rate everything'
    itemScores=[]
    for item in unratedItems:
        estimatedScore=estMethod(dataMat,user,simMeas,item)
        itemScores.append((item,estimatedScore))
    return sorted(itemScores,key=lambda jj:jj[1],reverse=True)[:N]

def printMat(inMat,thresh=0.8):
    for i in range(32):
        for k in range(32):
            if float(inMat[i,k])>thresh:
                print(1,end='')
            else: print(0,end='')
        print ('')
##图像压缩
def imgCompress(numSV=3,thresh=0.8):
    myl=[]
    for line in open('0_5.txt').readlines():
        newRow=[]
        for i in range(32):
            newRow.append(int(line[i]))
        myl.append(newRow)
    myMat=mat(myl)
    print('**** original matrix *****')
    printMat(myMat,thresh)
    U,sigma,VT=linalg.svd(myMat)
    sigRecon=mat(zeros((numSV,numSV)))
    for k in range(numSV):
        sigRecon[k,k]=sigma[k]
    reconMat=U[:,:numSV]*sigRecon*VT[:numSV,:]
    print('************reconstructed matrix using %d singular values******')
    printMat(reconMat,thresh)



if __name__ == "__main__":
    os.chdir('C:/Users/think/Documents/学习/python程序/Ailearning/AiLearning-master/AiLearning-master/data/14.SVD')
    mydata=mat(loadExData3())
    food=recommand(mydata,2)
    print(food)
    print('*********************************')
    food2=recommand(mydata,2,estMethod=svdEst)
    print(food2)
    print('***********************************')
    imgCompress(2)