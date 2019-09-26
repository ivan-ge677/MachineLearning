import socket
import os
import hashlib

server=socket.socket()
server.bind(('localhost',9999))
server.listen()

while True:
    conn,addr=server.accept()
    print("new conn",addr)

    while True:
        data=conn.recv(1024)  #接收客户端的命令
        if not data:
            print("断开")  #如果这个时候断开的话就重新连接
            break
        cmd,filename=data.decode().split()
        print(filename)
        if os.path.isfile(filename): #判断文件上是否存在
            f=open(filename,'rb')
            m=hashlib.md5()
            file_size=os.stat(filename).st_size  #获取文件大小
            conn.send(str(file_size).encode())  #发送文件大小
            conn.recv(1024) #等待确认
            for iine in f:  #利用生成器读文件
                m.updata(line)
                conn.send(line)
            print('file md5',m.hexdigest())
            
            f.close()
            conn.send(m.hexdigest().decode()) #发送文件的md5码
        else:
            print("找不到文件")
        print('send down') 
server.close()



