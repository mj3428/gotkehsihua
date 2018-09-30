#!/usr/bin/env python
# encoding: utf-8
'''
@author: miaojue
@contact: major3428@foxmail.com
@software: pycharm
@file: harmonic_wave.py
@time: 2018-9-29 下午 2:56
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
from scipy import stats
from scipy import optimize

#读取数据然后合并
#data1 = pd.read_csv('dznh_harmonic1.1.csv')
#data2 = pd.read_csv('dznh_harmonic1.2.csv')
#data3 = pd.read_csv('dznh_harmonic2.1.csv')
#data4 = pd.read_csv('dznh_harmonic2.2.csv')
#data5 = pd.read_csv('nborl_part5.csv')
#frame = [data1,data2]
#df = pd.concat(frame)
#df0 = pd.merge(data1,data2,on=['采集时间'],how='left')
#df1 = pd.merge(data3,data4,on=['采集时间'],how='left')
#df = pd.concat([df0,df1])
#df.to_csv('dznh_harmonic.csv')
#print(df0.head(5),df1.head(5))
#df.pop('Unnamed: 0')
#print (df.head(10))
df = pd.read_csv('dznh_harmonic.csv',index_col=0)#index_col=0去掉索引
#将时间改成datatime的格式
df['采集时间'] = pd.to_datetime(df['采集时间'],format='%Y-%m-%d %H:%M:%S')
df.rename(columns={'采集时间':'ds',\
                   'A相电流H3':'Ia_H3','A相电流H5':'Ia_H5','A相电流H7':'Ia_H7', \
                   'A相电流H9':'Ia_H9','A相电流H11':'Ia_H11','A相电流H13':'Ia_H13',\
                   'A相电流H15':'Ia_H15','A相电流H17':'Ia_H17','A相电流H19':'Ia_H19', \
                   'A相电流H21': 'Ia_H21', \
                   'B相电流H3': 'Ib_H3','B相电流H5': 'Ib_H5','B相电流H7': 'Ib_H7', \
                   'B相电流H9': 'Ib_H9','B相电流H11': 'Ib_H11','B相电流H13': 'Ib_H13', \
                   'B相电流H15': 'Ib_H15','B相电流H17': 'Ib_H17','B相电流H19': 'Ib_H19',
                   'B相电流H21': 'Ib_H21', \
                   'C相电流H3': 'Ic_H3','C相电流H5': 'Ic_H5','C相电流H7': 'Ic_H7', \
                   'C相电流H9': 'Ic_H9','C相电流H11': 'Ic_H11','C相电流H13': 'Ic_H13', \
                   'C相电流H15': 'Ic_H15','C相电流H17': 'Ic_H17','C相电流H19': 'Ic_H19', \
                   'C相电流H21': 'Ic_H21'}, inplace = True)
max_values = np.array([[df.Ia_H3.max(),df.Ia_H5.max(),df.Ia_H7.max(),df.Ia_H9.max(),\
                       df.Ia_H11.max(),df.Ia_H13.max(),df.Ia_H15.max(),df.Ia_H17.max(),\
                       df.Ia_H19.max(),df.Ia_H21.max()],\
                      [df.Ib_H3.max(),df.Ib_H5.max(),df.Ib_H7.max(),df.Ib_H9.max(),\
                       df.Ib_H11.max(),df.Ib_H13.max(),df.Ib_H15.max(),df.Ib_H17.max(),\
                       df.Ib_H19.max(),df.Ib_H21.max()],\
                      [df.Ic_H3.max(),df.Ic_H5.max(),df.Ic_H7.max(),df.Ic_H9.max(),\
                       df.Ic_H11.max(),df.Ic_H13.max(),df.Ic_H15.max(),df.Ic_H17.max(),\
                       df.Ic_H19.max(),df.Ic_H21.max()]])
print(max_values)
#设置字体
mpl.rcParams['font.sans-serif'] = ['Microsoft Yahei']
mpl.rcParams['font.family']='sans-serif'#解决负号'-'显示为方块的问题
mpl.rcParams['axes.unicode_minus'] = False

Ya = max_values[0]
Yb = max_values[1]
Yc = max_values[2]
X = np.arange(3,22,2)
Na = ['3rd','5th','7th','9th','11th','13th','15th','17th','19th','21th']
print(X)
fig4 = plt.figure(figsize=[8.0,3.8],dpi=144,facecolor='gainsboro')
plt.bar(X,Ya,width=0.38,facecolor='gold',edgecolor='white',label='A相分次谐波',alpha=0.84)
plt.bar(X+0.38,Yb,width=0.38,facecolor='mediumaquamarine',edgecolor='white',label='B相分次谐波',alpha=0.84)
plt.bar(X+0.76,Yc,width=0.38,facecolor='lightcoral',edgecolor='white',label='C相分次谐波',alpha=0.84)
for a,b in zip(X,Ya):
    plt.text(a,b+0.1,'%.1f'%b,ha='center',va='bottom',fontsize=6)
for a,b in zip(X+0.38,Yb):
    plt.text(a,b+0.1,'%.1f'%b,ha='center',va='bottom',fontsize=6)
for a,b in zip(X+0.76,Yc):
    plt.text(a,b+0.1,'%.1f'%b,ha='center',va='bottom',fontsize=6)
for a,b in zip(X,Ya):
    plt.text(a,b+0.1,'%.1f'%b,ha='center',va='bottom',fontsize=6)
'''for a,b in zip(X+0.38,Na):
    plt.text(a,0,b,ha='center',va='bottom',fontsize=7,color='royalblue')

#多项式拟合
f1 = np.polyfit(X, Yb, 3) #3次多项式
p1 = np.poly1d(f1)
Yval = p1(X) #拟合Y值
plot2 = plt.plot(X, Yval, color='darkcyan',linestyle='--',label='趋势')

#e的b/X次方拟合
#e指数形式
def func(x, a, b):
    return a * np.exp(b / x)
#非线性最小二乘法拟合
popt, pcov = optimize.curve_fit(func, X, Yb)
#获取popt里面是拟合系数
a = popt[0]
b = popt[1]
Y_values = func(X,a,b) #拟合y值
plot2 = plt.plot(X, Y_values, color='mediumslateblue',linestyle='--',label='指数型拟合')
'''
plt.legend()
plt.grid(alpha=0.618,linestyle='-.')
#plt.xlim(2.5,22,1)
plt.xticks(X,Na)
plt.title('电流分次谐波(最大值)')
plt.xlabel('谐波次级')
plt.ylabel('谐波电流值')
plt.tight_layout()
ax1 =plt.gca()
ax1.patch.set_facecolor('lightcyan')#设置ax1区域背景颜色
ax1.patch.set_alpha(0.5)
plt.savefig('Harmonic_wave.png')
plt.show()
