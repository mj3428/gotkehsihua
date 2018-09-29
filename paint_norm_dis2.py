#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: miaoj
@license: Apache Licence
@file: dznh.py
@time: 2018-09-25 18:45
"""
import matplotlib as mpl
#mpl.use('Qt5Agg')
#print(mpl.matplotlib_fname())
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
from scipy import stats
import numpy as np
from fbprophet import Prophet
import matplotlib.mlab as mlab#拟合模块

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
#print (df.head())

'''
#正态分布函数 mu: 均值 sigma:标准差 pdf:概率密度函数 np.exp():概率密度函数公式
def normfun(x,mu,sigma):
    pdf = np.exp(-((x-mu)**2)/(2*pow(sigma,2))/(sigma*np.sqrt(2*np.pi)))
    return pdf'''
mu = np.mean([df.Ua,df.Ub,df.Uc],axis=1)
#mu = np.mean(df.Ua)
sigma = np.std([df.Ua,df.Ub,df.Uc],axis=1)
print (mu[1],sigma[1])

#设置字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.family']='sans-serif'#解决负号'-'显示为方块的问题
mpl.rcParams['axes.unicode_minus'] = False


#画布大小 长 宽 dpi分辨率 facecolor背景颜色
fig = plt.figure(figsize=[12.0,4.0],dpi=144,facecolor='gainsboro')

#数据,数组，透明度，组宽，显示频率 (n,bins,patches分别是hist模块返回的数据)#这里denisity用来拟合正态分布
#n返回数组 bins返回直方图个数加1 patches返回类型及个数
###############Ua###############
plt.subplot(131)
n_a, bins_a, patches_a = plt.hist(df.Ua,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='orange',\
                                  label='Probability',density=True)
length_a = plt.xlim()
width_a = (length_a[1]-length_a[0])/(len(bins_a)-1)
print (n_a,length_a,width_a,np.sum(n_a)) #n代表直方图的柱子的y值
#显示数字标签 ha代表对齐方式 0.9代表上面的直方图柱子的宽度 需要乘
for a,b in zip(bins_a,n_a):
    plt.text(a,b + 0.0025,'%.1f%%'%(b*width_a*100*0.9),ha='left', va= 'bottom',fontsize=6)
#拟合Ua
y_a = stats.norm.pdf(bins_a, mu[0], sigma[0])
norm_a = plt.plot(bins_a, y_a, color='gold',linestyle='--',label='norm')
#画参考线
plt.vlines(235,0,0.17,colors=(0.953,0.641,0.406),linestyles='-.',label='Upper 235V')
plt.legend(fontsize=6,loc='upper left')
plt.xlabel('Ua',fontsize=9)
plt.ylabel('Pdf',fontsize=9)

###############Ub###############
plt.subplot(132)
n_b, bins_b, patches_b = plt.hist(df.Ub,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='mediumseagreen', \
                                  label='Probability',density=True) #这里norm用来拟合正态分布
length_b = plt.xlim()
width_b = (length_b[1]-length_b[0])/(len(bins_b)-1)
print (n_b,length_b,width_b) #n代表直方图的柱子的y值
#显示数字标签 ha代表对齐方式 0.9代表上面的直方图柱子的宽度 需要乘
for a,b in zip(bins_b,n_b):
    plt.text(a,b + 0.0025,'%.1f%%'%(b*width_b*100*0.9),ha='left', va= 'bottom',fontsize=6)
#拟合Ub
y_b = stats.norm.pdf(bins_b, mu[1], sigma[1])
norm_b = plt.plot(bins_b, y_b, 'g--',label='norm')
#画参考线
plt.vlines(235,0,0.165,colors=(0.395,0.816,0.766),linestyles='-.',label='Upper 235V')
plt.legend(fontsize=6,loc='upper left')
plt.xlabel('Ub',fontsize=9)
plt.ylabel('Pdf',fontsize=9)

###############Uc###############
plt.subplot(133)
n_c, bins_c, patches_c = plt.hist(df.Uc,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='orangered', \
                                  label='Probability',density=True) #这里norm用来拟合正态分布
length_c = plt.xlim()
width_c = (length_c[1]-length_c[0])/(len(bins_c)-1)
print (n_c,length_c,width_c) #n代表直方图的柱子的y值
#显示数字标签 ha代表对齐方式 0.9代表上面的直方图柱子的宽度 需要乘
for a,b in zip(bins_c,n_c):
    plt.text(a,b + 0.0025,'%.1f%%'%(b*width_c*100*0.9),ha='left', va= 'bottom',fontsize=6)
#拟合Uc
y_c = stats.norm.pdf(bins_c, mu[2], sigma[2])
norm_c = plt.plot(bins_c, y_c, 'r--',label='norm')
#画参考线
plt.vlines(235,0,0.165,colors=(0.957,0.625,0.559),linestyles='-.',label='Upper 235V')
plt.legend(fontsize=6,loc='upper left')
plt.xlabel('Uc',fontsize=9)
plt.ylabel('Pdf',fontsize=9)

#绘图
#设置数字标签
#plt.text(0.43,3.90, r'$\mu=0.69,\ \sigma=0.12$')

#图例设置
#plt.legend([],loc='lower right')

#命名
#总标题
plt.suptitle('A、B、C三相电压分布图')
#plt.title('正态分布')

#调整子图位置
#pad用于设置绘图区边缘与画布边缘的距离大小
#w_pad用于设置绘图区间水平距离的大小
#h_pad用于设置绘图区间垂直距离的大小
fig.tight_layout(pad=2.3)
#plt.show(block=True)
plt.show()
