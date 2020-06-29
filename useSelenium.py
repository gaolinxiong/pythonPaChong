
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

chrome_opt = Options()      # 创建参数设置对象.
chrome_opt.add_argument('--headless')   # 无界面化.
chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=1366,768')   # 设置窗口大小, 窗口大小会有影响.

def getImgs(page_source):

    return list

def findPic(url):
    driver = webdriver.Chrome(options=chrome_opt)
    driver.get(url)
    time.sleep(20)
    soup = BeautifulSoup(driver。page_source, 'html.parser')
    imgs = soup.find_all(class_='lazy')
    list = []
    for img in imgs:
        list.append(img['data-original'])
    driver.quit()
    return imgs

def findBook(url):
    driver = webdriver.Chrome(options=chrome_opt)
    driver.get(url)
    time.sleep(20)
    print('page_source', driver.page_source)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print('soup', soup)
    driver.quit()

findBook('https://read.douban.com/charts?type=sales&index=ebook&dcs=charts&dcm=charts-nav')

# try:
#     print(EC.title_contains('baidu'))
#     element = WebDriverWait(driver, 5).until(EC.title_is('baidu'))
#     print('123', element)
# except Exception as e:
#     print(e)
# finally:

# from selenium import webdriver
# import time

# print(webdriver)

# driver = webdriver.Chrome()     # 创建Chrome对象.
# # 操作这个对象.
# driver.get('https://www.baidu.com')     # get方式访问百度.
# time.sleep(2)
# driver.quit()
# 创建Chrome对象并传入设置信息.
# driver = webdriver.Chrome(options=chrome_opt)
# 操作这个对象.
# driver.get('https://iphone.reeoo.com/')     # get方式访问百度.

# time.sleep(5)
# print(driver.page_source)       # 打印加载的page code, 证明(prove) program is right.
# driver.quit()   # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.