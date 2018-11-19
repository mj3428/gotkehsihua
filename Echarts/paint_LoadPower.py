#!/usr/bin/env python
# encoding: utf-8
'''
@author: miaojue
@contact: major3428@foxmail.com
@software: pycharm
@file: paint_LoadPower.py
@time: 2018-11-19 上午 11:19
@desc:
'''

import matplotlib as mpl
import pandas as pd
from pandas import DataFrame
import numpy as np
import pyecharts
from fbprophet import Prophet
import matplotlib.pyplot as plt
from sklearn import preprocessing
import matplotlib.mlab as mlab#拟合模块
from scipy import stats
from scipy import optimize
from pyecharts import Line, Style
#读取
df = pd.read_csv('./data/nxlz_Oct_main1.csv',index_col=0)#index_col=0去掉索引
#更名
df.rename(columns={'采集时间':'ds', '电网A相电流':'Ia', '电网B相电流':'Ib', '电网C相电流':'Ic',
                   'A相电流谐波含有率':'Ia_THD', 'B相电流谐波含有率':'Ib_THD', 'C相电流谐波含有率':'Ic_THD',
                   '电网A相电压':'Ua', '电网B相电压':'Ub', '电网C相电压':'Uc',
                   'A相电压谐波含有率':'Ua_THD', 'B相电压谐波含有率':'Ub_THD', 'C相电压谐波含有率':'Uc_THD',
                   '总功率因数':'PF', '总无功功率':'Q', '总有功功率':'P',
                   '电网电流A相3次谐波含有率': 'Ia_H3', '电网电流A相5次谐波含有率': 'Ia_H5', '电网电流A相7次谐波含有率': 'Ia_H7', \
                   '电网电流A相9次谐波含有率': 'Ia_H9', '电网电流A相11次谐波含有率': 'Ia_H11', '电网电流A相13次谐波含有率': 'Ia_H13', \
                   '电网电流A相15次谐波含有率': 'Ia_H15', '电网电流A相17次谐波含有率': 'Ia_H17', '电网电流A相19次谐波含有率': 'Ia_H19', \
                   '电网电流A相21次谐波含有率': 'Ia_H21',
                   '电网电流B相3次谐波含有率': 'Ib_H3', '电网电流B相5次谐波含有率': 'Ib_H5', '电网电流B相7次谐波含有率': 'Ib_H7',
                   '电网电流B相9次谐波含有率': 'Ib_H9', '电网电流B相11次谐波含有率': 'Ib_H11', '电网电流B相13次谐波含有率': 'Ib_H13',
                   '电网电流B相15次谐波含有率': 'Ib_H15', '电网电流B相17次谐波含有率': 'Ib_H17', '电网电流B相19次谐波含有率': 'Ib_H19',
                   '电网电流B相21次谐波含有率': 'Ib_H21',
                   '电网电流C相3次谐波含有率': 'Ic_H3', '电网电流C相5次谐波含有率': 'Ic_H5', '电网电流C相7次谐波含有率': 'Ic_H7',
                   '电网电流C相9次谐波含有率': 'Ic_H9', '电网电流C相11次谐波含有率': 'Ic_H11', '电网电流C相13次谐波含有率': 'Ic_H13',
                   '电网电流C相15次谐波含有率': 'Ic_H15', '电网电流C相17次谐波含有率': 'Ic_H17', '电网电流C相19次谐波含有率': 'Ic_H19',
                   '电网电流C相21次谐波含有率': 'Ic_H21'
                   },inplace = True)



freq = len(df.ds)
KVA = 1250
df['I_ave'] = (df.Ia + df.Ib + df.Ic)/3
df['U_ave'] = (df.Ua + df.Ub + df.Uc)/3
#print(df.P.head(12),df.Q.head(12))
df['LP'] = np.sqrt(pow(df.P,2) + pow(df.Q,2))/KVA*100
values = np.array(df.LP)
print(values)
arr = np.array(df.ds)
print(arr)
#用style修改初始参数
style = Style(
    width=1800,
    height=800)
line = Line("负荷率趋势图", "宁夏用户10月", **style.init_style)
line.add("负荷率", arr, values, is_fill=True, area_color="#6BC7B3", area_opacity=0.62,
         is_smooth=True, line_color="#EBB97C")
line.render()
