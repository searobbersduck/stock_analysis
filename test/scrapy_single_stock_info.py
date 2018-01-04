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

stock_info_root = './stock_info'
os.makedirs(stock_info_root, exist_ok=True)

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
    req = requests.get(url=url)
    tree = html.fromstring(req.content.decode('gbk'))
    rows = tree.xpath('//div[@class="tagmain"]/table[@id="FundHoldSharesTable"]/tr')
    try:
        col_names = rows[0]
        columns = extract_columns(col_names)
    except:
        print('===>exception: {}-{}'.format(year, qr))
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
