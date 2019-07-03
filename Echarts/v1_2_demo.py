#!/usr/bin/env python
# encoding: utf-8
'''
@author: miaoj
@contact: major3428@foxmail.com
@software: pycharm
@file: v1_2demo.py
@time: 2019-1-7 下午 3:55
@desc:
'''

import numpy as np
from pyecharts.charts import Bar,Line
from pyecharts import options as opts
import pandas as pd
import datetime
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot


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
# print(df.columns.tolist()) 检查无误
def jungle(a):
    if a['I_ave'] == 0:
        return 0
    else:
        value = max(abs(a['Ia'] - a['I_ave']), abs(a['Ib'] - a['I_ave']), abs(a['Ic'] - a['I_ave'])) / a['I_ave']
        return value

df.ds = pd.to_datetime(df.ds, format='%Y-%m-%d %H:%M:%S')
#print(df.dtypes)检查类型
df = df.sort_values(by='ds')
#print(df.head(16))
df['PF'] = df['PF'].apply(lambda x:abs(x))
df.Ia_THD = df.Ia_THD * df.Ia / 100
df.Ib_THD = df.Ib_THD * df.Ib / 100
df.Ic_THD = df.Ic_THD * df.Ic / 100
df['I_ave'] = (df.Ia + df.Ib + df.Ic)/3
df['I_UP'] = df.apply(lambda x :jungle(x),axis=1) * 100
df = df.groupby([pd.Grouper(key='ds', freq='D')])['Ua', 'Ub', 'Uc', 'Ia','Ib','Ic',
                                                    'Ua_THD', 'Ub_THD', 'Uc_THD', 'Ia_THD', 'Ib_THD', 'Ic_THD',
                                                    'PF', 'P', 'Q', 'I_UP',
           'Ia_H3', 'Ia_H5', 'Ia_H7', 'Ia_H9', 'Ia_H11', 'Ia_H13', 'Ia_H15', 'Ia_H17', 'Ia_H19', 'Ia_H21',
           'Ib_H3', 'Ib_H5', 'Ib_H7', 'Ib_H9', 'Ib_H11', 'Ib_H13', 'Ib_H15', 'Ib_H17', 'Ib_H19', 'Ib_H21',
           'Ic_H3', 'Ic_H5', 'Ic_H7', 'Ic_H9', 'Ic_H11', 'Ic_H13', 'Ic_H15', 'Ic_H17', 'Ic_H19', 'Ic_H21'].mean()#聚合
#print(df.index) #ds变为index行
#print(df.head(16))
#df['Date'] = pd.to_datetime(df.index).dt.strftime('%m-%d %H:%M')
df = df.loc[df.Ua.isnull() != True] #处理空值，可不处理
KVA = 1600000 #变压器容量

#df['Date'] = [d.strftime('%m-%d %H:%M') for d in df.index]
df['Date'] = [d.strftime('%m-%d') for d in df.index]
df['LF'] = np.sqrt(pow(df.P, 2) + pow(df.Q, 2)) / KVA * 100
df['PF_upon'] = 0.9
df['U_upon'] = 235.4
df['U_down'] = 198
df['I_upon'] = KVA / 1000 * 1.4434
df['UTHD_upon'] = 5
df['IUP_upon'] = 15
df['LF_upon'] = 85
#print(df.Ua_THD.head(16))
values = np.array([df.Ua, df.Ub, df.Uc,
                   df.Ia, df.Ib, df.Ic,
                   df.Ua_THD, df.Ub_THD, df.Uc_THD,
                   df.Ia_THD, df.Ib_THD, df.Ic_THD,
                   df.I_UP, df.PF, df.LF])
paras = np.array([df.U_upon, df.U_down, df.I_upon,
                  df.UTHD_upon, df.IUP_upon, df.PF_upon])

#颜色配方
color_kinds = ['orange', 'mediumseagreen', 'orangered']
val = np.around(values, 1)#第二个参数为decimals，保留位数
print(val)
arr = df.Date.tolist()
print(df.dtypes)
print(len(val[0]), len(val[1]), len(val[2]))

def line_u() -> Line:
    c = (
        Line(opts.InitOpts(bg_color='#FFFFFF', width='800px', height='500px'))
        .add_xaxis(arr)
        .add_yaxis("Ua(V)", val[0], color='orangered',is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                           opts.MarkPointItem(type_="min")]))
        .add_yaxis("Ub(V)", val[1], color='mediumseagreen',is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                           opts.MarkPointItem(type_="min")]))
        .add_yaxis("Uc(V)", val[2], color='orange',is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                           opts.MarkPointItem(type_="min")]))
        .add_yaxis("上限", paras[0], linestyle_opts=opts.LineStyleOpts(width=1.5, type_='dashed'), is_symbol_show=False)
        .add_yaxis("下限", paras[1], linestyle_opts=opts.LineStyleOpts(width=1.5, type_='dashed'), is_symbol_show=False)
        .set_global_opts(
                         title_opts=opts.TitleOpts(title='电压趋势图',
                                                   subtitle='日期：' + df.Date.iloc[0] +' to ' + df.Date.iloc[-1],),
                         yaxis_opts=opts.AxisOpts(min_=190, max_=250))
        # title_textstyle_opts=opts.series_options.TextStyleOpts(color='#fff'),
        # subtitle_textstyle_opts=opts.series_options.TextStyleOpts(color='#fff')
    )
    return c
make_snapshot(snapshot, line_u().render(), "./pic/U_trend.png")

