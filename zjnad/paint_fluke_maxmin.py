#!/usr/bin/env python
# encoding: utf-8
'''
@author: miaoj
@contact: major3428@foxmail.com
@software: pycharm
@file: test12.py
@time: 2019-5-17 上午 11:15
@desc:
'''

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

df1 = pd.read_excel('1#data_fluke.xlsx', index_col='datetime')
df2 = pd.read_excel('1#500.xlsx', index_col='采集时间')
df3 = pd.read_excel('1#601.xlsx', index_col='采集时间')


#设置字体
mpl.rcParams['font.sans-serif'] = ['Microsoft Yahei']
mpl.rcParams['font.family'] = 'sans-serif'#解决负号'-'显示为方块的问题
mpl.rcParams['axes.unicode_minus'] = False

fig1 = plt.figure(figsize=[11, 9], dpi=160, facecolor='gainsboro')
plt.subplot(221)
plt.hist(df1['A相有功功率最大值'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df1['B相有功功率最大值'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df1['C相有功功率最大值'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('fluke有功功率最大值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)
# plt.title('fluke有功功率——值区间', fontsize=10)

plt.subplot(222)
plt.hist(df1['A相有功功率最小值'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df1['B相有功功率最小值'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df1['C相有功功率最小值'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('fluke有功功率最小值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)
# plt.title('1#500有功功率——值区间', fontsize=10)

plt.subplot(223)
plt.hist(df2['A相有功功率'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df2['B相有功功率'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df2['C相有功功率'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('1#500有功功率值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)
# plt.title('1#500有功功率——值区间', fontsize=10)

plt.subplot(224)
plt.hist(df3['A相有功功率'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df3['B相有功功率'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df3['C相有功功率'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('1#601有功功率值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)
# plt.title('1#601有功功率——值区间', fontsize=10)
plt.suptitle('1#变压器有功功率对比', fontsize=10)
fig1.tight_layout(pad=2.2, h_pad=3.3)
fig1.savefig('./pic/total_P.png')


fig2 = plt.figure(figsize=[11, 9], dpi=160, facecolor='gainsboro')
plt.subplot(221)
plt.hist(df1['A相无功功率最大值'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df1['B相无功功率最大值'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df1['C相无功功率最大值'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('fluke无功功率最大值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)
# plt.title('fluke有功功率——值区间', fontsize=10)

plt.subplot(222)
plt.hist(df1['A相无功功率最小值'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df1['B相无功功率最小值'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df1['C相无功功率最小值'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('fluke无功功率最小值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)
# plt.title('1#500有功功率——值区间', fontsize=10)

plt.subplot(223)
plt.hist(df2['A相无功功率'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df2['B相无功功率'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df2['C相无功功率'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('1#500无功功率值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)

plt.subplot(224)
plt.hist(df3['A相无功功率'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df3['B相无功功率'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df3['C相无功功率'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('1#601无功功率值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)
# plt.title('1#601有功功率——值区间', fontsize=10)
plt.suptitle('1#变压器无功功率对比', fontsize=10)
fig2.tight_layout(pad=2.2, h_pad=3.3)
fig2.savefig('./pic/total_Q.png')


fig3 = plt.figure(figsize=[11, 9], dpi=160, facecolor='gainsboro')
plt.subplot(221)
plt.hist(df1['A相功率因数最大值'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df1['B相功率因数最大值'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df1['C相功率因数最大值'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('fluke功率因数最大值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)
# plt.title('fluke有功功率——值区间', fontsize=10)

plt.subplot(222)
plt.hist(df1['A相功率因数最小值'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df1['B相功率因数最小值'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df1['C相功率因数最小值'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('fluke功率因数最小值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)
# plt.title('fluke有功功率——值区间', fontsize=10)

plt.subplot(223)
plt.hist(df2['A相功率因数'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df2['B相功率因数'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df2['C相功率因数'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('1#500功率因数值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)
# plt.title('1#500有功功率——值区间', fontsize=10)

plt.subplot(224)
plt.hist(df3['A相功率因数'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df3['B相功率因数'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df3['C相功率因数'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('1#601功率因数值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)
# plt.title('1#601有功功率——值区间', fontsize=10)
plt.suptitle('1#变压器功率因数对比', fontsize=10)
fig3.tight_layout(pad=2.2, h_pad=3.3)
fig3.savefig('./pic/total_PF.png')


fig4 = plt.figure(figsize=[11, 9], dpi=160, facecolor='gainsboro')
plt.subplot(221)
plt.hist(df1['A相电流最大值'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df1['B相电流最大值'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df1['C相电流最大值'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('fluke电流最大值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)
# plt.title('fluke电流——值区间', fontsize=10)

plt.subplot(222)
plt.hist(df1['A相电流最小值'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df1['B相电流最小值'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df1['C相电流最小值'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('fluke电流最小值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)
# plt.title('fluke电流——值区间', fontsize=10)

plt.subplot(223)
plt.hist(df2['A相电流'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df2['B相电流'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df2['C相电流'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('1#500电流值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)
# plt.title('1#500电流——值区间', fontsize=10)



plt.subplot(224)
plt.hist(df3['A相电流'], bins=15, alpha=0.6, rwidth=0.9, color='gold', label='A相', density=True)
plt.hist(df3['B相电流'], bins=15, alpha=0.6, rwidth=0.9, color='mediumaquamarine', label='B相', density=True)
plt.hist(df3['C相电流'], bins=15, alpha=0.6, rwidth=0.9, color='lightcoral', label='C相', density=True)
plt.legend(fontsize=7, loc='upper right')
plt.xlabel('1#601电流值范围', fontsize=8)
plt.ylabel('概率密度函数', fontsize=7)

plt.suptitle('1#变压器电流对比', fontsize=10)
fig4.tight_layout(pad=2.2, h_pad=3.3)
fig4.savefig('./pic/total_I.png')
