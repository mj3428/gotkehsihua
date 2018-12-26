#!/usr/bin/env python
# encoding: utf-8
'''
@author: mj
@contact: major3428@foxmail.com
@software: pycharm
@file: paint500v2_LF_Unb.py
@time: 2018-12-25 下午 3:00
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
df = pd.read_csv('./data/xinbang_Nov.csv',index_col=0)
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


#设置字体
mpl.rcParams['font.sans-serif'] = ['Microsoft Yahei']
mpl.rcParams['font.family']='sans-serif'#解决负号'-'显示为方块的问题
mpl.rcParams['axes.unicode_minus'] = False


def jungle(a):
    if a['I_ave'] == 0:
        return 0
    else:
        value = max(abs(a['Ia'] - a['I_ave']), abs(a['Ib'] - a['I_ave']), abs(a['Ic'] - a['I_ave'])) / a['I_ave']
        return value
#检查次数
freq = len(df.ds)
#print(freq)

#变压器容量
KVA = 2000000

df['I_ave'] = (df.Ia + df.Ib + df.Ic)/3
df['U_ave'] = (df.Ua + df.Ub + df.Uc)/3
#print(df.P.head(12),df.Q.head(12))
df['LF'] = np.sqrt(pow(df.P,2)+pow(df.Q,2))/KVA*100
#print(df.U_ave.head(12))
df['I_UP'] = df.apply(lambda x :jungle(x),axis=1)*100
#print(df.I_UP.head(12))
mu = np.mean([df.LF, df.I_UP], axis=1)
sigma = np.std([df.LF, df.I_UP], axis=1)
#print(mu[1])
#print(df.LF.max(),df.LF.min())
#df8 = df.query('LF > 48.3')
#print(df8.ds)

#负荷率判断
QR = len(df.query('LF <= 40'))/freq
GZ1 = len(df.query('LF > 100 and LF <= 110'))/freq
GZ2 = len(df.query('LF > 110 and LF <= 150'))/freq
US = 1 - QR - GZ1 - GZ2

beta = 0.85
gama = 0.90

values = [[QR, GZ1, US],
          [QR, GZ1, GZ2, US]]

labels = [['轻载 %.1f%%'%(QR*100), '1级过载 %.1f%%'%(GZ1*100), '正常 %.1f%%'%(US*100)],
          ['轻载 %.1f%%'%(QR*100), '1级过载 %.1f%%'%(GZ1*100), '2级过载 %.1f%%'%(GZ2*100), '正常 %.1f%%'%(US*100)]]

quality = len(df.query('I_UP <= 15.0'))/freq
unquality = 1 - quality
vals = [quality, unquality]
labs = ['合格率 %.1f%%'%(quality*100), '不合格率 %.1f%%'%(unquality*100)]
#颜色配方
color_kinds = [['cornflowerblue', 'paleturquoise', 'lavender'],
               ['cornflowerblue', 'paleturquoise', 'lavender', 'mediumpurple']]

class Paint:
    def __init__(self):
        self.pos = 'upper right'

    def paintLF(self, electricity, num):
        '''
        画负荷率
        :param electricity: 输入LF的数组，类型为Series
        :param num: 无二级过载填0，有二级过载填1
        :return:
        '''
        fig1 = plt.figure(figsize=[10.5, 3.55], dpi=150, facecolor='gainsboro')
        plt.subplot2grid((1, 3), (0, 0), colspan=2)
        n_lf, bins_lf, patches_lf = plt.hist(electricity, bins=25, alpha=0.6, rwidth=0.9,
                                             label='概率', density=False)
        #print(n_lf)
        #length_lf = plt.xlim()
        #width_lf = (length_lf[1] - length_lf[0]) / (len(bins_lf) - 1)
        #print(n_lf, length_lf, width_lf, np.sum(n_lf))

        for a, b in zip(bins_lf, n_lf):
            plt.text(a, b + 0.25, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)
        y_lf = stats.norm.pdf(bins_lf, mu[0], sigma[0])

        alpha = np.max(n_lf, axis=0) / np.max(y_lf, axis=0) * beta

        norm_lf = plt.plot(bins_lf, y_lf * alpha, color='mediumturquoise', linestyle='--', label='正态曲线')
        #plt.text(68, 410, '国标参考上限 85%', fontsize=8)
        if np.max(electricity, axis=0) > 85:
            plt.vlines(85, 0, np.max(n_lf, axis=0) * gama, colors='mediumturquoise', linestyles='-.', label='国标 85%')
        plt.legend(fontsize=10, loc=self.pos)
        plt.xlabel('负荷率(单位:%)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        plt.title('负荷率分布图', fontsize=10, loc='left')

        plt.subplot2grid((1, 3), (0, 2))
        wedges1, texts1, autotexts1 = plt.pie(values[num], autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=color_kinds[num], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'}
                                              )  # 保留2级过载的颜色 'mediumpurple'
        plt.legend(wedges1, labels[num], fontsize=7, title='负载级别', loc='center')
        plt.title('负载情况', fontsize=10)
        plt.suptitle('负荷率分布情况')
        fig1.set_tight_layout(True)
        plt.show()

    def paintUnb(self, electricity):
        '''
        画不平衡度
        :param electricity: 输入df.I_UP
        :return:
        '''
        fig2 = plt.figure(figsize=[10.5, 3.55], dpi=150, facecolor='gainsboro')
        plt.subplot2grid((1, 3), (0, 0), colspan=2)

        n_iup, bins_iup, patches_iup = plt.hist(electricity, bins=25, alpha=0.6,
                                                rwidth=0.9, label='概率', density=False)

        #length_iup = plt.xlim()
        #width_iup = (length_iup[1] - length_iup[0]) / (len(bins_iup) - 1)
        #print(n_iup, length_iup, width_iup, np.sum(n_iup))
        for a, b in zip(bins_iup, n_iup):
            plt.text(a, b + 0.0025, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)
        y_iup = stats.norm.pdf(bins_iup, mu[1], sigma[1])

        alpha = np.max(n_iup, axis=0) / np.max(y_iup, axis=0) * beta

        norm_iup = plt.plot(bins_iup, y_iup * alpha, color='mediumturquoise', linestyle='--', label='正态曲线')

        # plt.text(0.48, 12.8, '合格率=%.1f%%\n不合格率=%.1f%%'%(quality*100,unquality*100), fontsize=8)
        # plt.text(3.45, 136, '国标参考上限 15%', fontsize=8)
        if np.max(electricity, axis=0) > 15:
            plt.vlines(15, 0, np.max(n_iup,axis=0) * gama, colors='mediumturquoise', linestyles='-.', label='国标 15%')
        plt.legend(fontsize=10, loc=self.pos)
        plt.xlabel('三相电流不平度(单位:%)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        plt.title('三相电流不平衡分布图', fontsize=10, loc='left')

        plt.subplot2grid((1, 3), (0, 2))
        wedges2, texts2, autotexts2 = plt.pie(vals, autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=['cornflowerblue', 'lavender'], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'},
                                              )
        plt.legend(wedges2, labs, fontsize=8, loc='center')
        plt.title('三相不平衡合格及不合格情况', fontsize=10)
        plt.suptitle('三相电流不平衡分布情况')
        fig2.set_tight_layout(True)
        plt.show()

p = Paint()
#p.paintLF(df.LF, 0)
p.paintUnb(df.I_UP)
