#!/usr/bin/env python
# encoding: utf-8
'''
@author: miaojue
@contact: major3428@foxmail.com
@software: pycharm
@file: paint500v2_harmonic.py
@time: 2018-12-26 下午 1:03
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

#读取
df = pd.read_csv('./data/jmrz_Dec.csv',index_col=0)
#index_col=0去掉索引
#更名
df.rename(columns={'采集时间': 'ds', 'A相电流': 'Ia', 'B相电流': 'Ib', 'C相电流': 'Ic',
                   'A相电流THD': 'Ia_THD', 'B相电流THD': 'Ib_THD', 'C相电流THD': 'Ic_THD',
                   'A相电压': 'Ua', 'B相电压': 'Ub', 'C相电压': 'Uc',
                   'A相电压THD': 'Ua_THD', 'B相电压THD': 'Ub_THD', 'C相电压THD': 'Uc_THD',
                   '总功率因数': 'PF', '三相无功功率': 'Q', '三相有功功率': 'P',
                   'A相电流H3': 'Ia_H3', 'A相电流H5': 'Ia_H5', 'A相电流H7': 'Ia_H7',
                   'A相电流H9': 'Ia_H9', 'A相电流H11': 'Ia_H11', 'A相电流H13': 'Ia_H13',
                   'A相电流H15': 'Ia_H15', 'A相电流H17': 'Ia_H17', 'A相电流H19': 'Ia_H19',
                   'A相电流H21': 'Ia_H21',
                   'B相电流H3': 'Ib_H3', 'B相电流H5': 'Ib_H5', 'B相电流H7': 'Ib_H7',
                   'B相电流H9': 'Ib_H9', 'B相电流H11': 'Ib_H11', 'B相电流H13': 'Ib_H13',
                   'B相电流H15': 'Ib_H15', 'B相电流H17': 'Ib_H17', 'B相电流H19': 'Ib_H19',
                   'B相电流H21': 'Ib_H21',
                   'C相电流H3': 'Ic_H3', 'C相电流H5': 'Ic_H5', 'C相电流H7': 'Ic_H7',
                   'C相电流H9': 'Ic_H9', 'C相电流H11': 'Ic_H11', 'C相电流H13': 'Ic_H13',
                   'C相电流H15': 'Ic_H15', 'C相电流H17': 'Ic_H17', 'C相电流H19': 'Ic_H19',
                   'C相电流H21': 'Ic_H21'
                   }, inplace = True)
freq = len(df.ds) #总样本频次

max_values = np.array([[df.Ia_H3.max(), df.Ia_H5.max(), df.Ia_H7.max(), df.Ia_H9.max(),
                       df.Ia_H11.max(), df.Ia_H13.max(), df.Ia_H15.max(), df.Ia_H17.max(),
                       df.Ia_H19.max(), df.Ia_H21.max()],
                      [df.Ib_H3.max(), df.Ib_H5.max(), df.Ib_H7.max(), df.Ib_H9.max(),
                       df.Ib_H11.max(), df.Ib_H13.max(), df.Ib_H15.max(), df.Ib_H17.max(),
                       df.Ib_H19.max(), df.Ib_H21.max()],
                      [df.Ic_H3.max(), df.Ic_H5.max(), df.Ic_H7.max(), df.Ic_H9.max(),
                       df.Ic_H11.max(), df.Ic_H13.max(), df.Ic_H15.max(), df.Ic_H17.max(),
                       df.Ic_H19.max(), df.Ic_H21.max()]])

A1 = df.Ia
df['iam3'], df['iam5'], df['iam7'], df['iam9'] = A1*df.Ia_H3/100, A1*df.Ia_H5/100, A1*df.Ia_H7/100,A1*df.Ia_H9/100
df['iam11'], df['iam13'], df['iam15'] = A1*df.Ia_H11/100, A1*df.Ia_H13/100, A1*df.Ia_H15/100
df['iam17'], df['iam19'], df['iam21'] = A1*df.Ia_H17/100, A1*df.Ia_H19/100, A1*df.Ia_H21/100
A2 = df.Ib
df['ibm3'], df['ibm5'], df['ibm7'], df['ibm9'] = A2*df.Ib_H3/100,A2*df.Ib_H5/100,A2*df.Ib_H7/100,A2*df.Ib_H9/100
df['ibm11'], df['ibm13'], df['ibm15'] = A2*df.Ib_H11/100,A2*df.Ib_H13/100,A2*df.Ib_H15/100
df['ibm17'], df['ibm19'], df['ibm21'] = A2*df.Ib_H17/100,A2*df.Ib_H19/100,A2*df.Ib_H21/100
A3 = df.Ic
df['icm3'], df['icm5'], df['icm7'],df['icm9'] = A3*df.Ic_H3/100, A3*df.Ic_H5/100, A3*df.Ic_H7/100, A3*df.Ic_H9/100
df['icm11'], df['icm13'], df['icm15'] = A3*df.Ic_H11/100, A3*df.Ic_H13/100, A3*df.Ic_H15/100
df['icm17'], df['icm19'], df['icm21'] = A3*df.Ic_H17/100, A3*df.Ic_H19/100, A3*df.Ic_H21/100

#最大值
max_A = np.max([df.iam3, df.iam5, df.iam7, df.iam9, df.iam11, df.iam13, df.iam15, df.iam17, df.iam19, df.iam21],axis=1)
max_B = np.max([df.ibm3, df.ibm5, df.ibm7, df.ibm9, df.ibm11, df.ibm13, df.ibm15, df.ibm17, df.ibm19, df.ibm21],axis=1)
max_C = np.max([df.icm3, df.icm5, df.icm7, df.icm9, df.icm11, df.icm13, df.icm15, df.icm17, df.icm19, df.icm21],axis=1)

#均值
mean_A = np.mean([df.iam3, df.iam5, df.iam7, df.iam9, df.iam11, df.iam13, df.iam15, df.iam17, df.iam19, df.iam21],axis=1)
mean_B = np.mean([df.ibm3, df.ibm5, df.ibm7, df.ibm9, df.ibm11, df.ibm13, df.ibm15, df.ibm17, df.ibm19, df.ibm21],axis=1)
mean_C = np.mean([df.icm3, df.icm5, df.icm7, df.icm9, df.icm11, df.icm13, df.icm15, df.icm17, df.icm19, df.icm21],axis=1)

#设置字体
mpl.rcParams['font.sans-serif'] = ['Microsoft Yahei']
mpl.rcParams['font.family']= 'sans-serif'#解决负号'-'显示为方块的问题
mpl.rcParams['axes.unicode_minus'] = False

Y = [max_A, max_B, max_C]
Z = [mean_A, mean_B, mean_C]
rank = [0, 1, 2]
color_kinds = ['gold', 'mediumaquamarine', 'lightcoral']
phase = ['A', 'B', 'C']
distance = 0.42
ithdlist = np.array([[len(df.query('iam3<=62')), len(df.query('iam5<=62')), len(df.query('iam7<=44')),
                     len(df.query('iam9<=21')), len(df.query('iam11<=28')), len(df.query('iam13<=24')),
                     len(df.query('iam15<=12')), len(df.query('iam17<=18')), len(df.query('iam19<=16')),
                     len(df.query('iam21<=8.9'))],
                    [len(df.query('ibm3<=62')), len(df.query('ibm5<=62')), len(df.query('ibm7<=44')),
                     len(df.query('ibm9<=21')), len(df.query('ibm11<=28')), len(df.query('ibm13<=24')),
                     len(df.query('ibm15<=12')), len(df.query('ibm17<=18')), len(df.query('ibm19<=16')),
                     len(df.query('ibm21<=8.9'))],
                     [len(df.query('icm3<=62')), len(df.query('icm5<=62')),len(df.query('icm7<=44')),
                      len(df.query('icm9<=21')), len(df.query('icm11<=28')),len(df.query('icm13<=24')),
                      len(df.query('icm15<=12')), len(df.query('icm17<=18')) ,len(df.query('icm19<=16')),
                      len(df.query('icm21<=8.9'))]])
ithdqr = ithdlist / freq * 100
#print(ithdqr)
X = np.arange(3,22,2)
Na = ['3rd', '5th', '7th', '9th', '11th', '13th', '15th', '17th', '19th', '21th']
class Paint:
    def __init__(self,args):
        '''
        :param args:最大值为Y 均值为Z 合格率为ithdqr
        '''
        self.args = args

    def paintMax(self):
        fig1 = plt.figure(figsize=[9, 4], dpi=200, facecolor='gainsboro')
        sum = 0
        for i in rank:
            plt.bar(X + sum, self.args[i], width=0.4, facecolor=color_kinds[i], edgecolor='white', label=phase[i]+'相分次谐波', alpha=0.84)

            for a, b in zip(X + sum, self.args[i]):
                plt.text(a, b + 0.1, '%.1f' % b, ha='center', va='bottom', fontsize=4.8)

            sum += distance
        plt.legend()
        plt.grid(alpha=0.618, linestyle='-.') #画网格
        plt.xticks(X, Na)
        plt.title('电流分次谐波(最大值)')
        plt.xlabel('谐波次级')
        plt.ylabel('谐波电流值(单位:A)')
        fig1.tight_layout()
        ax1 = plt.gca()
        ax1.patch.set_facecolor('lightcyan')  # 设置ax1区域背景颜色
        ax1.patch.set_alpha(0.5)
        plt.show()

    def paintMean(self):
        fig2 = plt.figure(figsize=[9, 4], dpi=200, facecolor='gainsboro')
        sum = 0
        for i in rank:
            plt.bar(X + sum, self.args[i], width=0.4, facecolor=color_kinds[i], edgecolor='white',
                    label=phase[i] + '相分次谐波', alpha=0.84)

            for a, b in zip(X + sum, self.args[i]):
                plt.text(a, b + 0.1, '%.1f' % b, ha='center', va='bottom', fontsize=4.8)

            sum += distance
        plt.legend()
        plt.grid(alpha=0.618, linestyle='-.') #画网格
        plt.xticks(X, Na)
        plt.title('电流分次谐波(均值)')
        plt.xlabel('谐波次级')
        plt.ylabel('谐波电流值(单位:A)')
        ax2 = plt.gca()
        ax2.patch.set_facecolor('lightcyan')  #设置ax1区域背景颜色
        ax2.patch.set_alpha(0.5)
        fig2.tight_layout()
        plt.show()

    def paintQR(self):
        fig3 = plt.figure(figsize=[9, 4], dpi=200, facecolor='gainsboro')
        sum = 0
        for i in rank:
            plt.bar(X + sum, self.args[i], width=0.4, facecolor=color_kinds[i], edgecolor='white',
                    label=phase[i] + '相分次谐波', alpha=0.84)

            for a, b in zip(X + sum, self.args[i]):
                plt.text(a, b + 0.1, '%.1f' % b, ha='center', va='bottom', fontsize=4.8)

            sum += distance
        plt.legend()
        plt.grid(alpha=0.618, linestyle='-.') #画网格
        plt.xticks(X, Na)
        plt.title('电流分次谐波合格率')
        plt.xlabel('谐波次级')
        plt.ylabel('谐波电流值(单位:A)')
        ax3 = plt.gca()
        ax3.patch.set_facecolor('lightcyan')  #设置ax1区域背景颜色
        ax3.patch.set_alpha(0.5)
        fig3.tight_layout()
        plt.show()

p = Paint(ithdqr)
p.paintQR()
#p.paintMax()
