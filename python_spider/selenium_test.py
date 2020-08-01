# from selenium import webdriver
#
# driver = webdriver.Chrome()
# driver.get("https://www.baidu.com")
#
# input = driver.find_element_by_css_selector("#kw")
# input.send_keys("苹果")
#
# button = driver.find_element_by_css_selector("#su")
# button.click()

from selenium import webdriver
from selenium.webdriver import ActionChains

path = r'F:\PycharmProjects\Python3爬虫\chromedriver.exe'
browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to.frame('iframeResult')
source = browser.find_element_by_css_selector('#draggable')
target = browser.find_element_by_css_selector('#droppable')
actions = ActionChains(browser)
actions.drag_and_drop(source, target)
actions.perform()