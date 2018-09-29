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
print (df.Ia_THD.head(18))

'''
#正态分布函数 mu: 均值 sigma:标准差 pdf:概率密度函数 np.exp():概率密度函数公式
def normfun(x,mu,sigma):
    pdf = np.exp(-((x-mu)**2)/(2*pow(sigma,2))/(sigma*np.sqrt(2*np.pi)))
    return pdf'''
mu = np.mean([df.Ua,df.Ub,df.Uc,df.Ia,df.Ib,df.Ic,\
              df.Ua_THD,df.Ub_THD,df.Uc_THD, \
              df.Ia_THD, df.Ib_THD, df.Ic_THD],axis=1)
#mu = np.mean(df.Ua)
sigma = np.std([df.Ua,df.Ub,df.Uc,df.Ia,df.Ib,df.Ic,
                df.Ua_THD, df.Ub_THD, df.Uc_THD,\
                df.Ia_THD, df.Ib_THD, df.Ic_THD],axis=1)
freq = len(df.ds) #总样本频次
print (mu[3],sigma[3])

#设置字体
mpl.rcParams['font.sans-serif'] = ['Microsoft Yahei']
mpl.rcParams['font.family']='sans-serif'#解决负号'-'显示为方块的问题
mpl.rcParams['axes.unicode_minus'] = False


#画布大小 长 宽 dpi分辨率 facecolor背景颜色
fig1 = plt.figure(figsize=[11.0,3.8],dpi=144,facecolor='gainsboro')



#数据,数组，透明度，组宽，显示频率 (n,bins,patches分别是hist模块返回的数据)#这里denisity用来拟合正态分布
#n返回数组 bins返回直方图个数加1 patches返回类型及个数
#############Ua###############
ax_ua = plt.subplot(131)
n_a, bins_a, patches_a = plt.hist(df.Ua,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='orange',\
                                  label='Probability',density=False)
#sum_a =np.sum(n_a) #a电压的总数
print(n_a)
#显示数字标签 ha代表对齐方式
for a,b in zip(bins_a,n_a):
    plt.text(a,b + 2,'%.1f%%'%(b/freq*100),ha='left', va= 'bottom',fontsize=6)
#拟合Ua
y_a = stats.norm.pdf(bins_a, mu[0], sigma[0])
norm_a = plt.plot(bins_a, y_a*freq, color='goldenrod',linestyle='--',label='norm')
#画参考线
plt.vlines(235,0,165,colors=(0.953,0.641,0.406),linestyles='-.',label='Upper 235V')
plt.legend(fontsize=6,loc='upper left')
plt.xlabel('Ua',fontsize=9)
plt.ylabel('Frequency',fontsize=9)
plt.setp(ax_ua.get_yticklabels(),fontsize=9)

#############Ub###############
ax_ub = plt.subplot(132,sharey=ax_ua)
n_b, bins_b, patches_b = plt.hist(df.Ub,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='mediumseagreen', \
                                  label='Probability',density=False) #这里norm用来拟合正态分布
#sum_b =np.sum(n_b) #b电压的总数
print (n_b) #n代表直方图的柱子的y值
for a,b in zip(bins_b,n_b):
    plt.text(a,b + 2,'%.1f%%'%(b/freq*100),ha='left', va= 'bottom',fontsize=6)
#拟合Ub
y_b = stats.norm.pdf(bins_b, mu[1], sigma[1])
norm_b = plt.plot(bins_b, y_b*freq, 'g--',label='norm')
#画参考线
plt.vlines(235,0,165,colors=(0.395,0.816,0.766),linestyles='-.',label='Upper 235V')
plt.legend(fontsize=6,loc='upper left')
plt.xlabel('Ub',fontsize=9)
plt.ylabel('Frequency',fontsize=9)
plt.setp(ax_ub.get_yticklabels(),visible=False)

#############Uc###############
ax_uc = plt.subplot(133,sharey=ax_ua)
n_c, bins_c, patches_c = plt.hist(df.Uc,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='orangered', \
                                  label='Probability',density=False) #这里norm用来拟合正态分布
#sum_c = np.sum(n_c) #c电压的总数
print (n_c) #n代表直方图的柱子的y值
for a,b in zip(bins_c,n_c):
    plt.text(a,b + 2,'%.1f%%'%(b/freq*100),ha='left', va= 'bottom',fontsize=6)
#拟合Uc
y_c = stats.norm.pdf(bins_c, mu[2], sigma[2])
norm_c = plt.plot(bins_c, y_c*freq, 'r--',label='norm')
#画参考线
plt.vlines(235,0,165,colors=(0.957,0.625,0.559),linestyles='-.',label='Upper 235V')
plt.legend(fontsize=6,loc='upper left')
plt.xlabel('Uc',fontsize=9)
plt.ylabel('Frequency',fontsize=9)
plt.setp(ax_uc.get_yticklabels(),visible=False)


#绘图
#设置数字标签
#plt.text(0.43,3.90, r'$\mu=0.69,\ \sigma=0.12$')

