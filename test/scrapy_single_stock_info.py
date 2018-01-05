'''
# 抓取指定股票的信息
# 参考： https://github.com/nooperpudd/chinastock/blob/master/stockHistory.py
# 抓取
'''

import requests
from lxml import html
import os
import pandas as pd
import numpy as np
from datetime import datetime
import time

stock_info_root = './stock_info'
os.makedirs(stock_info_root, exist_ok=True)

def get_proxy():
    # return requests.get("http://127.0.0.1:5010/get/").content
    proxy = requests.get("http://127.0.0.1:5010/get/").text
    proxy = "http://{}".format(proxy)
    return proxy

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def extract_columns(row):
    res = row.xpath('td//text()')
    columns = []
    for r in res:
        r = r.strip()
        if len(r) > 0:
            columns.append(r)
    return columns

def get_stock_info(stock_code, year, qr):
    info = []
    url = "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%s&jidu=%s" \
          % (stock_code, year, qr)
    # headers似乎是必须设置的，否则会被网站的反爬虫机制限制。
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    proxy = get_proxy()
    print('proxy addr is: {}'.format(proxy))
    # req = requests.get(url=url, headers=headers, proxies={"http": "http://{}".format(proxy)})
    # req = requests.get(url=url, proxies={"http": proxy})
    req = requests.get(url=url, headers=headers)
    # delete_proxy()
    tree = html.fromstring(req.content.decode('gbk'))
    rows = tree.xpath('//div[@class="tagmain"]/table[@id="FundHoldSharesTable"]/tr')
    try:
        col_names = rows[0]
        columns = extract_columns(col_names)
    except:
        # print('===>exception: {}-{}'.format(year, qr))
        return None, None
    rows = rows[1:]
    for row in rows:
        tmp_list = []
        res = row.xpath('td//text()')
        for r in res:
            r = r.strip()
            if len(r) > 0:
                tmp_list.append(r)
        info.append(tmp_list)
    return columns, info

def get_stock_all_infos(stock_code, years, qrs):
    infos = []
    columns = []
    for year in years:
        for qr in qrs:
            print('{}-{}'.format(year, qr))
            time.sleep(2)
            columns, tmp_list = get_stock_info(stock_code, year, qr)
            if columns is None:
                continue
            infos += tmp_list
    info_arr = np.array(infos)
    df = pd.DataFrame(info_arr, columns=columns)
    return df

# 按日期重排
def arange_by_date(df):
    df = df.sort_values(by=['日期'])
    df = df.reset_index(drop=True)
    return df


def test():
    # 丽珠集团：stock_code = '000513'
    # years: 2006-2017
    # qr: 1-4
    stock_code = '000513'
    years = [i for i in range(2006, 2018)]
    qrs = [i for i in range(1,5)]
    df = get_stock_all_infos(stock_code, years, qrs)
    df = arange_by_date(df)
    df.to_csv('stock_info/丽珠集团.csv')

if __name__ == '__main__':
    test()
