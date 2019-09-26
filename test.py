from numpy import *


a=mat([[1,2,3],[4,5,6],[7,8,9]])
b=mean(a,axis=0)
print(b)

a1=array([[1,2,3],[4,5,6],[7,8,9]])
b1=mean(a1,axis=0)
print(b1)

x=arange(5)
print(logical_and(x>1,x<4))