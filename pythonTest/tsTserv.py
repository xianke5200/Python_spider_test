from socket import *
from time import ctime

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print("wating for connection...")
    tcpCliSock, addr = tcpSerSock.accept()
    print("...connected from,", addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        send_data = "[%s] %s" %(ctime(), data.decode())
        tcpCliSock.send(send_data.encode())
    tcpCliSock.close()
tcpSerSock.close()