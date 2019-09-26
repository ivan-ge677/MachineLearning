import socket
import os
import hashlib
client = socket.socket()

client.connect(("localhost",9999))

while True:
    cmd=input(">>:").strip()
    if len(cmd)==0:
        continue  #如果没有输出，就必须重新输入
    if cmd.startwith("get"):
        client.send(cmd.encode())
        server_response=client.recv(1024)
        print("response:",server_response)
        slient.send(b'ok')  #受到长度之后给一个回应，防止黏包
        file_total.size=int(server_response.decode())
        received_size=0
        filename=cmd.split()[1]
        f=open(filename,'wb')  #直接读字节
        m=hashlib.md5()

        while received_size<file_total_size:
            if file_total_size-received_size>1024:   #防止黏包，最后一次发送文件内容的时候，定量接收。
                size=1024
            else:
                size=file_total_size-received_size
            data=client.recv(size)
            received_size+=len(data)
            m.updata(data)
            f.write(data)
           # print(file_total_size,' ',received_size)
        else:
            print("file recv down")
            new_file_md5=m.hexdigest()
            f.close()
            server_file_md5=client.recv(1024)
            print("server file md5:",server_file_md5.decode())
            print("client file md5:",new_file_md5)

client.close()