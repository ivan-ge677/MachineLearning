from numpy import log
from numpy import ones,array
import random
import os

##把数据集转变成元素不重复的列表形式
def createVocabList(dataSet):
    vocaSet=set([])
    for document in dataSet:
        vocaSet=vocaSet|set(document)
    return list(vocaSet)

##文本转变为向量
##根据文本库，将输入的文本转变成一个长度为文本库单词数量的列表
##列表对应值为0，说明输入的文本没出现文本库中的该文本
##列表对应值为1，说明输入的文本出现了文本库中的该文本
def setOfWord2Vec(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else:
            print("the word %s is not in my vocabulary!"%word)
    return returnVec

##根据文本库，将输入的文本转变成一个长度为文本库单词数量的列表
##列表对应值为i，说明输入的文本出现了文本库中的该文本共i次
##文档词袋模型
def bagOfWord2VecMN(vocabList,inputList):
    returnVec=[0]*len(vocabList)
    for word in inputList:
        if word in vocabList:
            returnVec[vocabList.index(word)]+=1
    return returnVec


##训练函数，把训练集文本的向量与训练集种类输入
##输出log(p(wi|c0))与log(p(wi|c1))与P(c1)

def trainNB(trainMatrix,trainCategory):
    numTrainDocs=len(trainMatrix)
    numWords=len(trainMatrix[0])
    pAbusive=sum(trainCategory)/float(numTrainDocs)
    p0Num=ones(numWords)
    p1Num=ones(numWords)
    p0Denom=2.0
    p1Denom=2.0
    # p0Num=zeros(numWords)
    # p1Num=zeros(numWords)
    # p0Denom=0.0
    # p1Denom=0.0
    # 这里的概率进行了修改就是为了下面使用自然对数，这样概率不会下溢出，而且比较大小的时候不会有任何损失
    for i in range(numTrainDocs):
        if trainCategory[i]==0:
            p0Num+=trainMatrix[i]
            p0Denom+=sum(trainMatrix[i])
        else:
            p1Num+=trainMatrix[i]
            p1Denom+=sum(trainMatrix[i])
    p1Vect=log(p1Num/p1Denom)  ####numpy的数组处理的时候用numpy的方法，所以log不能从math中导入
    p0Vect=log(p0Num/p0Denom)
    return p0Vect,p1Vect,pAbusive

##预测函数
def classifyNB(vec2Classify,p0Vect,p1Vect,pClass1):
    p1=sum(vec2Classify*p1Vect)+log(pClass1)
    p0=sum(vec2Classify*p0Vect)+log(1.0-pClass1)
    if p1>p0:
        return 1
    else:
        return 0

##文本分割函数
##把所有除字母数字之外的符号看做分隔符，把一段文本变成文本列表
def textParse(bigString):
    import re
    listOfTokens=re.split(r'\W+',bigString)
    return [tol.lower() for tol in listOfTokens if len(tol)>2]

##交叉验证
def spamTest():
    docList=[];classList=[];fullText=[]
    for i in range(1,26):
        fr1=open('email/spam/%d.txt'%i,encoding='gbk')
        wordList=textParse(fr1.read())
        
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        fr1.close()
        fr0=open('email/ham/%d.txt' % i,encoding='gbk')
        wordList=textParse(fr0.read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
        fr0.close()
    vocabList=createVocabList(docList)
    trainingSet=list(range(50));testSet=[] ##一共50个文本
    for i in range(10):
        randIndex=int(random.uniform(0,len(trainingSet)))  #随机抽取十个文本为测试，其它四十个为训练
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(setOfWord2Vec(vocabList,docList[docIndex]))
        #trainMat.append(bagOfWord2VecMN(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam=trainNB(array(trainMat),array(trainClasses))
    errorCount=0
    
    for docIndex in testSet:
        #testWord=bagOfWord2VecMN(vocabList,docList[docIndex])
        testWord=setOfWord2Vec(vocabList,docList[docIndex])
        #print(classList[docIndex])
        if classifyNB(array(testWord),p0V,p1V,pSpam)!=classList[docIndex]:  #测试时，预测结果不对则记录错误
            errorCount+=1
    print('the error rate is :',float(errorCount)/len(testSet))

if __name__ == "__main__":
    
    current_path=os.path.dirname(__file__)
    print("当前路径 ->%s" %os.getcwd())

    os.chdir('C:/Users/think/Documents/学习/python程序/.vscode/AiLearning-master/AiLearning-master/data/4.NaiveBayes')

    spamTest()


