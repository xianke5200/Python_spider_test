from socket import *
from time import ctime

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

udpSerSock = socket(AF_INET, SOCK_DGRAM)
udpSerSock.bind(ADDR)

while True:
    print("waiting for message...")
    data, addr = udpSerSock.recvfrom(BUFSIZ)
    data_send = "[%s] %s" %(ctime(), data.decode())
    udpSerSock.sendto(data_send.encode(), addr)
    print("...received from and return to:", addr)

udpSerSock.close()