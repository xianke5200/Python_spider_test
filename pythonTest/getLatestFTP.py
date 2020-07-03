

import ftplib
import os
import socket

HOST = '192.168.1.153'
DIRN = 'pub/mozilla.org/webtools'
FILE = 'bugzilla-LATEST.tar.gz'

class myFtp():
    def __init__(self):
        self.ftp_client = ftplib.FTP()

    def ftp_login(self, host_ip, username, password):
        try:
            self.ftp_client.connect(host_ip, timeout=1000)
        except:
            print("network connect timeout")
            return 1001

        print("ftp connect success")
        try:
            if(username and password):
                print("username and password not null")
                self.ftp_client.login(user=username, passwd=password)
            else:
                print("username or password null")
                self.ftp_client.login()
        except:
            print("username and password error")
            return 1002
        return 1000

    def execute_some_cmd(self):
        command_result = self.ftp_client.sendcmd('pwd')
        print("command result: %s" % command_result)
        command_result = self.ftp_client.sendcmd('ls')
        print("command result: %s" % command_result)
        command_result = self.ftp_client.pwd()
        print("command result: %s" % command_result)
        command_result = self.ftp_client.cwd('\share')
        print("command result: %s" % command_result)
        command_result = self.ftp_client.storbinary('stor ftp_client.py', open('ftp_client.py', 'rb'))
        print("command result: %s" % command_result)
        command_result = self.ftp_client.retrbinary('retr ftp_client.py', open('ftp_client.py', 'wb').write())
        print("command result: %s" % command_result)

    def ftp_logout(self):
        print("ftp connect timeout")
        self.ftp_client.close()

def main():
    try:
        f = ftplib.FTP(HOST)
    except (socket.error, socket.gaierror) as e:
        print('ERROR: cannot reach"%s"' %(HOST))
        return
    print('***Connected to host "%s"' %(HOST))

    try:
        f.login()
    except ftplib.error_perm:
        print('ERROR: cannot login  anonymiusly')
        f.quit()
        return
    print("*** Logged in as 'anonymous'")

    try:
        f.cwd(DIRN)
    except ftplib.error_perm:
        print('ERROR: cannot CD to "%s"' %(DIRN))
        f.quit()
        return
    print("*** Changed to '%s' folder" %(DIRN))

    try:
        f.retrbinary('RETR %s' %(FILE), open(FILE, 'wb').write())
    except ftplib.error_perm:
        print('ERROR: cannot read file "%s"' %(FILE))
        os.unlink(FILE)
    else:
        print("***Downloaded [%s] to CWD" %(FILE))
    f.quit()
    return

if __name__ == '__main__':
    #main()
    host_ip = HOST
    username = 'chenlue'
    password = 'chenlue'
    myftp = myFtp()
    if myftp.ftp_login(host_ip, username, password) == 1000:
        myftp.execute_some_cmd()
        myftp.ftp_logout()