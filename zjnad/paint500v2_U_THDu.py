#!/usr/bin/env python
# encoding: utf-8
'''
@author: mj
@contact: major3428@foxmail.com
@software: pycharm
@file: paint500v2_U_THDu.py
@time: 2018-12-26 上午 9:33
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

print(np.max([df.Ua_THD, df.Ub_THD, df.Uc_THD], axis=1))
mu = np.mean([df.Ua, df.Ub, df.Uc,
              df.Ua_THD, df.Ub_THD, df.Uc_THD], axis=1)
#mu = np.mean(df.Ua)
sigma = np.std([df.Ua, df.Ub, df.Uc,
                df.Ua_THD, df.Ub_THD, df.Uc_THD], axis=1)
freq = len(df.ds) #总样本频次
#print(freq)

#设置字体
mpl.rcParams['font.sans-serif'] = ['Microsoft Yahei']
mpl.rcParams['font.family']='sans-serif'#解决负号'-'显示为方块的问题
mpl.rcParams['axes.unicode_minus'] = False

#配置参数
gama = 0.90
beta = 0.85
QR = np.array([len(df.query('Ua_THD < 5')),len(df.query('Ub_THD < 5')),len(df.query('Uc_THD < 5'))])/freq
UR = 1-QR
qur = np.array([len(df.query('Ua < 235')), len(df.query('Ub < 235')), len(df.query('Uc < 235'))])/freq
unr = 1 - qur
values = [[qur[0], unr[0]], [qur[1], unr[1]], [qur[2], unr[2]]]
UTHDQR = np.array([len(df.query('Ua_THD < 5')), len(df.query('Ub_THD < 5')), len(df.query('Uc_THD < 5'))])/freq
UTHDUR = 1 - UTHDQR
vals = [[UTHDQR[0], UTHDUR[0]], [UTHDQR[1], UTHDUR[1]], [UTHDQR[2], UTHDUR[2]]]

#配置颜色
color_kinds = [['orange', 'goldenrod', ['khaki', 'goldenrod'], 'darkorange'],
               ['mediumseagreen', 'green', ['mediumseagreen', 'green'], 'lightseagreen'],
               ['orangered', 'red', ['lightcoral', 'orangered']], 'lightcoral']

thd_color = [['orange', 'darkorange', ['khaki', 'goldenrod']],
             ['mediumseagreen', 'lightseagreen', ['mediumseagreen', 'green']],
             ['orangered', 'lightcoral', ['lightcoral', 'orangered']]]

#面向对象
class Paint:
    def __init__(self):
        self.pos = 'upper left'

    def paintU(self, electricity, phase, num):
        '''
        画电压
        :param electricity: 电压数组
        :param phase: 相
        :param num: A:0 B:1 C:2
        :return:
        '''
        # 画布大小 长 宽 dpi分辨率 facecolor背景颜色
        fig1 = plt.figure(figsize=[10.5, 3.55], dpi=150, facecolor='gainsboro')
        plt.subplot2grid((1, 3), (0, 0), colspan=2)
        n_u, bins_u, patches_u = plt.hist(electricity, bins=17, alpha=0.6, rwidth=0.9, color=color_kinds[num][0],
                                          label='概率', density=False)

        # 显示数字标签 ha代表对齐方式
        for a, b in zip(bins_u, n_u):
            plt.text(a, b + 2, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)
        # 拟合U
        y_u = stats.norm.pdf(bins_u, mu[num], sigma[num])

        alpha = np.max(n_u, axis=0) / np.max(y_u, axis=0) * beta

        norm_u = plt.plot(bins_u, y_u * alpha, color=color_kinds[num][1], linestyle='--', label='正态曲线')
        # 画参考线
        if np.max(electricity, axis=0) > 235:
            plt.vlines(235, 0, np.max(n_u, axis=0) * gama, colors=color_kinds[num][3], linestyles='-.', label='国标上限 235V')

        plt.legend(fontsize=6, loc=self.pos)
        plt.xlabel(phase+'相电压(单位:V)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        #plt.title(phase+'相电压', fontsize=10)

        plt.subplot2grid((1, 3), (0, 2))
        wedges1, texts1, autotexts1 = plt.pie(values[num], autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=color_kinds[num][2], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'},
                                              )
        plt.legend(wedges1, labels=['合格率 %.1f%%' % (qur[num] * 100), '不合格率 %.1f%%' % (unr[num] * 100)], fontsize=7,
                   title=phase+'相电压', loc='center')
        fig1.set_tight_layout(True)
        plt.show()

    def paintTHDu(self, electricity, phase, num):
        fig2 = plt.figure(figsize=[10.5, 3.55], dpi=150, facecolor='gainsboro')
        plt.subplot2grid((1, 3), (0, 0), colspan=2)
        n_thdu, bins_thdu, patches_thdu = plt.hist(electricity, bins=17, alpha=0.6, rwidth=0.9, color=thd_color[num][0],
                                                      label='概率', density=False)
        print(n_thdu)  # 检查

        # 显示数字标签 ha代表对齐方式
        for a, b in zip(bins_thdu, n_thdu):
            plt.text(a, b + 2, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)

        if np.max(electricity, axis=0) > 5:
            plt.vlines(5, 0, np.max(n_thdu, axis=0), colors=thd_color[num][1], linestyles='-.', label='上限 5%')

        plt.legend(fontsize=6, loc=self.pos)
        plt.xlabel(phase+'相电压THD(单位:%)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)

        plt.subplot2grid((1, 3), (0, 2))
        wedges2, texts2, autotexts2 = plt.pie(vals[num], autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=thd_color[num][2], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'}
                                              )
        plt.legend(wedges2, labels=['合格率 %.1f%%' % (UTHDQR[num] * 100), '不合格率 %.1f%%' % (UTHDUR[num] * 100)], fontsize=7,
                   title=phase+'相电压谐波含有率', loc='center')
        #plt.title(phase+'相谐波电压含有率合格率', fontsize=9)
        fig2.set_tight_layout(True)
        plt.show()
p = Paint()
#p.paintU(df.Ub, 'B', 1)
#p.paintTHDu(df.Ub_THD, 'B', 1)