#图例设置
#plt.legend([],loc='lower right')

#命名
#总标题
plt.suptitle('A、B、C三相电压概率分布图')
#plt.title('正态分布')

#调整子图位置
#pad用于设置绘图区边缘与画布边缘的距离大小
#w_pad用于设置绘图区间水平距离的大小
#h_pad用于设置绘图区间垂直距离的大小
fig1.tight_layout(pad=2.3)
#plt.show(block=True)
#plt.show()



#画电流
#画布大小 长 宽 dpi分辨率 facecolor背景颜色
fig2 = plt.figure(figsize=[11.0,3.8],dpi=144,facecolor='gainsboro')

#########Ia#######Ia#############
ax_ia  = plt.subplot(131)
n_Ia, bins_Ia, patches_Ia = plt.hist(df.Ia,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='orange',\
                                  label='Probability',density=False)
print(n_Ia)#检查
#显示数字标签 ha代表对齐方式
for a,b in zip(bins_Ia,n_Ia):
    plt.text(a,b + 2,'%.1f%%'%(b/freq*100),ha='left', va= 'bottom',fontsize=6)
#拟合Ia
y_Ia = stats.norm.pdf(bins_Ia, mu[3], sigma[3])
norm_Ia = plt.plot(bins_Ia, y_Ia*freq*66.7, color='goldenrod',linestyle='--',label='norm')
#print(y_Ia)
plt.legend(fontsize=6,loc='upper right')
plt.xlabel('Ia',fontsize=9)
plt.ylabel('Frequency',fontsize=9)
plt.setp(ax_ia.get_yticklabels(),fontsize=9)

#########Ib#######Ib#############
ax_ib = plt.subplot(132,sharey=ax_ia)
n_Ib, bins_Ib, patches_Ib = plt.hist(df.Ib,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='mediumseagreen', \
                                  label='Probability',density=False)
print(n_Ib)#检查
#显示数字标签 ha代表对齐方式
for a,b in zip(bins_Ib,n_Ib):
    plt.text(a,b + 2,'%.1f%%'%(b/freq*100),ha='left', va= 'bottom',fontsize=6)
#拟合Ia
y_Ib = stats.norm.pdf(bins_Ib, mu[4], sigma[4])
norm_Ib = plt.plot(bins_Ib, y_Ib*freq*66.7, 'g--',label='norm')

plt.legend(fontsize=6,loc='upper right')
plt.xlabel('Ib',fontsize=9)
plt.ylabel('Frequency',fontsize=9)
plt.setp(ax_ib.get_yticklabels(),visible=False)

#########Ic#######Ic#############
ax_ic = plt.subplot(133)
n_Ic, bins_Ic, patches_Ic = plt.hist(df.Ic,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='orangered', \
                                  label='Probability',density=False)
print(n_Ic)#检查
#显示数字标签 ha代表对齐方式
for a,b in zip(bins_Ic,n_Ic):
    plt.text(a,b + 2,'%.1f%%'%(b/freq*100),ha='left', va= 'bottom',fontsize=6)
#拟合Ib
y_Ic = stats.norm.pdf(bins_Ic, mu[5], sigma[5])
norm_Ic = plt.plot(bins_Ic, y_Ic*freq*66.7,'r--',label='norm')

plt.legend(fontsize=6,loc='upper right')
plt.xlabel('Ic',fontsize=9)
plt.ylabel('Frequency',fontsize=9)
plt.setp(ax_ic.get_yticklabels(),visible=False)

plt.suptitle('A、B、C三相电流概率分布图')
fig2.tight_layout(pad=2.3)
#plt.show(block=True)
#plt.show()


#电压谐波含有率
fig3 = plt.figure(figsize=[11.0,3.8],dpi=144,facecolor='gainsboro')
###############Ua_THD##############
ax_thdua  = plt.subplot(131)
n_thdua, bins_thdua, patches_thdua = plt.hist(df.Ua_THD,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='orange',\
                                  label='Probability',density=False)
print(n_thdua)#检查
#显示数字标签 ha代表对齐方式
for a,b in zip(bins_thdua,n_thdua):
    plt.text(a,b + 2,'%.1f%%'%(b/freq*100),ha='left', va= 'bottom',fontsize=6)
#拟合Ia
y_thdua = stats.norm.pdf(bins_thdua, mu[6], sigma[6])
norm_thdua = plt.plot(bins_thdua, y_thdua*freq*0.23, color='goldenrod',linestyle='--',label='norm')
#print(y_Ia)
plt.legend(fontsize=6,loc='upper right')
plt.xlabel('THD_Ua',fontsize=9)
plt.ylabel('Frequency',fontsize=9)
plt.setp(ax_thdua.get_yticklabels(),fontsize=9)

###############Ub_THD##############
ax_thdub  = plt.subplot(132,sharey=ax_thdua)
n_thdub, bins_thdub, patches_thdub = plt.hist(df.Ub_THD,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='mediumseagreen',\
                                  label='Probability',density=False)
