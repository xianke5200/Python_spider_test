from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import xlwt
import time
import re
import requests
import os

chrome_options = Options()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
#browser = webdriver.PhantomJS()
WAIT = WebDriverWait(browser, 20)
browser.set_window_size(1400, 900)

book = xlwt.Workbook(encoding='utf-8', style_compression=0)

sheet = book.add_sheet('蔡徐坤篮球', cell_overwrite_ok=True)
sheet.write(0, 0, '名称')
sheet.write(0, 1, '地址')
sheet.write(0, 2, '描述')
sheet.write(0, 3, '观看次数')
sheet.write(0, 4, '弹幕数')
sheet.write(0, 5, '发布时间')

n = 1

def search():
    try:
        print('开始访问b站....')
        browser.get("https://www.bilibili.com/")

        search = browser.find_element_by_xpath('//div[@class="nav-search"]/form/input')
        search.send_keys("蔡徐坤 篮球")
        search.send_keys(Keys.ENTER)

        # 跳转到新的窗口
        print('跳转到新窗口')
        all_h = browser.window_handles
        browser.switch_to.window(all_h[1])

        # html = browser.page_source
        # # print(html)
        # soup = BeautifulSoup(html, 'html.parser')
        # save_to_excel(soup)
        # total_index = soup.find(class_='page-item last').find(class_='pagination-btn')

        get_source()
        total_index = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                 "li.page-item.last > button")))

        # pattern = re.compile('<div class="page-wrap">.*?<li class="page-item last">.*?(\d+).*?</div>', re.S)
        # total_index = int(re.findall(pattern, html)[0])
        return int(total_index.text)
    except TimeoutException:
        return search()


def next_page(page_num):
    try:
        print('获取第(%d)页数据' % page_num)
        next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                          'li.page-item.next > button')))
        next_btn.click()
        get_source()
    except TimeoutException:
        browser.refresh()
        return next_page(page_num)


def save_to_excel(soup):
    list = soup.find(class_='video-list clearfix').find_all_next(class_='info')

    for item in list:
        item_title = item.find('a').get('title')
        item_link = item.find('a').get('href')
        item_dec = item.find(class_='des hide').text
        item_view = item.find(class_='so-icon watch-num').text
        item_biubiu = item.find(class_='so-icon hide').text
        item_date = item.find(class_='so-icon time').text

        print('爬取：' + item_title)

        global n

        sheet.write(n, 0, item_title)
        sheet.write(n, 1, item_link)
        sheet.write(n, 2, item_dec)
        sheet.write(n, 3, item_view)
        sheet.write(n, 4, item_biubiu)
        sheet.write(n, 5, item_date)

        n = n + 1

def img_save(soup):
    img_url_list = soup.find(class_='video-list clearfix').find_all_next(class_='img-anchor')
    index = 0
    for url in img_url_list:
        img_url = url.find('img').get('src')
        print(img_url)
        if img_url != '':
            img_request = ('https:'+ img_url).replace('webp', 'jpg')
            print(img_request)
            img_resp = requests.get(img_request)

            if not os.path.exists("cxk_video_img"):
                os.mkdir('cxk_video_img')
            with open('cxk_video_img/%d.jpg' %index, 'wb') as f:
                f.write(img_resp.content)
        index += 1
        time.sleep(1)

def video_save(soup):
    video_url_list = soup.find(class_='video-list clearfix').find_all_next(class_='info')
    index = 0
    for url in video_url_list:
        video_url = url.find('a').get('href')
        print(video_url)
        if video_url != None:
            video_request = 'https:'+ video_url
            print(video_request)
            video_resp = requests.get(video_request)

            if not os.path.exists("cxk_video_img"):
                os.mkdir('cxk_video_img')
            with open('cxk_video_img/%d.mp4' %index, 'wb') as f:
                f.write(video_resp.content)
        index += 1
        time.sleep(1)

def get_source():
    WAIT.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'ul.video-list.clearfix')))
    # browser.refresh()
    html = browser.page_source
    # print(html)
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)
    img_save(soup)
    # video_save(soup)


def main():
    try:
        total = search()
        # print(total)

        for i in range(2, int(total)+1):
            next_page(i)

    finally:
        browser.close()
        browser.quit()


if __name__ == '__main__':
    main()
    book.save(u'蔡徐坤篮球.xls')