# coding=utf-8

import requests
import bs4
from bs4 import BeautifulSoup
from datetime import datetime

url = 'http://news.sina.com.cn/o/2017-05-16/doc-ifyfecvz1475416.shtml'
data = requests.get(url)
data.encoding = 'utf-8'
soup = BeautifulSoup(data.text,'html.parser')
timesource = soup.select('.time-source')[0].contents[0].strip()
print(datetime.strptime(timesource,'%Y年%m月%d日%H:%M'))