print(n_thdub)#检查
#显示数字标签 ha代表对齐方式
for a,b in zip(bins_thdub,n_thdub):
    plt.text(a,b + 2,'%.1f%%'%(b/freq*100),ha='left', va= 'bottom',fontsize=6)
#拟合Ia
y_thdub = stats.norm.pdf(bins_thdub, mu[7], sigma[7])
norm_thdub = plt.plot(bins_thdub, y_thdub*freq*0.23, 'g--',label='norm')
#print(y_Ia)
plt.legend(fontsize=6,loc='upper right')
plt.xlabel('THD_Ub',fontsize=9)
plt.ylabel('Frequency',fontsize=9)
plt.setp(ax_thdub.get_yticklabels(),visible=False)

###############Uc_THD##############
ax_thduc  = plt.subplot(133,sharey=ax_thdua)
n_thduc, bins_thduc, patches_thduc = plt.hist(df.Uc_THD,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='orangered',\
                                  label='Probability',density=False)
print(n_thduc)#检查
#显示数字标签 ha代表对齐方式
for a,b in zip(bins_thduc,n_thduc):
    plt.text(a,b + 2,'%.1f%%'%(b/freq*100),ha='left', va= 'bottom',fontsize=6)

y_thduc = stats.norm.pdf(bins_thduc, mu[8], sigma[8])
norm_thduc = plt.plot(bins_thduc, y_thduc*freq*0.23, 'r--',label='norm')

plt.legend(fontsize=6,loc='upper right')
plt.xlabel('THD_Uc',fontsize=9)
plt.ylabel('Frequency',fontsize=9)
plt.setp(ax_thduc.get_yticklabels(),visible=False)

plt.suptitle('A、B、C三相电压谐波含有率概率分布图')
fig2.tight_layout(pad=2.3)


#电流谐波含有率
fig4 = plt.figure(figsize=[11.0,3.8],dpi=144,facecolor='gainsboro')
###############Ia_THD##############
ax_thdia  = plt.subplot(131)
n_thdia, bins_thdia, patches_thdia = plt.hist(df.Ia_THD,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='orange',\
                                  label='Probability',density=False)
print(n_thdia)#检查
#显示数字标签 ha代表对齐方式
for a,b in zip(bins_thdia,n_thdia):
    plt.text(a,b + 2,'%.1f%%'%(b/freq*100),ha='left', va= 'bottom',fontsize=6)

y_thdia = stats.norm.pdf(bins_thdia, mu[9], sigma[9])
norm_thdia = plt.plot(bins_thdia, y_thdia*freq*2, color='goldenrod',linestyle='--',label='norm')

plt.legend(fontsize=6,loc='upper right')
plt.xlabel('THD_Ia',fontsize=9)
plt.ylabel('Frequency',fontsize=9)
plt.setp(ax_thdia.get_yticklabels(),fontsize=9)

###############Ub_THD##############
ax_thdib  = plt.subplot(132,sharey=ax_thdia)
n_thdib, bins_thdib, patches_thdib = plt.hist(df.Ib_THD,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='mediumseagreen',\
                                  label='Probability',density=False)
print(n_thdib)#检查
#显示数字标签 ha代表对齐方式
for a,b in zip(bins_thdib,n_thdib):
    plt.text(a,b + 2,'%.1f%%'%(b/freq*100),ha='left', va= 'bottom',fontsize=6)

y_thdib = stats.norm.pdf(bins_thdib, mu[10], sigma[10])
norm_thdib = plt.plot(bins_thdib, y_thdib*freq*2, 'g--',label='norm')

plt.legend(fontsize=6,loc='upper right')
plt.xlabel('THD_Ib',fontsize=9)
plt.ylabel('Frequency',fontsize=9)
plt.setp(ax_thdib.get_yticklabels(),visible=False)

###############Ic_THD##############
ax_thdic  = plt.subplot(133,sharey=ax_thdia)
n_thdic, bins_thdic, patches_thdic = plt.hist(df.Ic_THD,bins=13,alpha=0.6,\
                                  rwidth=0.9,color='orangered',\
                                  label='Probability',density=False)
print(n_thdic)#检查
#显示数字标签 ha代表对齐方式
for a,b in zip(bins_thdic,n_thdic):
    plt.text(a,b + 2,'%.1f%%'%(b/freq*100),ha='left', va= 'bottom',fontsize=6)
#拟合Ia
y_thdic = stats.norm.pdf(bins_thdic, mu[11], sigma[11])
norm_thdic = plt.plot(bins_thdic, y_thdic*freq*2, 'r--',label='norm')
#print(y_Ia)
plt.legend(fontsize=6,loc='upper right')
plt.xlabel('THD_Ic',fontsize=9)
plt.ylabel('Frequency',fontsize=9)
plt.setp(ax_thdic.get_yticklabels(),visible=False)

plt.suptitle('A、B、C三相谐波电流概率分布图')
fig4.tight_layout(pad=2.3)

plt.show()
