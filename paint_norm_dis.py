#!/usr/bin/env python
# encoding: utf-8
'''
@author: miaojue
@contact: major3428@foxmail.com
@software: pycharm
@file: merge_all_data.py
@time: 2018-9-18 上午 9:11
@desc:
'''
import matplotlib as mpl
import pandas as pd
from pandas import DataFrame
import numpy as np
from fbprophet import Prophet
import matplotlib.pyplot as plt
from sklearn import preprocessing
import matplotlib.mlab as mlab#拟合模块

#读取数据然后合并
#data1 = pd.read_csv('nborl_part1.csv')
#data2 = pd.read_csv('nborl_part2.csv')
#data3 = pd.read_csv('nborl_part3.csv')
#data4 = pd.read_csv('nborl_part4.csv')
#data5 = pd.read_csv('nborl_part5.csv')
#frame = [data1,data2]
#df = pd.concat(frame)
#df.pop('Unnamed: 0')
#print (df.head(10))

#保存
#df.to_csv('nborl_Aug_Sep_main1.csv')

#判断函数,预警信号判断
def make_signal(a,b):
    if a < 30:
        return 0
    elif a >=30 and b >= 0.15:
        return 1
    else:
        return 0
#读取合并后的数据文件
df = pd.read_csv('nborl_Aug_Sep_main1.csv',index_col=0) #index_col=0去掉索引
#print (df.head(10))

#将时间改成datatime的格式
df['采集时间'] = pd.to_datetime(df['采集时间'],format='%Y-%m-%d %H:%M:%S')
df.rename(columns={'采集时间':'ds', 'A相电流':'Ia','B相电流':'Ib','C相电流':'Ic', \
                   'A相电压':'Ua','B相电压':'Ub','C相电压':'Uc',\
                   '三相有功功率':'P','三相无功功率':'Q','剩余电流IR':'IR'}, inplace = True)
df = df[['ds','Ia','Ib','Ic','Ua','Ub','Uc','P','Q']]
df['L_factor']=(np.sqrt(np.square(df['P'])+np.square(df['Q'])))/1000000.0
#print (type(df.Ia)) #df是Series序列类型
df['I_mean'] = (df.Ia+df.Ib+df.Ic)/3.0 #False会生成新的DataFrame
df['I_unbalance_percent'] = df.apply(lambda x : max(abs(x['Ia']-x['I_mean']),\
                                                    abs(x['Ib']-x['I_mean']),\
                                                    abs(x['Ic']-x['I_mean']))/x['I_mean'],axis=1)
#这里dataframe.apply里的axis=1代表函数用于每一列 0代表函数用于每一行


# 对数
df['log'] = np.log(df['I_unbalance_percent'])#本身条件限制，取对数查看

mu = df['log'].mean()
sigma = np.std(df['log'])
#print (np.mean(df['I_unbalance_percent'])) #结果与df.mean一致
print (mu,sigma)

#z-score
df['z-score'] = df.apply(lambda x:(x['I_unbalance_percent']- mu)/sigma,axis=1)

#sklearn求z-score因结果不同 先屏蔽
#print (len(df['I_unbalance_percent']))
#arrs = np.array(df['I_unbalance_percent']).reshape(int(len(df['I_unbalance_percent'])/2),2)
#zscore_scaler = preprocessing.StandardScaler() #建立对象
#data_scale = zscore_scaler.fit_transform(arrs)
#df['norm'] = np.array(data_scale).reshape(int(len(df['I_unbalance_percent'])),1)
#print (df['norm'].head(10))

#正态分布函数 mu: 均值 sigma:标准差 pdf:概率密度函数 np.exp():概率密度函数公式
def normfun(x,mu,sigma):
    pdf = np.exp(-((x-mu)**2)/(2*pow(sigma,2))/(sigma*np.sqrt(2*np.pi)))
    return pdf

#设置字体
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

#数据,数组，透明度，组宽，显示频率 (n,bins,patches分别是hist模块返回的数据)
n, bins, patches = plt.hist(df.log,bins=50,alpha=0.6,rwidth=0.9,density=True) #这里norm用来拟合正态分布

#拟合
y = mlab.normpdf(bins, mu, sigma)
plt.plot(bins, y, 'g--')

#图例设置
plt.legend(labels = ['拟合正态分布', 'Log Values'], loc = 'upper left')

#设置数字标签
#plt.text(0.43,3.90, r'$\mu=0.23,\ \sigma=0.20$')

#命名
plt.title('对数与拟合正态分布')
plt.xlabel('电流不平衡')
plt.ylabel('概率密度')
plt.savefig('I_unbalance_percent-Log.png')
plt.show()

#预警产生信号
#df['signal'] = df.apply(lambda x:make_signal(x.I_mean,x.I_unbalance_percent),axis=1)
#df['signal'] = df['signal'].astype(dtype=np.int64)
#print (df[['I_mean','signal']].head(10)) #检验结果

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

#df['y'] = df['signal'] #对数情况
df['y'] = df['I_unbalance_percent']
prophet = Prophet() #可添加区间interval_width=小于1的值表示期望数值范围
prophet.fit(df)
future = prophet.make_future_dataframe(freq='H',periods=24)
forecast = prophet.predict(future)
#plt.figure(figsize=(24,8)) #无效
#plt.title('LoadFactor_circle_prediction') #命名表名
#prophet.plot(forecast, xlabel = 'Date', ylabel = 'log_values').savefig('LoadFactor_log.png')
#prophet.plot(forecast, xlabel = 'Date', ylabel = 'log_values').show()
#prophet.plot(forecast).savefig('LoadFactor_log.png')
#prophet.plot(forecast,xlabel = 'Date', ylabel = 'original_values').show()
#prophet.plot(forecast,xlabel = 'Date', ylabel = 'original_values').savefig('I_unbalance_percent_original.png')
#prophet.plot(forecast,xlabel = 'Date', ylabel = 'adjusted_signal').savefig('I_unbalance_percent_adjusted_signal.png')
#prophet.plot_components(forecast).savefig('LoadFactor_components.png')
#prophet.plot_components(forecast).show()
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
#future = prophet.make_seasonality_features(df['date'])
