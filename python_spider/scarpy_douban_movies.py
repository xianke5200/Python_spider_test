#import json
import requests
import re
import xlwt
from bs4 import BeautifulSoup

global n
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
sheet.write(0, 0, '名称')
sheet.write(0, 1, '图片')
sheet.write(0, 2, '排名')
sheet.write(0, 3, '评分')
sheet.write(0, 4, '作者')
sheet.write(0, 5, '简介')

def request_dangdang(url):
    try:
        response = requests.get(url)
        print('url request status code:', response.status_code)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def parse_paging_result(html):
    pattern = re.compile('<div class="paginator">.*?<a\shref="?start=(\d+)&filter=">(\d+)</a>.*?</div>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield{
            'start_count':item[0],
            'page':item[1]
        }

def save_to_execl(soup):
    list = soup.find(class_='grid_view').find_all('li')
    for item in list:
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = item.find(class_='').string
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text
        if(item.find(class_='inq') != None):
            item_intr = item.find(class_='inq').string

        print('爬取电影:' + item_index + '|' + item_name + '|' + item_score + '|' + item_intr)

        sheet.write(n, 0, item_name)
        sheet.write(n, 1, item_img)
        sheet.write(n, 2, item_index)
        sheet.write(n, 3, item_score)
        sheet.write(n, 4, item_author)
        sheet.write(n, 5, item_intr)
        n += 1

def main(page):
    url = 'https://movie.douban.com/top250?start='+str(page*25)+'&filter='
    html = request_dangdang(url)
    if html == None:
        print('url request failed')
    else:
        soup = BeautifulSoup(html, 'lxml')
        save_to_execl(soup)

if __name__ == '__main__':
    # url = 'https://movie.douban.com/top250'
    # html = request_dangdang(url)
    # print(html)
    #items = parse_paging_result(html)
    #get max page
    # for _item in items:
    #     print(_item)
    #
    # max_page = int(_item['page'])
    n = 1
    for i in range(0, 10):
        main(i)

    book.save(u'豆瓣最受欢迎的250部电影.xlsx')