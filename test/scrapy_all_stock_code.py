'''
# 抓取沪深所有股票的代码
# 需用用到的链接: http://quote.eastmoney.com/stocklist.html
'''

import requests
from lxml import html
import pandas as pd
import numpy as np
import os

url = 'http://quote.eastmoney.com/stocklist.html#sh'

req = requests.get(url=url)

# with open('all_sh_list.html', 'wb') as f:
#     f.write(req.content)

tree = html.fromstring(req.content.decode('gbk'))

all_stocks = tree.xpath('//div[@class="quotebody"]')[0].xpath('.//li')

df = pd.DataFrame(columns=['股票代码','股票名称','股票链接'])

for stock in all_stocks:
    stock_code = stock.xpath('./a/text()')[0]
    stock_link = stock.xpath('./a/@href')[0]
    dict = {}
    dict['股票名称'] = stock_code.split('(')[0]
    dict['股票代码'] = stock_code.split('(')[1].split(')')[0]
    dict['股票链接'] = stock_link
    # 只保留沪A，深A，创业板股票：[股票代码](https://baike.baidu.com/item/%E8%82%A1%E7%A5%A8%E4%BB%A3%E7%A0%81)
    if not (dict['股票代码'].startswith('6') or dict['股票名称'].startswith('3' or dict['股票名称'].startswith('0'))):
        continue
    df = df.append(dict, ignore_index=True)
    print(stock_code)

os.makedirs('./result', exist_ok=True)
df.to_csv('./result/all_sh_list.csv')