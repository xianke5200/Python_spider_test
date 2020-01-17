import urllib
from urllib import request,parse
import ssl

#response = urllib.request.urlopen('http://192.168.1.153/bugfree/index.php/site/login')
#print(response.read().decode('utf-8'))

#context = ssl._create_unverified_context()
url = 'http://192.168.1.153/bugfree/index.php/site/login'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
}
dict = {
    #'return_url':'http://192.168.1.153/bugfree/index.php/bug/list/12',
    'LoginForm[username]':'chenlue',
    'LoginForm[password]':'chenlue',
    'LoginForm[language]':'zh_cn',
    'LoginForm[rememberMe]':'0'
}
data = bytes(parse.urlencode(dict),'utf-8')
req = request.Request(url,data=data,headers=headers,method='POST')
response = request.urlopen(req,data=data,timeout=1000)
print(response.read().decode('utf-8'))
