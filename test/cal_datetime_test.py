# 1. 参考：日期的加减操作：[python计算时间差，时间加减运算代码](http://outofmemory.cn/code-snippet/698/python-tell-shijiancha-time-jiajian-operation-code)

from datetime import datetime
from datetime import timedelta

d1 = datetime(2017,3,3)
d2 = datetime(2017,3,5)

deltad = d1 - d2
print(deltad.days)

# 2. string to datetime
import pandas as pd

csv_file = 'stock_info/龙马环卫.csv'
df = pd.DataFrame.from_csv(csv_file)

df['日期'] = pd.to_datetime(df['日期'])

delta_date = df['日期'][1:].reset_index(drop=True) - df['日期'][:-1].reset_index(drop=True)
print(len(df['日期']))
print(len(delta_date))

print(delta_date[:20])

print(delta_date.nlargest(6))

# delta_date = delta_date.insert(0, timedelta(100))

delta_date = pd.concat(pd.Series([timedelta(100)]), delta_date)

print(len(delta_date))


# 3.