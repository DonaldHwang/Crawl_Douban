import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import csv
import json
import codecs
import time


def get_page(uppertolower, starter):
    headers = {
        'Host':'movie.douban.com',
        'Referer':'https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85&type=11&interval_id=100:90&action=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'}
    baseurl = 'https://movie.douban.com/j/chart/top_list?'

    params = {
        'type': '30',  # type determine the film type
        'interval_id': uppertolower,
        'action': '',
        'start': starter,
        'limit': '20'
    }
    url = baseurl + urlencode(params)
    s = requests.session()
    s.keep_alive = False
    s.adapters.DEFAULT_RETRIES = 5
    try:
        url_text = s.get(url, headers=headers)
    except:
        print("fail")
        time.sleep(2)

    return url_text.json()


def parse_page(html1):
    rows = []
    data = json.dumps(html1)
    data1 = json.loads(data)

    for every in data1:
        row = (
            every['rank'],
            every['regions'][0],
            every['rating'][0],
            every['title']
        )
        rows.append(row)

    # output file name modify
    with codecs.open('C:\\Users\\94983\\Desktop\\output_ancientcos.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


if __name__ == "__main__":
    for i in range(100, 0, -10):  # percent number
        for j in range(0, 50, 20):  # the number of films between 10 percent
            interval = str(i)+':'+str(i-10)
            html = get_page(interval, j)
            parse_page(html)
