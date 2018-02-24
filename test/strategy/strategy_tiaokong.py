# 1. 向上跳空不缺口？

import pandas as pd
import numpy as np
from datetime import timedelta

csv_file = '../stock_info/111.csv'

df = pd.DataFrame.from_csv(csv_file)

print(df.columns.values)

row_num = df.index.size

dict = {}

df_out = pd.DataFrame(columns=['日期', '间隔天数', '跳空比例', '索引'])

df['日期'] = pd.to_datetime(df['日期'])

for i in range(row_num-1):
    row0 = df.iloc[i]
    row1 = df.iloc[i+1]
    if not row1['最低价'] > row0['最高价']:
        continue
    date0 = row0['日期']
    date1 = row1['日期']
    deltad = date1 - date0
    ratio = (row1['最低价'] - row0['最高价'])/row0['最高价']*100
    ratio = round(ratio, 4)
    tmp_dict = {}
    tmp_dict['日期'] = date0
    tmp_dict['间隔天数'] = deltad
    tmp_dict['跳空比例'] = ratio
    tmp_dict['索引'] = i
    df_out = df_out.append(tmp_dict, ignore_index=True)

print(df_out)

df_out = df_out[df_out['跳空比例']>1]

df_out = df_out.reset_index(drop=True)

print(df_out)

list = []

for i in range(df_out.index.size):
    row = df_out.iloc[i]
    raw_index = row['索引']
    min_price = df.iloc[raw_index]['最高价']
    for j in range(raw_index+1, row_num):
        raw_row = df.iloc[j]
        if raw_row['最低价'] < min_price:
            list.append(raw_row['日期'])
            break

series_fill = pd.Series(np.array(list))

print(series_fill)

df_out['补缺口日期'] = series_fill

series_fill_delta = series_fill - df_out['日期']

df_out['补缺口间隔'] = series_fill_delta

df_out['补缺口间隔'] = df_out['补缺口间隔'] - df_out['间隔天数']

print(df_out)

df_out = df_out[df_out['补缺口间隔'] < timedelta(30)]

df_out = df_out.reset_index(drop=True)

print(df_out)
