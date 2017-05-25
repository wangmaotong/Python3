from json import JSONDecodeError
from urllib.parse import urlencode
import requests
from hashlib import md5
import json
from bs4 import BeautifulSoup
import re
import pymongo
from config import *
import os
from multiprocessing import Pool  ##引入线程池

client = pymongo.MongoClient(MONGO_URL,content = False)
db= client[MONGO_DB]


##1 首先构造ajax请求访问今日头条街拍页
def get_page_url(offset,keyword):
    data = {
    'offset': offset,
    'format': 'json',
    'keyword': keyword,
    'autoload': 'true',
    'count': '20',
    'cur_tab': '1',
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(data)   ##  urlencode是将字典格式的数据转换为url形式
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text  ##获得街拍首页的返回数据
        return None
    except  Exception:
        print ('获取街拍页数据失败')
        return None


##解析目标页的信息
def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except  Exception:
        print('error', url)
        return None

##获得目标页里面每张图片的url信息。
def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'html.parser')
    title = soup.select('title')[0].get_text()    ##获得组图的名称
    print(title)
    image_pattern = re.compile('var gallery = (.*?);',re.S)
    result = re.search(image_pattern,html)
    if result:
        data = json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            image = [item.get('url') for item in sub_images]
            for image in image:download_image(image)
            return {
                'title': title,
                'image': image,
                'url': url
            }

##解析首页获得的json格式的数据,通过json。lodas，获取其中article_url，即每篇文章的url链接
def parsr_page_url(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass


##获得图片链接之后下载这些图片
def download_image(url):
    print('正在下载',url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except  Exception:
        print ('请求图片出错')
        return None

#将下载的图片存入数据库
def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


##定义存储到mongodb的方法
def save_to_mongo(result):
    if result != None:
        if db[MONGO_TABLE].insert(result):
            print('存储到Mongodb成功',result)
            return True
        return False

##主函数从这里开始
def main(offset):
    html = get_page_url(offset,KEYWORD)
    for url in parsr_page_url(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html,url)
            if result: save_to_mongo(result)

if __name__ == '__main__':

    groups = [x * 20 for x in range(GROUP_START,GROUP_END + 1)]
    pool = Pool()
    pool.map(main,groups)