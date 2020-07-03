from socketserver import (TCPServer as TCP,
    StreamRequestHandler as SRH)
from time import ctime

HOST = ''
PORT = 21567
ADDR = (HOST, PORT)

class MyRequestHandler(SRH):
    def handle(self):
        print("...connect from:", self.client_address)
        send_data = "[%s] %s" %(ctime(), self.rfile.readline().decode())
        self.wfile.write(send_data.encode())

tcpServ = TCP(ADDR, MyRequestHandler)
print("waiting for connection...")
tcpServ.serve_forever()