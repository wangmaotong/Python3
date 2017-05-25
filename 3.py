
# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
import pymongo


connection = pymongo.MongoClient()
TuPianDB = connection.TuPianDB
TuPianTable = TuPianDB.books


url = 'http://quote.eastmoney.com/sh601238.html'
data = requests.get(url)
soup = BeautifulSoup(data.text,'html.parser')
for m in soup.select('#picr'):
    pattern = re.compile('http.*?"')
    html = pattern.findall(str(m))
    TuPian = {}
    TuPian['name'] = str(html)
    TuPianTable.insert_one(TuPian)
    image = requests.get(html).read()
    with open('001.jpg','wb') as fp:
        fp.write(image)
        print('图片下载成功')






    # dt_1 > tbody > tr:nth-child(1) > td:nth-child(2) > a

