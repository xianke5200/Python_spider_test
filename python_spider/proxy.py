'''
urllib with proxy
'''
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

proxy = '127.0.0.1:1080'
proxy_handler = ProxyHandler({
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
})
opener = build_opener(proxy_handler)
try:
    response = opener.open('http://httpbin.org/get')
    print(response.read().decode('utf8'))
except URLError as e:
    print(e.reason)

#
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

proxy = 'username:password@127.0.0.1:1080'
proxy_handler = ProxyHandler({
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
})
opener = build_opener(proxy_handler)
try:
    response = opener.open('http://httpbin.org/get')
    print(response.read().decode('utf8'))
except URLError as e:
    print(e.reason)

#
import socks
import socket
from urllib import request
from urllib.error import URLError

socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 1080)
socket.socket = socks.socksocket
try:
    response = request.urlopen('http://httpbin.org/get')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)

'''
request with proxy
'''
import requests

proxy = '127.0.0.1:1080'
proxies = ({
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
})
try:
    response = requests.get('http://httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ChunkedEncodingError as e:
    print('Error', e.args)

#
import requests

proxy = 'username:password@127.0.0.1:1080'
proxies = ({
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
})
try:
    response = requests.get('http://httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ChunkedEncodingError as e:
    print('Error', e.args)

#request[socks]
import requests

proxy = '127.0.0.1:1080'
proxies = {
    'http': 'socks5://' + proxy,
    'https': 'socks5://' + proxy
}
try:
    response = requests.get('http://httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)

#socks
import requests
import socks
import socket

socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 1080)
socket.socket = socks.socksocket
try:
    response = requests.get('http://httpbin.org/get')
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)


'''
selenium with proxy
'''
from selenium import webdriver

proxy = '127.0.0.1:1080'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://' + proxy)
path = r'F:\PycharmProjects\Python3爬虫\chromedriver.exe'
browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
browser.get('http://httpbin.org/get')

#
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import zipfile

ip = '127.0.0.1'
port = 1080
username = 'username'
password = 'password'

manifest_json = """{"version":"1.0.0","manifest_version": 2,"name":"Chrome Proxy","permissions": ["proxy","tabs","unlimitedStorage","storage","<all_urls>","webRequest","webRequestBlocking"],"background": {"scripts": ["background.js"]
    }
}
"""

background_js ="""
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "%(ip) s",
            port: %(port) s
          }
        }
      }

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {username: "%(username) s",
            password: "%(password) s"
        }
    }
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
)
""" % {'ip': ip, 'port': port, 'username': username, 'password': password}

plugin_file = 'proxy_auth_plugin.zip'
with zipfile.ZipFile(plugin_file, 'w') as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("background.js", background_js)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
path = r'F:\PycharmProjects\Python3爬虫\chromedriver.exe'
chrome_options.add_extension(plugin_file)
browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
browser.get('http://httpbin.org/get')


'''
phantomJS
'''
from selenium import webdriver

service_args = [
    '--proxy=127.0.0.1:1080',
    '--proxy-type=http'
]
path = r'F:\PycharmProjects\Python3爬虫\phantomjs-2.1.1\bin\phantomjs.exe'
browser = webdriver.PhantomJS(executable_path=path, service_args=service_args)
browser.get('http://httpbin.org/get')
print(browser.page_source)


#
from selenium import webdriver

service_args = [
    '--proxy=127.0.0.1:1080',
    '--proxy-type=http',
    '--proxy-auth=username:password'
]
path = r'F:\PycharmProjects\Python3爬虫\phantomjs-2.1.1\bin\phantomjs.exe'
browser = webdriver.PhantomJS(executable_path=path, service_args=service_args)
browser.get('http://httpbin.org/get')
print(browser.page_source)
