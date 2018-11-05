# encoding: utf-8
#!/usr/bin/env python
'''
@author: miaojue
@contact: major3428@foxmail.com
@software: pycharm
@file: test.py
@time: 2018-10-16 下午 2:54
@desc:
'''
import pyecharts
from pyecharts import Geo,Bar,Line,Funnel,TreeMap
import pandas as pd
import matplotlib.pyplot as plt
import sys
from pyecharts import Page
from pyecharts.utils import write_utf8_html_file


#散点地图
data = [('杭州', 82), ('宁波', 21), ('台州', 22), ('金华', 25),
        ('丽水', 21), ('温州', 48), ('营口', 18), ('芜湖', 17),
        ('烟台', 13), ('威海', 10), ('常德', 12), ('衡阳',19),
        ('厦门', 11), ('泉州', 17), ('开封', 16),  ('石嘴山', 18), ('哈尔滨', 13)
        ]

geo = Geo('全国监测用户市级区域','data from PowerYun',title_color="#fff",
          title_pos='center',width=1000,height=600,background_color="#0E1736")  #正常时颜色为#404a59
attr, value = geo.cast(data)
geo.add("", attr, value, visual_range=[0, 100], visual_text_color="#fff",
        symbol_size=15, is_visualmap=True)

geo.show_config()
geo.render()

'''
#制作多图
page = Page()

#条形图
X_AXIS = ['浙江省','湖南省','山东省','福建省']
bar = Bar("前四省份", "对应用户数",title_color="white",background_color="#0E1736")
#bar.use_theme('dark')
bar.add("省份", X_AXIS, ['19','2','2','2'],legend_text_color='white',
        xaxis_label_textcolor="white",yaxis_label_textcolor="white",label_color=["#5AF0FA"])

page.add(bar)


#折线
attr = ["第40周", "第41周", "第42周", "第43周"]
v1 = [28,29,30,30]
line = Line('用户趋势','10月份',title_color="white",background_color="#0E1736")
#line.use_theme('dark')
line.add("用户数", attr, v1, mark_point=["max"],line_width=2,label_color=["#5AF0FA"],
         legend_text_color="white", xaxis_label_textcolor="white",yaxis_label_textcolor="white")
page.add(line)

page.render()
'''
'''
#漏斗
attr = ['房地产', '工业生产','教育','商业综合体','交通场站','电力系统','公共事业单位','医疗','文化中心']
value = [0.097,0.613,0.032,0.065,0.032,0.065,0.032,0.032,0.032]
data = [{"value": 0.097,"name": "房地产"},{"value": 0.613,"name": "工业生产"},{"value": 0.032,"name": "教育"},
        {"value": 0.065, "name": "商业综合体"},{"value": 0.032,"name": "交通场站"},{"value": 0.065,"name": "电力系统"},
        {"value": 0.032, "name": "公共事业单位"},{"value": 0.032,"name": "医疗"},{"value": 0.032,"name": "文化中心"}]
treemap = TreeMap("行业分布","十月份", width=1200, height=600, background_color="#0E1736",title_color="white")
treemap.add("Industry", data, is_label_show=True, label_pos='inside',legend_text_color="white")
treemap.render()
#df = pd.read_excel('C:/Users/Administrator/Desktop/zjnad_Sep.xlsx',sheet_name='隐患统计')
#print (df)
'''
