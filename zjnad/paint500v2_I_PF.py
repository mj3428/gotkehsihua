#!/usr/bin/env python
# encoding: utf-8
'''
@author: mj
@contact: major3428@foxmail.com
@software: pycharm
@file: paint500v2_I_PF.py
@time: 2018-12-25 上午 9:23
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
df = pd.read_csv('./data/huabang2_Nov.csv',index_col=0)
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
                   },inplace = True)

#print(np.max([df.Ua_THD, df.Ub_THD, df.Uc_THD], axis=1))
mu = np.mean([df.Ia, df.Ib, df.Ic, df.PF], axis=1)
print(mu)
#mu = np.mean(df.Ua)
sigma = np.std([df.Ia, df.Ib, df.Ic, df.PF], axis=1)
freq = len(df.ds) #总样本频次
print(freq)
#QR = np.array([len(df.query('Ua_THD < 5')),len(df.query('Ub_THD < 5')),len(df.query('Uc_THD < 5'))])/freq
#UR = 1-QR
#print(QR)
#print(UR)

#设置字体
mpl.rcParams['font.sans-serif'] = ['Microsoft Yahei']
mpl.rcParams['font.family']='sans-serif'#解决负号'-'显示为方块的问题
mpl.rcParams['axes.unicode_minus'] = False

#需要的变量
gama = 0.90
beta = 0.85
qr = np.array([len(df.query('Ia < 2886.8')), len(df.query('Ib < 2886.8')), len(df.query('Ic < 2886.8'))]) / freq
ur = 1 - qr
quality = len(df.query('PF >= 0.9')) / freq
unquality = 1 - quality
values = [[qr[0], ur[0]], [qr[1], ur[1]], [qr[2], ur[2]]]
labels = ['合格率 %.1f%%' % (quality * 100), '不合格率 %.1f%%' % (unquality * 100)]
vals = [quality, unquality]
#颜色方案
color_kinds = [['orange', 'goldenrod', ['khaki', 'goldenrod']],
               ['mediumseagreen', 'green', ['mediumseagreen', 'green']],
               ['orangered', 'red', ['lightcoral', 'orangered']]]

#面向对象
class Paint:
    def __init__(self):
        self.pos = 'upper right'

    def paintI(self, electricity, phase, num):
        '''
        画电流
        :param electricity:电流的数组，格式为Series
        :param phase: 三相电，填字母，带上引号
        :param num: A相填0,B相填1,C相填2
        :return:
        '''
        # 建画布
        fig = plt.figure(figsize=[10.5, 3.55], dpi=150, facecolor='gainsboro')
        #ax_ia = plt.subplot(131)
        plt.subplot2grid((1, 3), (0, 0), colspan=2)
        n_I, bins_I, patches_I = plt.hist(electricity, bins=17, alpha=0.6, rwidth=0.9, color=color_kinds[num][0],
                                             label='概率', density=False)
        # 显示数字标签 ha代表对齐方式
        for a, b in zip(bins_I, n_I):
            plt.text(a, b + 2, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)
        # 拟合I
        y_I = stats.norm.pdf(bins_I, mu[num], sigma[num])

        alpha = np.max(n_I, axis=0) / np.max(y_I, axis=0) * beta

        norm_I = plt.plot(bins_I, y_I * alpha, color=color_kinds[num][1], linestyle='--', label='正态曲线')

        plt.legend(fontsize=6, loc=self.pos)
        plt.xlabel(phase+'相电流(单位:A)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        #plt.setp(ax_ia.get_yticklabels(), fontsize=9)
        #画环形
        plt.subplot2grid((1, 3), (0, 2))
        wedges1, texts1, autotexts1 = plt.pie(values[num], autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=color_kinds[num][2], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'}
                                              )
        plt.legend(wedges1, labels=['合格率 %.1f%%' % (qr[num] * 100), '不合格率 %.1f%%' % (ur[num] * 100)], fontsize=7,
                   title=phase+'相电流', loc='center')
        plt.title(phase+'相电流合格率', fontsize=10)
        #plt.suptitle(phase+'相电流')
        fig.set_tight_layout(True)
        plt.show()

    def painPF(self, electricity):
        '''
        画功率因数
        :param electricity:
        :return:
        '''
        fig1 = plt.figure(figsize=[10.5, 3.55], dpi=150, facecolor='gainsboro')
        plt.subplot2grid((1, 3), (0, 0), colspan=2)

        n_pf, bins_pf, patches_pf = plt.hist(electricity, bins=20, alpha=0.6,
                                             rwidth=0.9, label='概率', density=False)

        #length_pf = plt.xlim()
        #width_pf = (length_pf[1] - length_pf[0]) / (len(bins_pf) - 1)
        #print(n_pf, length_pf, width_pf, np.sum(n_pf))#检查
        for a, b in zip(bins_pf, n_pf):
            plt.text(a, b + 0.0025, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)

        y_pf = stats.norm.pdf(bins_pf, mu[3], sigma[3])

        alpha = np.max(n_pf, axis=0) / np.max(y_pf, axis=0) * beta

        norm_pf = plt.plot(bins_pf, y_pf * alpha, color='mediumturquoise', linestyle='--', label='正态曲线')

        # plt.text(0.971, 125, '国标 0.9',fontsize=8)
        plt.vlines(0.9, 0, np.max(n_pf, axis=0) * gama, colors='mediumturquoise', linestyles='-.', label='国标 0.9')
        plt.legend(fontsize=9, loc=self.pos)
        # arr = np.arange(0, 1.1, 0.1)
        # plt.xticks(arr)
        plt.xlabel('功率因数', fontsize=8)
        plt.ylabel('发生次数', fontsize=9)
        plt.title('总功率因数分布图', fontsize=10, loc='left')

        plt.subplot2grid((1, 3), (0, 2))
        wedges2, texts2, autotexts2 = plt.pie(vals, autopct="%.1f%%", radius=1, pctdistance=0.85,
                                           colors=['cornflowerblue', 'lavender'], textprops={'color': 'w'},
                                           startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'}
                                           )
        plt.legend(wedges2, labels, fontsize=8, loc='center')
        plt.title('功率因数合格及不合格情况', fontsize=10)
        #plt.suptitle('总功率因数情况一览')
        fig1.set_tight_layout(True)
        plt.show()

p = Paint()#实例化
p.paintI(df.Ib, 'B', 1)
#plt.savefig('./pic/Power_Factor.png')
#p.pos = 'upper left'
#p.painPF(df.PF)
#plt.savefig('./pic/Power_Factor.png')

