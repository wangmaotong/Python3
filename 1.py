# coding=utf-8

import requests
import bs4
from bs4 import BeautifulSoup

url = 'http://news.sina.com.cn/china/'
data = requests.get(url)
data.encoding = 'utf-8'
soup = BeautifulSoup(data.text,'html.parser')
for news in soup.select('.news-item'):
    if len(news.select('h2')) > 0:
        h2 = news.select('h2')[0].text
        a = news.select('a')[0]['href']
        time = news.select('.time')[0].text
        print(time,h2,a)
