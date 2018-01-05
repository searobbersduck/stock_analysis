import sys
from scrapy_single_stock_info import get_stock_all_infos, arange_by_date
import pandas as pd
import os
import time

# import all stock codes
stock_code_file = './result/all_sh_list.csv'
df = pd.DataFrame.from_csv(stock_code_file)
print('====> load stock code file: {}'.format(stock_code_file))

root = 'stock_info'
os.makedirs(root, exist_ok=True)

for index, row in df.iterrows():
    try:
        stock_code = str(row[0])
        stock_name = str(row[1])
        years = [i for i in range(2006, 2018)]
        qrs = [i for i in range(1, 5)]
        df = get_stock_all_infos(stock_code, years, qrs)
        df = arange_by_date(df)
        print('====> extracting {} information'.format(stock_name))
        df.to_csv(os.path.join(root, '{}.csv'.format(stock_name)))
        # time.sleep(2)
    except:
        print('====> failed to extract {} information'.format(row[1]))
        continue