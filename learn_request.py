import requests

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
r1 = requests.post(url, data=dict, headers=headers)
print(r1.text)