#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: miaoj
@license: Apache Licence 
@file: dznh.py
@time: 2018-09-25 18:45
"""
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
import numpy as np
from fbprophet import Prophet

# 读取数据
#data1 = pd.read_csv('dznh_part1.csv')
#data2 = pd.read_csv('dznh_part2.csv')
#frame = [data1,data2]
#df = pd.concat(frame)
#df.to_csv('dznh_Sep_main.csv')

#读取合并后数据
df = pd.read_csv('dznh_Sep_main.csv',index_col=0)
#print (df.head())

#数据处理
df['采集时间'] = pd.to_datetime(df['采集时间'],format='%Y-%m-%d %H:%M:%S')
df.rename(columns={'采集时间':'ds', 'A相电流':'Ia','B相电流':'Ib','C相电流':'Ic',\
                   'A相电流THD':'Ia_THD','B相电流THD':'Ib_THD','C相电流THD':'Ic_THD',\
                   'A相电压':'Ua','B相电压':'Ub','C相电压':'Uc',\
                   'A相电压THD':'Ua_THD','B相电压THD':'Ub_THD','C相电压THD':'Uc_THD','总功率因数':'PF'},inplace = True)
print (df.head())

#正态分布函数 mu: 均值 sigma:标准差 pdf:概率密度函数 np.exp():概率密度函数公式
def normfun(x,mu,sigma):
    pdf = np.exp(-((x-mu)**2)/(2*pow(sigma,2))/(sigma*np.sqrt(2*np.pi)))
    return pdf

mu = np.mean(df.PF)
sigma = np.std(df.PF)

#x轴的取值范围 -5.5 至 5.5 单位长度0.1
x = np.arange(0,1.1,0.05)

#y轴为 x对应的函数
y = normfun(x,mu,sigma)

#绘图
#参数，颜色，线宽
plt.plot(x,y,color='g',linewidth=2.8)
#数据,数组，透明度，组宽，显示频率
plt.hist(df.PF,bins=17,alpha=0.6,rwidth=0.9,normed=True) #这里norm用来拟合正态分布
#命名
plt.title('normal Distribution')
plt.xlabel('Power Factor')
plt.ylabel('Probability')
plt.show(block=True)
