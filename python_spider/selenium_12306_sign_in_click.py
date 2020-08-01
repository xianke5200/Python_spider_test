import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

USERNAME = '155********'
PASSWORD = '***********'

CHAOJIYING_USERNAME = '***********'
CHAOJIYING_PASSWORD = '***********'
CHAOJIYING_SOFT_ID = '******'
CHAOJIYING_KIND = '9004'


class CrackTouClick():
    def __init__(self):     #登陆
        self.url = 'https://kyfw.12306.cn/otn/resources/login.html'
        path = r'F:\PycharmProjects\Python3爬虫\chromedriver.exe'
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        self.browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 20)
        self.email = USERNAME
        self.password = PASSWORD
        self.chaojiying = Chaojiying_Client(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)

    def crack(self):
        self.open()
        image = self.get_touclick_image()
        bytes_array = BytesIO()
        image.save(bytes_array, format='PNG')
        result = self.chaojiying.PostPic(bytes_array.getvalue(), CHAOJIYING_KIND)
        print(result)
        locations = self.get_points(result)
        self.touch_click_words(locations)
        self.login()
        try:
            success = self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.welcome-name'), '谭仁侯'))
            print(success)
            cc = self.browser.find_element(By.CSS_SELECTOR, '.welcome-name')
            print(cc.text)

        except TimeoutException:
            self.chaojiying.ReportError(result['pic_id'])
            self.crack()

    def open(self):
        self.browser.get(self.url)
        login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.login-hd-account')))
        login.click()
        time.sleep(3)
        username = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#J-userName')))
        password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#J-password')))
        username.send_keys(self.email)
        password.send_keys(self.password)

    def get_screenshot(self):
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_touclick_element(self):
        element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.login-pwd-code')))
        return element

    def get_position(self):
        element = self.get_touclick_element()
        time.sleep(3)
        location = element.location
        size = element.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)

    def get_touclick_image(self, name='12306.png'):
        top, bottom, left, right = self.get_position()
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def get_points(self, captcha_result):
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def touch_click_words(self, locations):
        for location in locations:
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_element(), location[0]/1.25, location[1]/1.25).click().perform()

    def login(self):
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'J-login')))
        submit.click()

import requests
from hashlib import md5

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

if __name__ == '__main__':
    crack = CrackTouClick()
    crack.crack()