def line_i() -> Line:
    c = (
        Line(opts.InitOpts(bg_color='#FFFFFF', width='800px', height='500px'))
        .add_xaxis(arr)
        .add_yaxis("Ia(A)", val[3], color='orangered',is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                           opts.MarkPointItem(type_="min")]))
        .add_yaxis("Ib(A)", val[4], color='mediumseagreen',is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                           opts.MarkPointItem(type_="min")]))
        .add_yaxis("Ic(A)", val[5], color='orange',is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                           opts.MarkPointItem(type_="min")]))
        .add_yaxis("上限(In)", paras[2], linestyle_opts=opts.LineStyleOpts(width=1.5, type_='dashed'), is_symbol_show=False)
        .set_global_opts(
                         title_opts=opts.TitleOpts(title='电流趋势图',
                                                   subtitle='日期：' + df.Date.iloc[0] +' to ' + df.Date.iloc[-1],))
        # title_textstyle_opts=opts.series_options.TextStyleOpts(color='#fff'),
        # subtitle_textstyle_opts=opts.series_options.TextStyleOpts(color='#fff')
    )
    return c
make_snapshot(snapshot, line_i().render(), "./pic/I_trend.png")

def line_uthd() -> Line:
    c = (
        Line(opts.InitOpts(bg_color='#FFFFFF', width='800px', height='500px'))
        .add_xaxis(arr)
        .add_yaxis("Ua(V)", val[6], color='orangered',is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                           opts.MarkPointItem(type_="min")]))
        .add_yaxis("Ub(V)", val[7], color='mediumseagreen',is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                           opts.MarkPointItem(type_="min")]))
        .add_yaxis("Uc(V)", val[8], color='orange',is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                           opts.MarkPointItem(type_="min")]))
        .add_yaxis("上限(5%)", paras[3], linestyle_opts=opts.LineStyleOpts(width=1.5, type_='dashed'), is_symbol_show=False)
        .set_global_opts(
                         title_opts=opts.TitleOpts(title='电压谐波含有率趋势图',
                                                   subtitle='日期：' + df.Date.iloc[0] +' to ' + df.Date.iloc[-1],))
        # title_textstyle_opts=opts.series_options.TextStyleOpts(color='#fff'),
        # subtitle_textstyle_opts=opts.series_options.TextStyleOpts(color='#fff')
    )
    return c
make_snapshot(snapshot, line_uthd().render(), "./pic/UTHD_trend.png")

def line_ithd() -> Line:
    c = (
        Line(opts.InitOpts(bg_color='#FFFFFF', width='800px', height='500px'))
        .add_xaxis(arr)
        .add_yaxis("Ia(A)", val[9], color='orangered',is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                           opts.MarkPointItem(type_="min")]))
        .add_yaxis("Ib(A)", val[10], color='mediumseagreen',is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                           opts.MarkPointItem(type_="min")]))
        .add_yaxis("Ic(A)", val[11], color='orange',is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                           opts.MarkPointItem(type_="min")]))
        .set_global_opts(
                         title_opts=opts.TitleOpts(title='谐波电流趋势图',
                                                   subtitle='日期：' + df.Date.iloc[0] +' to ' + df.Date.iloc[-1],))
        # title_textstyle_opts=opts.series_options.TextStyleOpts(color='#fff'),
        # subtitle_textstyle_opts=opts.series_options.TextStyleOpts(color='#fff')
    )
    return c
make_snapshot(snapshot, line_ithd().render(), "./pic/ITHD_trend.png")

def line_unb() -> Line:
    c = (
        Line(opts.InitOpts(bg_color='#FFFFFF', width='800px', height='500px'))
        .add_xaxis(arr)
        .add_yaxis("不平衡度(%)", val[12], color='SandyBrown',is_symbol_show=False,
                   areastyle_opts=opts.AreaStyleOpts(opacity=0.4),
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                           opts.MarkPointItem(type_="min")]))
        .add_yaxis("上限(15%)", paras[4], linestyle_opts=opts.LineStyleOpts(width=1.5, type_='dashed'), is_symbol_show=False)
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
                         title_opts=opts.TitleOpts(title='电流不平衡趋势图',
                                                   subtitle='日期：' + df.Date.iloc[0] +' to ' + df.Date.iloc[-1],))

    )
    return c
make_snapshot(snapshot, line_unb().render(), "./pic/Unb_trend.png")

def line_pf() -> Line:
    c = (
        Line(opts.InitOpts(bg_color='#FFFFFF', width='800px', height='500px'))
        .add_xaxis(arr)
        .add_yaxis("功率因数", val[13], color='LightSkyBlue',is_symbol_show=False,
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                   areastyle_opts=opts.AreaStyleOpts(opacity=0.4),
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                           opts.MarkPointItem(type_="min")]))
        .add_yaxis("下限(0.9)", paras[5], linestyle_opts=opts.LineStyleOpts(width=1.5, type_='dashed'), is_symbol_show=False)
        .set_series_opts(

            label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title='功率因数趋势图',
                                                   subtitle='日期：' + df.Date.iloc[0] +' to ' + df.Date.iloc[-1],))

    )
    return c
make_snapshot(snapshot, line_pf().render(), "./pic/PF_trend.png")


def bar_lf() -> Bar:
    c = (
        Bar(opts.InitOpts(bg_color='#FFFFFF', width='800px', height='500px'))
        .add_xaxis(arr)
        .add_yaxis("负荷率(%)", val[14].tolist(), color='orange',
                   markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=85)]))
        .set_series_opts(markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),
                                                                 opts.MarkPointItem(type_="min")]),
                         label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
                         title_opts=opts.TitleOpts(title='负荷率趋势图',
                                                   subtitle='日期：' + df.Date.iloc[0] +' to ' + df.Date.iloc[-1],))
    )
    return c
make_snapshot(snapshot, bar_lf().render(), "./pic/LF_trend.png")
