import itchat

# itchat.auto_login()
# friends = itchat.get_friends()
# print(friends)
# itchat.send('hello', toUserName='filehelper')

from pyqrcode import QRCode
import sys

url = QRCode('https://blog.csdn.net/sinat_33323544')
# url.png('xianke5200.png')#保存图片到本地
url.show()

# url.svg(sys.stdout, scale=1)
# url.svg('uca.svg', scale=4)
# number = QRCode(123456789012345)
# number.png('big-number.png')