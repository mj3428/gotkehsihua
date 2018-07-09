#要处理的文件其实是一个很长的列表，每个元素都包含五个键的字典
from urllib.request import urlopen
import json
json_url = 'http://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json'
response = urlopen(json_url)
#读取数据
req = response.read()
#将数据写入文件
with open('btc_close_2017_urllib.json','wb')as f:
  f.write(req)
#加载json格式
file_urllib = json.loads(req)
print(file_urllib)

#方法2
import requests
json_url = 'http://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json'
req = requests.get(json_url)
#将数据写入文件
with open('btc_close_2017_request.json','w')as f:
  f.write(req.text)
file_requests = req.json()

#提取数据
import json
#将数据加载到一个列表中
filename = 'btc_close_2017.json'
with open(filename) as f:
  btc_data = json.load(f)
#打印每天的信息
for btc_dict in btc_data:
  date  = btc_dict['date']
  month = btc_dict['month']
  week  = btc_dict['week']
  weekday=btc_dcit['weekday']
  close = float(btc_dict['close'])#这里要将数值转换一下,变为浮点数
  print("{}is month{}week{},{},the colse price is{}RMB".format(date,month,week,weekday,close))
#结果如下：
#2017-01-01 is month 01 week 52,Sunday,the close price is 6928.6492 RMB
#2017-01-02 is month 01 week 1 ,Monday,the close price is 7070.2554 RMB

#绘制收盘图
#数据较大，进行编排
--snip--
date  = []
month = []
week  = []
weekday=[]
close = []
#每天的信息
for btc_dict in btc_data:
  dates.append(btc_dict['date'])
  months.append(month = btc_dict['month'])
  weeks.append(btc_dict['week'])
  weekdays.append(btc_dcit['weekday'])
  close.append(int(float(btc_dict['close'])))
import pygal

line_chart = pygal.Line(x_label_rotation=20,show_minor_x_labels=False)#x轴的标签顺时针旋转20°
line_chart.title = '收盘价（¥）'
line_chart.xlabels = dates
N = 20#X轴坐标每20天显示一次
line_chart.x_labels_major = dates[::N]
line_cahrt.add('收盘价'，close)
line_chart.render_to_file('收盘价折线图.svg')

#时间序列
--snip--
import pygal
import math
line_chart = pygal.Line(x_label_rotation=20,show_minor_x_labels=False)
line_chart.title = '收盘价对数变换（¥）'
line_chart.xlabels = dates
N = 20#X轴坐标每20天显示一次
line_chart.x_labels_major = dates[::N]
close_log = [math.log10(_) for _in close]
line_chart.add('log收盘价'，close_log)
line.chart.render_to_file('收盘价对数变换折线图（¥）.svg')

#均值
--snip--
from itertools import groupby #groupby是在itertools模块中的，用于分组
def draw_line(x_data,y_data,title,y_legend):
  xy_map = [] #存储变量的均值
  for x,y in groupby(sorted(zip(x_data,y_data)),key=lambda _:_[0]):
    y_list = [v for _,v in y]
    xy_map.append([x,sum(y_list)/len(y_list)])
  x_unique,y_mean = [*zip(*xy_map)]
  line_chart = pygal.Line()
  line_chart.title = title
  line.chart.x_labels = x_unique
  line_chart.add(y_legend,y_mean)
  line_chart.render_to_file(title+'.svg')
  return line_chart
#确定周数和收盘价的取数范围
idx_month = dates.index('2017-12-01')
line_chart_month = draw_line(months[:idx_month],close[:idx_month],'收盘价月日均值（¥）','月日均值')
line_chart_month
#周
idx_week = dates.index('2017-12-11')
line_chart_week = draw_line(weeks[1:idx_week],close[1:idx_week],'收盘价周日均值（¥）','周日均值')
line_chart_week

#整合 建立收盘价仪表盘
--snip--
with open('收盘价Dashboard.html','w',encoding='utf8') as html_file:
  html_file.write('<html><head><title>收盘价Dashboard</title><metacharset="utf-8"></head><body>\n')
  for svg in ['收盘价折线图.svg','收盘价对数变换折线图（¥）.svg','收盘价月日均值（¥）.svg','收盘价周日均值（¥）.svg']:
    html_file.write('<object type="image/svg+xml" date="{0}"height=500></objest>\n'.format(svg))
  html_file.write('</body></html>')  
