import requests
from bs4 import BeautifulSoup


# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
header_base = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
r = requests.get('https://iphone.reeoo.com/', headers=header_base)
content = r.text

# 把刚刚保存在content中的文件放入Beautiful Soup中
soup = BeautifulSoup(content, 'html.parser')
# print(soup.article.div.ul.find_all('li'))
# print(soup.article.div.ul)

imgs = soup.find_all(class_ = 'lazy')

for img in imgs:
    print(img)
