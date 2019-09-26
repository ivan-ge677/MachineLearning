

def createData():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]



def createC1(dataSet):
    C1=[]
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset,C1))  ##python3中的map返回一个迭代对象，如果这个迭代对象在第二层循环里，那么迭代一次就不会再迭代第二次了


def scanD(D,Ck,minSupport):
    ssCnt={}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):  ##can是不是tid的子集
                if can not in ssCnt:
                    ssCnt[can]=1
                else:
                    ssCnt[can]+=1
    numItems=float(len(D))
    retList=[]
    supportData={}
    for key in ssCnt:
        support=ssCnt[key]/numItems
        if support>=minSupport:
            retList.insert(0,key)
        supportData[key]=support
    return retList,supportData


def aprioriGen(LK,k):
    retList=[]
    lenLK=len(LK)
    for i in range(lenLK):
        for j in range(i+1,lenLK):
            L1=list(LK[i])[:k-2]  ##set转化为list会自动排序
            L2=list(LK[j])[:k-2]
            if L1==L2:
                retList.append(LK[i]|LK[j])
    return retList

##频繁项集
def apriori(dataSet,minSupport=0.5):
    C1=createC1(dataSet)
    D=list(map(set,dataSet))
    L1,supportData=scanD(D,C1,minSupport)
    L=[L1]
    k=2
    while(len(L[k-2])>0):
        Ck=aprioriGen(L[k-2],k)
        Lk,supK=scanD(D,Ck,minSupport)
        supportData.update(supK)  ##字典的多项更新
        L.append(Lk)
        k+=1
    return L,supportData

##从频繁项集中挖掘关联规则
def generateRules(L,supportData,minConf=0.7):
    bigRuleList=[]
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1=[frozenset([item]) for item in freqSet]
            if i>1:
                #calcConf(freqSet,H1,supportData,bigRuleList,minConf) 考虑下面的疑问的话应该加上这句
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)
    return bigRuleList

##计算是够大于可信度
def calcConf(freqSet,H,supportData,br1,minConf=0.7):
    prunedH=[]
    for conseq in H:
        conf=supportData[freqSet]/supportData[freqSet-conseq]
        if conf>=minConf:
            print(freqSet-conseq,'--->',conseq,'conf',conf)
            br1.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    return prunedH
##频繁项集的元素数目超过2，则会考虑对其合并（这个地方有疑问）
#（如果频繁项集是123，那么这个程序不考虑12->3 , 13->2的情况，只考虑1->23）
def rulesFromConseq(freqSet,H,supportData,br1,minConf=0.7):
    m=len(H[0])
    if(len(freqSet)>(m+1)):
        Hmp1=aprioriGen(H,m+1)
        Hmp1=calcConf(freqSet,Hmp1,supportData,br1,minConf)
        if (len(Hmp1)>1):
            rulesFromConseq(freqSet,Hmp1,supportData,br1,minConf)




if __name__ == "__main__":
    dataSet=createData()
    L,supportData=apriori(dataSet,0.5)
    rules=generateRules(L,supportData,0.5)

