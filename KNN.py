import numpy as np 
import operator
import os



def createDate():
    group=np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A',"A",'B','B']
    return group,labels

def classify0(inx,dataSet,labels,k):
    dataSetSize=dataSet.shape[0]
    diffMat=np.tile(inx,(dataSetSize,1))-dataSet
    sqdiffmat=diffMat**2
    diffsum=np.sum(sqdiffmat,1)
    distances=diffsum**0.5
    sortedDistances=distances.argsort()
    classCount={}
    for i in range(k):
        votelabel=labels[sortedDistances[i]]
        classCount[votelabel]=classCount.get(votelabel,0)+1
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr=open(current_path+filename)
    array=fr.readlines()
    length=len(array)
    returnMat=np.zeros((length,3))
    classLabelVector=[]
    index=0
    for line in array:
        linetext=line.strip()
        linefromarray=linetext.split('\t')
        returnMat[index,:]=linefromarray[0:3]
        classLabelVector.append(int(linefromarray[-1]))
        index+=1
    fr.close()
    return returnMat,classLabelVector

def autonorm(dataSet):
    minVal=dataSet.min(0)
    maxVal=dataSet.max(0)
    ranges=maxVal-minVal
    normalDataSet=np.zeros(np.shape(dataSet))
    m=dataSet.shape[0]
    normalDataSet=dataSet-np.tile(minVal,(m,1))
    normalDataSet=normalDataSet/np.tile(ranges,(m,1))
    return normalDataSet

def classifyPerson():
    resultlist=['not at all','in small doses','in large doses']
    personTats=float(input("percentage of time spent playing video games?"))
    ffMiles=float(input("frequent flier miles earned per year"))
    iceCream=float(input("liters of ice cream consumed per week"))
    datingDataMat,datingLabels=file2matrix('/learn.txt')
    normDatingDataMat=autonorm(datingDataMat)
    arr=np.array([ffMiles,personTats,iceCream])
    result=classify0(arr,normDatingDataMat,datingLabels,3)
    print(resultlist[result])

if __name__ == "__main__":
    
    print("当前路径 ->%s" %os.getcwd())
    current_path=os.path.dirname(__file__)
    classifyPerson()