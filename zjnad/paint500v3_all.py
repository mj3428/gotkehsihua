#!/usr/bin/env python
# encoding: utf-8
'''
@author: miaoj
@contact: major3428@foxmail.com
@software: pycharm
@file: paint500v3_all.py
@time: 2019-1-14 上午 10:30
@desc:
'''


import matplotlib as mpl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


#读取
df = pd.read_csv('./data/jmrz_semi.csv', encoding='gbk', index_col=None)
#index_col=0去掉索引
#更名
df.rename(columns={'采集时间': 'ds', 'A相电流': 'Ia', 'B相电流': 'Ib', 'C相电流': 'Ic',
                   'A相电流THD': 'Ia_THD', 'B相电流THD': 'Ib_THD', 'C相电流THD': 'Ic_THD',
                   'A相电压': 'Ua', 'B相电压': 'Ub', 'C相电压': 'Uc',
                   'A相电压THD': 'Ua_THD', 'B相电压THD': 'Ub_THD', 'C相电压THD': 'Uc_THD',
                   '总功率因数': 'PF', '三相无功功率': 'Q', '三相有功功率': 'P',
                   'A相有功功率': 'Pa', 'B相有功功率': 'Pb', 'C相有功功率': 'Pc',
                   'A相无功功率': 'Qa', 'B相无功功率': 'Qb', 'C相无功功率': 'Qc',
                   'A相功率因数': 'PFa', 'B相功率因数': 'PFb', 'C相功率因数': 'PFc',
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

freq = len(df.ds) #总样本频次

#判断不平衡
def jungle(a):
    if a['I_ave'] == 0:
        return 0
    else:
        value = max(abs(a['Ia'] - a['I_ave']), abs(a['Ib'] - a['I_ave']), abs(a['Ic'] - a['I_ave'])) / a['I_ave']
        return value

#清洗数据
for i in df.columns:
    if df[i].isnull().any() == True:
        df[i].fillna(df[i].mean(),inplace=True)

#需要的变量
KVA = 1600000 #变压器容量大小
ele_n = KVA * 1.4434 / 1000#额定电流
df['PF'] = df['PF'].apply(lambda x:abs(x))
df['I_ave'] = (df.Ia + df.Ib + df.Ic) / 3
df['U_ave'] = (df.Ua + df.Ub + df.Uc) / 3
df['LF'] = np.sqrt(pow(df.P, 2) + pow(df.Q, 2)) / KVA * 100
df['I_UP'] = df.apply(lambda x :jungle(x), axis=1) * 100

max_values = np.array([[df.Ia_H3.max(), df.Ia_H5.max(), df.Ia_H7.max(), df.Ia_H9.max(),
                       df.Ia_H11.max(), df.Ia_H13.max(), df.Ia_H15.max(), df.Ia_H17.max(),
                       df.Ia_H19.max(), df.Ia_H21.max()],
                      [df.Ib_H3.max(), df.Ib_H5.max(), df.Ib_H7.max(), df.Ib_H9.max(),
                       df.Ib_H11.max(), df.Ib_H13.max(), df.Ib_H15.max(), df.Ib_H17.max(),
                       df.Ib_H19.max(), df.Ib_H21.max()],
                      [df.Ic_H3.max(), df.Ic_H5.max(), df.Ic_H7.max(), df.Ic_H9.max(),
                       df.Ic_H11.max(), df.Ic_H13.max(), df.Ic_H15.max(), df.Ic_H17.max(),
                       df.Ic_H19.max(), df.Ic_H21.max()]])

mu = np.mean([df.Ia, df.Ib, df.Ic, df.PF,
              df.Ua, df.Ub, df.Uc,
              df.LF, df.I_UP], axis=1)
sigma = np.std([df.Ia, df.Ib, df.Ic, df.PF,
                df.Ua, df.Ub, df.Uc,
                df.LF, df.I_UP], axis=1)

#设置字体
mpl.rcParams['font.sans-serif'] = ['Microsoft Yahei']
mpl.rcParams['font.family'] = 'sans-serif'#解决负号'-'显示为方块的问题
mpl.rcParams['axes.unicode_minus'] = False

print(df.columns)

#合格率内容
qr_i = np.array([len(df.ix[df.Ia < ele_n]), len(df.ix[df.Ib < ele_n]), len(df.ix[df.Ic < ele_n])]) / freq
ur_i = 1 - qr_i
qr_u = np.array([len(df.query('Ua < 235')), len(df.query('Ub < 235')), len(df.query('Uc < 235'))]) / freq
ur_u = 1 - qr_u
qr_uthd = np.array([len(df.query('Ua_THD < 5')), len(df.query('Ub_THD < 5')), len(df.query('Uc_THD < 5'))]) / freq
ur_uthd = 1 - qr_uthd
qr_pf = len(df.query('PF >= 0.9')) / freq
ur_pf = 1 - qr_pf
qr_unb = len(df.query('I_UP <= 15.0')) / freq
ur_unb = 1 - qr_unb
qr_lf = len(df.query('LF <= 40')) / freq
gz_lf1 = len(df.query('LF > 100 and LF <= 110')) / freq
gz_lf2 = len(df.query('LF > 110 and LF <= 150')) / freq
ur_lf = 1 - qr_lf - gz_lf1 - gz_lf2
values_i = [[qr_i[0], ur_i[0]], [qr_i[1], ur_i[1]], [qr_i[2], ur_i[2]]]
values_u = [[qr_u[0], ur_u[0]], [qr_u[1], ur_u[1]], [qr_u[2], ur_u[2]]]
values_uthd = [[qr_uthd[0], ur_uthd[0]], [qr_uthd[1], ur_uthd[1]], [qr_uthd[2], ur_uthd[2]]]
labels_pf = ['合格率 %.1f%%' % (qr_pf * 100), '不合格率 %.1f%%' % (ur_pf * 100)]
values_pf = [qr_pf, ur_pf]
values_lf = {'GZ1':[qr_lf, gz_lf1, ur_lf],
             'GZ2':[qr_lf, gz_lf1, gz_lf2, ur_lf]}
labels_lf = {'GZ1': ['轻载 %.1f%%' % (qr_lf * 100), '1级过载 %.1f%%' % (gz_lf1 * 100), '正常 %.1f%%' % (ur_lf * 100)],
             'GZ2': ['轻载 %.1f%%' % (qr_lf * 100), '1级过载 %.1f%%' % (gz_lf1 * 100), '2级过载 %.1f%%' % (gz_lf2 * 100),
                    '正常 %.1f%%' %(ur_lf * 100)]}
values_unb = [qr_unb, ur_unb]
labels_unb = ['合格率 %.1f%%' % (qr_unb * 100), '不合格率 %.1f%%' % (ur_unb * 100)]


#谐波电流处理
A1 = df.Ia
df['iam3'], df['iam5'] = A1 * df.Ia_H3 / 100, A1 * df.Ia_H5 / 100
df['iam7'], df['iam9'] = A1 * df.Ia_H7 / 100, A1 * df.Ia_H9 / 100
df['iam11'], df['iam13'], df['iam15'] = A1 * df.Ia_H11 / 100, A1 * df.Ia_H13 / 100, A1 * df.Ia_H15 / 100
df['iam17'], df['iam19'], df['iam21'] = A1 * df.Ia_H17 / 100, A1 * df.Ia_H19 / 100, A1 * df.Ia_H21 / 100
A2 = df.Ib
df['ibm3'], df['ibm5'] = A2 * df.Ib_H3 / 100, A2 * df.Ib_H5 / 100
df['ibm7'], df['ibm9'] = A2 * df.Ib_H7 / 100, A2 * df.Ib_H9 / 100
df['ibm11'], df['ibm13'], df['ibm15'] = A2 * df.Ib_H11 / 100, A2 * df.Ib_H13 / 100, A2 * df.Ib_H15 / 100
df['ibm17'], df['ibm19'], df['ibm21'] = A2 * df.Ib_H17 / 100, A2 * df.Ib_H19 / 100, A2 * df.Ib_H21 / 100
A3 = df.Ic
df['icm3'], df['icm5'] = A3 * df.Ic_H3 / 100, A3 * df.Ic_H5 / 100
df['icm7'], df['icm9'] = A3 * df.Ic_H7 / 100, A3 * df.Ic_H9 / 100
df['icm11'], df['icm13'], df['icm15'] = A3 * df.Ic_H11 / 100, A3 * df.Ic_H13 / 100, A3 * df.Ic_H15 / 100
df['icm17'], df['icm19'], df['icm21'] = A3 * df.Ic_H17 / 100, A3 * df.Ic_H19 / 100, A3 * df.Ic_H21 / 100


print(df.isnull().any()) # 有缺失值
# 最大值
max_A = np.max([df.iam3, df.iam5, df.iam7, df.iam9, df.iam11, df.iam13, df.iam15, df.iam17, df.iam19, df.iam21],
               axis=1)
max_B = np.max([df.ibm3, df.ibm5, df.ibm7, df.ibm9, df.ibm11, df.ibm13, df.ibm15, df.ibm17, df.ibm19, df.ibm21],
               axis=1)
max_C = np.max([df.icm3, df.icm5, df.icm7, df.icm9, df.icm11, df.icm13, df.icm15, df.icm17, df.icm19, df.icm21],
               axis=1)

# 均值
mean_A = np.mean(
    [df.iam3, df.iam5, df.iam7, df.iam9, df.iam11, df.iam13, df.iam15, df.iam17, df.iam19, df.iam21], axis=1)
mean_B = np.mean(
    [df.ibm3, df.ibm5, df.ibm7, df.ibm9, df.ibm11, df.ibm13, df.ibm15, df.ibm17, df.ibm19, df.ibm21], axis=1)
mean_C = np.mean(
    [df.icm3, df.icm5, df.icm7, df.icm9, df.icm11, df.icm13, df.icm15, df.icm17, df.icm19, df.icm21], axis=1)

yyy = [max_A, max_B, max_C]
zzz = [mean_A, mean_B, mean_C]

rank = [0, 1, 2]
color_hv = ['gold', 'mediumaquamarine', 'lightcoral']
phase = ['A', 'B', 'C']
distance = 0.42
X = np.arange(3,22,2)
Na = ['3rd', '5th', '7th', '9th', '11th', '13th', '15th', '17th', '19th', '21th']
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
qr_ithd = ithdlist / freq * 100

#面向对象
class Paint:
    def __init__(self):
        self.gama = 0.90
        self.beta = 0.85 #曲线高度
        self.pos = 'upper right'
        self.path = './pic/'
        self.color_kinds = {'A0': 'orange', 'A1': 'goldenrod', 'A2': ['khaki', 'goldenrod'],
                            'B0': 'mediumseagreen', 'B1': 'green', 'B2': ['mediumseagreen', 'green'],
                            'C0': 'orangered', 'C1': 'red', 'C2': ['lightcoral', 'orangered'],
                            'GZ1':['cornflowerblue', 'paleturquoise', 'lavender'],
                            'GZ2':['cornflowerblue', 'paleturquoise', 'lavender', 'mediumpurple']}

    def paint_i(self, save=True):
        # 建画布
        fig = plt.figure(figsize=[10.5, 3.55], dpi=150, facecolor='gainsboro')
        #A相电流
        ax_ia = plt.subplot(131)
        n_ia, bins_ia, patches_ia = plt.hist(df.Ia, bins=13, alpha=0.6,
                                             rwidth=0.9, color=self.color_kinds['A0'],
                                             label='概率', density=False)
        for a, b in zip(bins_ia, n_ia):
            plt.text(a, b + 2, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)

        y_ia = stats.norm.pdf(bins_ia, mu[0], sigma[0])

        alpha = np.max(n_ia, axis=0) / np.max(y_ia, axis=0) * self.beta

        plt.plot(bins_ia, y_ia * alpha, color=self.color_kinds['A1'], linestyle='--', label='正态曲线')
        if np.max(df.Ia, axis=0) > (KVA * 1.44 / 1000):
            plt.vlines(KVA * 1.44 / 1000, 0, np.max(n_ia, axis=0) * self.gama,
                       colors=self.color_kinds['A1'], linestyles='-.', label='额定电流')
        plt.legend(fontsize=6, loc=self.pos)
        plt.xlabel('A相电流(单位:A)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        plt.setp(ax_ia.get_yticklabels(), fontsize=9)
        #B相电流
        ax_ib = plt.subplot(132, sharey=ax_ia)
        n_ib, bins_ib, patches_ib = plt.hist(df.Ib, bins=13, alpha=0.6,
                                             rwidth=0.9, color=self.color_kinds['B0'],
                                             label='概率', density=False)
        for a, b in zip(bins_ib, n_ib):
            plt.text(a, b + 2, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)

        y_ib = stats.norm.pdf(bins_ib, mu[1], sigma[1])

        alpha_b = np.max(n_ib, axis=0) / np.max(y_ib, axis=0) * self.beta
        plt.plot(bins_ib, y_ib * alpha_b, 'g--', label='正态曲线')
        if np.max(df.Ib,axis=0) > (KVA * 1.44 / 1000):
            plt.vlines(KVA * 1.44 / 1000, 0, np.max(n_ib, axis=0) * self.gama,
                       colors='green', linestyles='-.', label='额定电流')
        plt.legend(fontsize=6, loc=self.pos)
        plt.xlabel('B相电流(单位:A)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        plt.setp(ax_ib.get_yticklabels(), visible=False)
        #C相
        ax_ic = plt.subplot(133)
        n_ic, bins_ic, patches_ic = plt.hist(df.Ic, bins=13, alpha=0.6,
                                             rwidth=0.9, color=self.color_kinds['C0'],
                                             label='概率', density=False)
        for a, b in zip(bins_ic, n_ic):
            plt.text(a, b + 2, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)

        y_ic = stats.norm.pdf(bins_ic, mu[2], sigma[2])
        alpha_c = np.max(n_ic, axis=0) / np.max(y_ic, axis=0) * 0.85
        plt.plot(bins_ic, y_ic * alpha_c, 'r--', label='正态曲线')
        if np.max(df.Ic, axis=0) > (KVA * 1.44 / 1000):
            plt.vlines(KVA * 1.44 / 1000, 0, np.max(n_ic, axis=0) * self.gama,
                       colors='red', linestyles='-.', label='额定电流')
        plt.legend(fontsize=6, loc=self.pos)
        plt.xlabel('C相电流(单位：A)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        plt.setp(ax_ic.get_yticklabels(), visible=False)
        #总标题
        plt.suptitle('A、B、C三相电流概率分布图')
        fig.tight_layout(pad=1.8)
        if save == True:
            plt.savefig(self.path + 'I.png')
            plt.show()
            plt.close()
        return

    def paint_ipie(self, save=True):
        #建画布
        fig0 = plt.figure(figsize=[7.5, 2.5], dpi=150, facecolor='gainsboro')
        # 画A相电流环形图
        plt.subplot(131)
        wedges1, texts1, autotexts1 = plt.pie(values_i[0], autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=self.color_kinds['A2'], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'},
                                              )
        plt.legend(wedges1, labels=['合格率 %.1f%%' % (qr_i[0] * 100), '不合格率 %.1f%%' % (ur_i[0] * 100)], fontsize=7,
                   title='A相电流', loc='center')

        # 画B相电流环形图
        plt.subplot(132)
        wedges2, texts2, autotexts2 = plt.pie(values_i[1], autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=self.color_kinds['B2'], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'},
                                              )
        plt.legend(wedges2, labels=['合格率 %.1f%%' % (qr_i[1] * 100), '不合格率 %.1f%%' % (ur_i[1] * 100)], fontsize=7,
                   title='B相电流', loc='center')

        # 画C相电流环形图
        plt.subplot(133)
        wedges3, texts3, autotexts3 = plt.pie(values_i[2], autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=self.color_kinds['C2'], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'},
                                              )
        plt.legend(wedges3, labels=['合格率 %.1f%%' % (qr_i[2] * 100), '不合格率 %.1f%%' % (ur_i[2] * 100)], fontsize=7,
                   title='C相电流', loc='center')
        plt.suptitle('A、B、C三相电流合格率')
        fig0.set_tight_layout(True)
        if save == True:
            plt.savefig(self.path+'I_Pie.png')
            plt.show()
            plt.close()
        return

    def paint_pf(self, save=1):
        '''
        画功率因数
        :param electricity:
        :return:
        '''
        #建画布
        fig1 = plt.figure(figsize=[10.5, 3.55], dpi=150, facecolor='gainsboro')
        plt.subplot2grid((1, 3), (0, 0), colspan=2)

        n_pf, bins_pf, patches_pf = plt.hist(df.PF, bins=20, alpha=0.6,
                                             rwidth=0.9, label='概率', density=False)
        for a, b in zip(bins_pf, n_pf):
            plt.text(a, b + 0.0025, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)

        y_pf = stats.norm.pdf(bins_pf, mu[3], sigma[3])

        alpha = np.max(n_pf, axis=0) / np.max(y_pf, axis=0) * self.beta

        plt.plot(bins_pf, y_pf * alpha, color='mediumturquoise', linestyle='--', label='正态曲线')
        plt.vlines(0.9, 0, np.max(n_pf, axis=0) * self.gama, colors='mediumturquoise', linestyles='-.', label='国标 0.9')
        plt.legend(fontsize=9, loc=self.pos)

        plt.xlabel('功率因数', fontsize=8)
        plt.ylabel('发生次数', fontsize=9)
        plt.title('总功率因数分布图', fontsize=10, loc='left')

        plt.subplot2grid((1, 3), (0, 2))
        wedges2, texts2, autotexts2 = plt.pie(values_pf, autopct="%.1f%%", radius=1, pctdistance=0.85,
                                           colors=['cornflowerblue', 'lavender'], textprops={'color': 'w'},
                                           startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'}
                                           )
        plt.legend(wedges2, labels_pf, fontsize=8, loc='center')
        plt.title('功率因数合格率', fontsize=10)
        fig1.set_tight_layout(True)
        if save == True:
            plt.savefig(self.path+'PF.png')
            plt.show()
            plt.close()
        return

    def paint_u(self, save=True):
        #建画布
        fig2 = plt.figure(figsize=[10.5, 3.55], dpi=150, facecolor='gainsboro')
        #Ua
        ax_ua = plt.subplot(131)
        n_a, bins_a, patches_a = plt.hist(df.Ua, bins=16, alpha=0.6,
                                          rwidth=0.9, color=self.color_kinds['A0'], label='概率', density=False)
        for a, b in zip(bins_a, n_a):
            plt.text(a, b + 2, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)
        y_a = stats.norm.pdf(bins_a, mu[4], sigma[4])
        alpha = np.max(n_a, axis=0) / np.max(y_a, axis=0) * self.beta
        plt.plot(bins_a, y_a * alpha, color=self.color_kinds['A1'], linestyle='--', label='正态曲线')
        # 画参考线
        plt.vlines(235, 0, np.max(n_a, axis=0) * self.gama, colors=self.color_kinds['A1'], linestyles='-.',
                   label='国标上限 235V')
        plt.legend(fontsize=6, loc=self.pos)
        plt.xlabel('A相电压(单位:V)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        plt.setp(ax_ua.get_yticklabels(), fontsize=9)
        #Ub
        ax_ub = plt.subplot(132, sharey=ax_ua)
        n_b, bins_b, patches_b = plt.hist(df.Ub, bins=16, alpha=0.6,
                                          rwidth=0.9, color=self.color_kinds['B0'],
                                          label='概率', density=False)  # 这里norm用来拟合正态分布
        for a, b in zip(bins_b, n_b):
            plt.text(a, b + 2, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)
        y_b = stats.norm.pdf(bins_b, mu[5], sigma[5])
        alpha_b = np.max(n_b, axis=0) / np.max(y_b, axis=0) * self.beta
        plt.plot(bins_b, y_b * alpha_b, 'g--', label='正态曲线')
        plt.vlines(235, 0, np.max(n_b,axis=0) * self.gama, colors=self.color_kinds['B1'],
                   linestyles='-.', label='国标上限 235V')
        plt.legend(fontsize=6, loc=self.pos)
        plt.xlabel('B相电压(单位:V)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        plt.setp(ax_ub.get_yticklabels(), visible=False)
        #Uc
        ax_uc = plt.subplot(133, sharey=ax_ua)
        n_c, bins_c, patches_c = plt.hist(df.Uc, bins=16, alpha=0.6,
                                          rwidth=0.9, color=self.color_kinds['C0'],
                                          label='概率', density=False)  # 这里norm用来拟合正态分布
        for a, b in zip(bins_c, n_c):
            plt.text(a, b + 2, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)
        y_c = stats.norm.pdf(bins_c, mu[6], sigma[6])
        alpha_c = np.max(n_c, axis=0) / np.max(y_c, axis=0) * self.beta
        plt.plot(bins_c, y_c * alpha_c, 'r--', label='正态曲线')
        # 画参考线
        plt.vlines(235, 0, np.max(n_c, axis=0) * self.gama, colors=self.color_kinds['C1'],
                   linestyles='-.', label='国标上限 235V')
        plt.legend(fontsize=6, loc=self.pos)
        plt.xlabel('C相电压(单位:V)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        plt.setp(ax_uc.get_yticklabels(), visible=False)

        fig2.tight_layout(pad=1.8)
        plt.suptitle('A、B、C三相电压概率分布图')# 总标题
        if save == True:
            plt.savefig(self.path+'U.Png')
            plt.show()
            plt.close()
        return

    def paint_upie(self, save=True):
        fig3 = plt.figure(figsize=[7.5, 2.5], dpi=150, facecolor='gainsboro')
        # 画A相电压环形图
        plt.subplot(131)
        wedges1, texts1, autotexts1 = plt.pie(values_u[0], autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=self.color_kinds['A2'], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'},
                                              )
        plt.legend(wedges1, labels=['合格率 %.1f%%' % (qr_u[0] * 100), '不合格率 %.1f%%' % (ur_u[0] * 100)], fontsize=7,
                   title='A相电压', loc='center')

        # 画B相电压环形图
        plt.subplot(132)
        wedges2, texts2, autotexts2 = plt.pie(values_u[1], autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=self.color_kinds['B2'], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'},
                                              )
        plt.legend(wedges2, labels=['合格率 %.1f%%' % (qr_u[1] * 100), '不合格率 %.1f%%' % (ur_u[1] * 100)], fontsize=7,
                   title='B相电压', loc='center')

        # 画C相电压环形图
        plt.subplot(133)
        wedges3, texts3, autotexts3 = plt.pie(values_u[2], autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=self.color_kinds['C2'], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'},
                                              )
        plt.legend(wedges3, labels=['合格率 %.1f%%' % (qr_u[2] * 100), '不合格率 %.1f%%' % (ur_u[2] * 100)], fontsize=7,
                   title='C相电压', loc='center')
        plt.suptitle('A、B、C三相电压合格率')
        fig3.set_tight_layout(True)
        if save == True:
            plt.savefig(self.path+'Upie.png')
            plt.show()
            plt.close()
        return

    def paint_uthd(self, save=True):
        fig4 = plt.figure(figsize=[10.5, 3.55], dpi=150, facecolor='gainsboro')
        #UaTHD
        ax_thdua = plt.subplot(131)
        n_thdua, bins_thdua, patches_thdua = plt.hist(df.Ua_THD, bins=13, alpha=0.6,
                                                      rwidth=0.9, color=self.color_kinds['A0'],
                                                      label='概率', density=False)
        for a, b in zip(bins_thdua, n_thdua):
            plt.text(a, b + 2, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)
        if np.max(df.Ua_THD, axis=0) > 5:
            plt.vlines(5, 0, np.max(n_thdua, axis=0) * self.gama,
                       colors=(0.953, 0.641, 0.406), linestyles='-.', label='上限 5%')
        plt.legend(fontsize=6, loc=self.pos)
        plt.xlabel('A相电压THD(单位:%)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        plt.setp(ax_thdua.get_yticklabels(), fontsize=9)
        #UbTHD
        ax_thdub = plt.subplot(132, sharey=ax_thdua)
        n_thdub, bins_thdub, patches_thdub = plt.hist(df.Ub_THD, bins=13, alpha=0.6,
                                                      rwidth=0.9, color=self.color_kinds['B0'],
                                                      label='概率', density=False)
        for a, b in zip(bins_thdub, n_thdub):
            plt.text(a, b + 2, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)
        if np.max(df.Ub_THD, axis=0) > 5:
            plt.vlines(5, 0, np.max(n_thdub, axis=0) * self.gama,
                        colors=self.color_kinds['B1'], linestyles='-.', label='上限 5%')
        plt.legend(fontsize=6, loc=self.pos)
        plt.xlabel('B相电压THD(单位:%)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        plt.setp(ax_thdub.get_yticklabels(), visible=False)
        #UcTHD
        ax_thduc = plt.subplot(133, sharey=ax_thdua)
        n_thduc, bins_thduc, patches_thduc = plt.hist(df.Uc_THD, bins=13, alpha=0.6,
                                                      rwidth=0.9, color=self.color_kinds['C0'],
                                                      label='概率', density=False)
        for a, b in zip(bins_thduc, n_thduc):
            plt.text(a, b + 2, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)
        if np.max(df.Uc_THD,axis=0) > 5:
            plt.vlines(5, 0, np.max(n_thduc, axis=0) * self.gama,
                       colors=self.color_kinds['C1'], linestyles='-.', label='上限 5%')
        plt.legend(fontsize=6, loc='upper right')
        plt.xlabel('C相电压THD(单位:%)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        plt.setp(ax_thduc.get_yticklabels(), visible=False)
        plt.suptitle('A、B、C三相电压谐波含有率概率分布图')
        fig4.tight_layout(pad=1.8)
        if save == True:
            plt.savefig(self.path+'U_THD.png')
            plt.show()
            plt.close()
        return

    def paint_uthdpie(self,save=True):
        fig5 = plt.figure(figsize=[7.5, 2.5], dpi=150, facecolor='gainsboro')
        # 画A相谐波电压环形图
        plt.subplot(131)
        wedges4, texts4, autotexts4 = plt.pie(values_uthd[0], autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=self.color_kinds['A2'], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'},
                                              )
        plt.legend(wedges4, labels=['合格率 %.1f%%' % (qr_uthd[0] * 100), '不合格率 %.1f%%' % (ur_uthd[0] * 100)], fontsize=7,
                   title='A相电压', loc='center')

        # 画B相谐波电压环形图
        plt.subplot(132)
        wedges5, texts5, autotexts5 = plt.pie(values_uthd[1], autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=self.color_kinds['B2'], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'},
                                              )
        plt.legend(wedges5, labels=['合格率 %.1f%%' % (qr_uthd[1] * 100),
                                    '不合格率 %.1f%%' % (ur_uthd[1] * 100)], fontsize=7,
                   title='B相电压', loc='center')

        # 画C相谐波电压环形图
        plt.subplot(133)
        wedges6, texts6, autotexts6 = plt.pie(values_uthd[2], autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=self.color_kinds['C2'], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'},
                                              )
        plt.legend(wedges6, labels=['合格率 %.1f%%' % (qr_uthd[2] * 100),
                                    '不合格率 %.1f%%' % (ur_uthd[2] * 100)], fontsize=7,
                   title='C相电压', loc='center')
        plt.suptitle('A、B、C三相谐波电压合格率')
        fig5.set_tight_layout(True)
        if save == True:
            plt.savefig(self.path+'UTHD_pie.png')
            plt.show()
            plt.close()
        return

    def paint_lf(self, electricity=df.LF, args='GZ1', save=True):
        '''
        画负荷率
        :param electricity: 输入LF的数组，类型为Series
        :param args: 无二级过载填'GZ1'，有二级过载填'GZ2'
        :return:
        '''
        fig6 = plt.figure(figsize=[10.5, 3.55], dpi=150, facecolor='gainsboro')
        plt.subplot2grid((1, 3), (0, 0), colspan=2)
        n_lf, bins_lf, patches_lf = plt.hist(electricity, bins=25, alpha=0.6, rwidth=0.9,
                                             label='概率', density=False)

        for a, b in zip(bins_lf, n_lf):
            plt.text(a, b + 0.25, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)
        y_lf = stats.norm.pdf(bins_lf, mu[7], sigma[7])

        alpha = np.max(n_lf, axis=0) / np.max(y_lf, axis=0) * self.beta

        plt.plot(bins_lf, y_lf * alpha, color='mediumturquoise', linestyle='--', label='正态曲线')
        if np.max(electricity, axis=0) > 85:
            plt.vlines(85, 0, np.max(n_lf, axis=0) * self.gama, colors='mediumturquoise', linestyles='-.',
                       label='国标 85%')
        plt.legend(fontsize=10, loc=self.pos)
        plt.xlabel('负荷率(单位:%)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        plt.title('负荷率分布图', fontsize=10, loc='left')

        plt.subplot2grid((1, 3), (0, 2))
        wedges1, texts1, autotexts1 = plt.pie(values_lf[args], autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=self.color_kinds[args], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'}
                                              )  # 保留2级过载的颜色 'mediumpurple'
        plt.legend(wedges1, labels_lf[args], fontsize=7, title='负载级别', loc='center')
        plt.title('负载情况', fontsize=10)
        plt.suptitle('负荷率分布情况')
        fig6.set_tight_layout(True)
        if save == True:
            plt.savefig(self.path + 'LF.png')
            plt.show()
            plt.close()
        return

    def paint_unb(self, electricity=df.I_UP, save=1):
        '''
        画不平衡度
        :param electricity: 输入df.I_UP
        :return:
        '''
        fig7 = plt.figure(figsize=[10.5, 3.55], dpi=150, facecolor='gainsboro')
        plt.subplot2grid((1, 3), (0, 0), colspan=2)

        n_iup, bins_iup, patches_iup = plt.hist(electricity, bins=25, alpha=0.6,
                                                rwidth=0.9, label='概率', density=False)
        for a, b in zip(bins_iup, n_iup):
            plt.text(a, b + 0.0025, '%.1f%%' % (b / freq * 100), ha='left', va='bottom', fontsize=6)
        y_iup = stats.norm.pdf(bins_iup, mu[8], sigma[8])

        alpha = np.max(n_iup, axis=0) / np.max(y_iup, axis=0) * self.beta

        plt.plot(bins_iup, y_iup * alpha, color='mediumturquoise', linestyle='--', label='正态曲线')

        if np.max(df.I_UP, axis=0) > 15:
            plt.vlines(15, 0, np.max(n_iup,axis=0) * self.gama, colors='mediumturquoise',
                       linestyles='-.', label='国标 15%')
        plt.legend(fontsize=10, loc=self.pos)
        plt.xlabel('三相电流不平度(单位:%)', fontsize=9)
        plt.ylabel('发生次数', fontsize=9)
        plt.title('三相电流不平衡分布图', fontsize=10, loc='left')
        plt.subplot2grid((1, 3), (0, 2))
        wedges2, texts2, autotexts2 = plt.pie(values_unb, autopct="%.1f%%", radius=1, pctdistance=0.85,
                                              colors=['cornflowerblue', 'lavender'], textprops={'color': 'w'},
                                              startangle=90, wedgeprops={'width': 0.3, 'edgecolor': 'w'},
                                              )
        plt.legend(wedges2, labels_unb, fontsize=8, loc='center')
        plt.title('三相不平衡合格及不合格情况', fontsize=10)
        plt.suptitle('三相电流不平衡分布情况')
        fig7.set_tight_layout(True)
        if save == True:
            plt.savefig(self.path+'Unb.png')
            plt.show()
            plt.close()
        return

    def paint_hvmax(self, args=yyy, save=1):
        fig8 = plt.figure(figsize=[9, 4], dpi=180, facecolor='gainsboro')
        sum = 0
        for i in rank:
            plt.bar(X + sum, args[i], width=0.4, facecolor=color_hv[i], edgecolor='white', label=phase[i] + '相分次谐波',
                    alpha=0.84)

            for a, b in zip(X + sum, args[i]):
                plt.text(a, b + 0.1, '%.1f' % b, ha='center', va='bottom', fontsize=4.8)

            sum += distance
        plt.legend()
        plt.grid(alpha=0.618, linestyle='-.')  # 画网格
        plt.xticks(X, Na)
        plt.title('电流分次谐波(最大值)')
        plt.xlabel('谐波次级')
        plt.ylabel('谐波电流值(单位:A)')
        fig8.tight_layout()
        ax1 = plt.gca()
        ax1.patch.set_facecolor('lightcyan')  # 设置ax1区域背景颜色
        ax1.patch.set_alpha(0.5)
        if save == True:
            plt.savefig(self.path + 'HVmax.png')
            plt.show()
            plt.close()
        return

    def paint_hvmean(self, args=zzz, save=1):
        import matplotlib.pyplot as plt
        fig9 = plt.figure(figsize=[9, 4], dpi=180, facecolor='gainsboro')
        sum = 0
        for i in rank:
            plt.bar(X + sum, args[i], width=0.4, facecolor=color_hv[i], edgecolor='white',
                    label=phase[i] + '相分次谐波', alpha=0.84)

            for a, b in zip(X + sum, args[i]):
                plt.text(a, b + 0.01, '%.1f' % b, ha='center', va='bottom', fontsize=4.8)

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
        fig9.tight_layout()
        if save == True:
            plt.savefig(self.path+'HVmean.png')
            plt.show()
            plt.close()
        return

    def paint_hvqr(self, args=qr_ithd, save=1):
        import matplotlib.pyplot as plt
        fig10 = plt.figure(figsize=[9, 4], dpi=180, facecolor='gainsboro')
        sum = 0
        for i in rank:
            plt.bar(X + sum, args[i], width=0.4, facecolor=color_hv[i], edgecolor='white',
                    label=phase[i] + '相分次谐波', alpha=0.84)

            for a, b in zip(X + sum, args[i]):
                plt.text(a, b + 0.1, '%.1f' % b, ha='center', va='bottom', fontsize=4.8)

            sum += distance
        plt.legend()
        plt.grid(alpha=0.618, linestyle='-.') #画网格
        plt.xticks(X, Na)
        plt.title('电流分次谐波合格率')
        plt.xlabel('谐波次级')
        plt.ylabel('谐波分次合格率(单位:%)')
        ax3 = plt.gca()
        ax3.patch.set_facecolor('lightcyan')  #设置ax1区域背景颜色
        ax3.patch.set_alpha(0.5)
        fig10.tight_layout()
        if save == True:
            plt.savefig(self.path+'HVqrate.png')
            plt.show()
            plt.close()
        return

#测试画图
if __name__ == "__main__":
    p = Paint()
    p.pos = 'upper left' #改变标签位置 一般为upper left
    p.paint_u() #画电压
    p.paint_upie() #画电压合格率
    p.pos = 'upper left' #改变标签位置
    p.paint_i() #画电流
    p.paint_ipie() #画电流合格率
    p.paint_uthd() #画电压THD
    p.paint_uthdpie() #画电压THD合格率
    p.pos = 'upper right'
    p.paint_unb() #画不平衡
    p.pos = 'upper left' #出现标签挡住了图形 改变位置 一般为upper left或者upper right，也可以放中间'upper center'
    p.paint_pf() #画功率因数
    #p.pos = 'upper right'  # 图形标签位置
    #p.beta = 0.5  # 调整曲线的高度 范围为0~1 觉得曲线高度太高了可以在对应图形上面加上该语句
    p.paint_lf(args='GZ1')  # 有二级过载时括号内填 args='GZ2'；没有则填'GZ1'(不要忘记引号)
    p.paint_hvmean(args=zzz)  # 画谐波均值
    p.paint_hvmax(args=yyy) #画谐波最大值
    p.paint_hvqr(qr_ithd) #画谐波合格率
