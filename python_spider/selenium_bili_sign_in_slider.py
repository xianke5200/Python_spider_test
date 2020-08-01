from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import random
from PIL import Image

def init():
    global url, browser, username, password, wait

    url = 'https://passport.bilibili.com/login'
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    username = '15671621332'
    password = 'ws4658213'
    wait = WebDriverWait(browser, 20)

def login():
    browser.get(url)
    user = wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
    passwd = wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
    user.send_keys(username)
    passwd.send_keys(password)
    login_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn.btn-login')))
    time.sleep(random.random()*3)
    login_btn.click()

def find_element():
    c_background = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas.geetest_canvas_bg.geetest_absolute')))
    c_slice = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas.geetest_canvas_slice.geetest_absolute')))
    c_full_bg = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas.geetest_canvas_fullbg.geetest_fade.geetest_absolute')))
    hide_element(c_slice)
    save_screenshot(c_background, 'back')
    show_element(c_slice)
    save_screenshot(c_slice, 'slice')
    show_element(c_full_bg)
    save_screenshot(c_full_bg, 'full')

def hide_element(element):
    browser.execute_script("arguement[0].style=arguement[1]", element, "display: none;")

def show_element(element):
    browser.execute_script("arguement[0].style=arguement[1]", element, "display: block;")

def save_screenshot(obj, name):
    try:
        pic_url = browser.save_screenshot('.\\bilibili.png')
        print("%s:截图成功!" % pic_url)
        left =obj.location['x']
        top = obj.location['y']
        right = left + obj.size['width']
        buttom = top + obj.size['height']
        print('图:' + name)
        print('Left %s' % left)
        print('Top %s' % top)
        print('Right %s' % right)
        print('Buttom %s' % buttom)
        print('')
        im = Image.open('.\\bilibili.png')
        im = im.crop(left, top, right, buttom)
        file_name = 'bili_' + name + '.png'
        im.save(file_name)
    except BaseException as msg:
        print('%s: 截图失败!' % msg)

def slide():
    distance = get_distance(Image.open('.\\bili_back.png'), Image.open('.\\bili_full.png'))
    print('计算偏移量: %s Px' % distance)
    trace = get_trace(distance - 5)
    move_to_gap(trace)
    time.sleep(3)

def get_distance(bg_image, fullbg_image):
    distance = 60
    for i in range(distance, fullbg_image.size[0]):
        for j in range(fullbg_image.size[1]):
            if not is_pixel_equal(fullbg_image, bg_image, i, j):
                return i

def is_pixel_equal(bg_image, fullbg_image, x, y):
    bg_pixel = bg_image.load()[x, y]
    fullbg_pixel = fullbg_image.load()[x, y]
    threshold = 60
    if (abs(bg_pixel[0] - fullbg_pixel[0] < threshold) and abs(bg_pixel[1] - fullbg_pixel[1] < threshold)
            and abs(bg_pixel[2] - fullbg_pixel[2] < threshold)):
        return True
    else:
        return False

def get_trace(distance):
    trace = []
    faster_distance = distance * (4/5)
    start, v0, t = 0, 0, 0.1
    while start < distance:
        if start < faster_distance:
            a = 10
        else:
            a = -10
        move = v0 * t + 1/2*a*t*t
        v = v0 + a*t
        v0 = v
        start += move
        trace.append(round(move))
    return trace

def move_to_gap(trace):
    slider = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.geetest_slider_button')))
    ActionChains(browser).click_and_hold(slider).perform()
    for x in trace:
        ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(browser).release().perform()

if __name__ == '__main__':
    init()
    login()
    find_element()
    slide()