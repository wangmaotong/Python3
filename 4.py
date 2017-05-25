import json
from urllib.parse import urlencode
from requests.exceptions import RequestException
import lxml

import requests
from bs4 import BeautifulSoup
import re

##抓取索引页的内容，也就是今日头条街拍首页
def get_page_index(offset,keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except  RequestException:
        print ('error')
        return None

##解析索引页的内容，获取其中每个标题的url(也就是详情页的URL)
def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


##请求详情页信息
def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except  RequestException:
        print('error')
        return None

##解析详情页的信息
def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    image_pattern = re.compile('var gallery = (.*?);', re.S)
    result = re.search(image_pattern, html)
    if result:
        data = json.loads(result.group(1))
        sub_images = data.get('sub_images')
        images = [item.get('url') for item in sub_images]
        return {
                'title': title,
                'url': url,
                'images': images
            }


def main():
    html = get_page_index(0,'街拍')
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html,url)
            print(result)


if __name__ == '__main__':
    main()