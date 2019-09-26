from numpy import *


def binSplitDataSet(dataSet,feature,value):
    mat0=dataSet[nonzero(dataSet[:,feature] > value)[0],:]
    mat1=dataSet[nonzero(dataSet[:,feature] <= value)[0],:]
    return  mat0,mat1