import pandas as pd
from pandas import DataFrame
import numpy as np
from fbprophet import Prophet

#读取数据
#data1 = pd.read_csv('hddc_merge1.csv')
#data2 = pd.read_csv('hddc_merge2.csv')
#data3 = pd.read_csv('hddc_merge3.csv')
#data4 = pd.read_csv('hddc_merge4.csv')
#frame = [data1,data2,data3,data4]
#df = pd.concat(frame)
#df.pop('Unnamed: 0')
#print (df.head(10))

#保存
#df.to_csv('merge_all_data.csv')

#读取合并后的数据文件
df = pd.read_csv('merge_all_data.csv',index_col=0) #index_col=0去掉索引

#将时间改成datatime的格式
df['采集时间'] = pd.to_datetime(df['采集时间'],format='%Y-%m-%d %H:%M:%S')
df.rename(columns={'采集时间':'date', 'A相电流':'Ia','B相电流':'Ib','C相电流':'Ic', \
                   'A相电压':'Ua','B相电压':'Ub','C相电压':'Uc',\
                   '三相有功功率':'P','三相无功功率':'Q','剩余电流IR':'IR'}, inplace = True)
df = df[['date','Ia','Ib','Ic','Ua','Ub','Uc','P','Q']]
df['L_factor']=(np.sqrt(np.square(df['P'])+np.square(df['Q'])))/1000000.0

#☆☆☆想按时间升序排列(但未实现)
#df.date = pd.DatetimeIndex(df.date)
#df.date.sort_index(ascending=True)
#df.sort_values(by='date',axis=0,ascending=True) #axis=0按列排序

#查看数据类型
print ('{:*^60}'.format('Data dtypes:'))
print (df.dtypes)  # 数据类型
print (df.head(10))

#缺失值审查(未缺失)
#na_cols = df.isnull().any(axis=0)  # 查看每一列是否具有缺失值
#print ('NA Cols:')
#print (na_cols)  # 查看具有缺失值的列
#print ('-' * 30)

df['y'] = np.log(df['L_factor'])
prophet = Prophet()
prophet.fit(df)
future = prophet.make_future_dataframe(freq='H',periods=24)
forecast = prophet.predict(future)
prophet.plot(forecast).show()
#future = prophet.make_seasonality_features(df['date'])
