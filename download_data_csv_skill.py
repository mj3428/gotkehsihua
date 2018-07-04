import csv
filename = 'sitka_weather_07-2014.csv'
with open(filename) as f:
  reader = csv.reader(f)#reader处理的时候以逗号分隔 数据
  header_row = next(reader)#阅读文件第一行，且包含文件头
  print(header_row)

#打印文件头及其位置
--snip--
with open(filename) as f:
  reader = csv.reader(f)
  header_row = next(reader)
  
  for index,column_header in enumerate(header_row):
    print(index,column_header)

#提取并读取数据
imort csv
#从文件中获取最高气温
filename = 'sitka_weather_07-2014.csv'
with open(filename) as f:
  reader = csv.reader(f)
  header_row = next(reader)
  
  highs = []
  for row in reader:
    highs.append(row[1])#遍历文件中余下的各行，循环从第二行开始
  print(highs)
  
  highs = []
  for row in reader:
    high = int(row[1])
    highs.append(high)#若为非数值型，进行int
  print(highs)

#绘图
fig = plt.figure(dpi=128,figsize=(10,6))
plt.plot(highs,c='red')
#设置图形格式
plt.title("Daily high temperatures,July 2014",fontsize=24)
plt.xlabel('',fontsize=16)
plt.ylabel("Temperature(F)",fontsize=16)
plt.tick_params(axis='both',which='major',labelsize=16)
plt.show()

#若要添加横轴为时间
dates = []
  for row in reader:
    current_date = datetime.striptime(row[0],"%Y-%m-%d")
    dates.append(current_date)
plt.plot(dates,highs,c='red')
fig.autofmt_xdate()

#在最高气温与最低气温之间着色
--snip--
#根据数据绘制图形
fig = plt.figure(dpi=128,figsize=(10,6))
plt.plot(dates,highs,c='red',alpha=0.5)#alpha表示透明度，0代表完全透明
plt.plot(dates,lows,c='blue',alpha=0.5)
plt.fill_between(dates,highs,lows,facecolor='blue',alpha=0.1)#这里代表两类数据之间绘图
--snip--

#错误检查
#出现ValueError时
try:
  current_date = datetime.striptime(row[0],"%Y-%m-%d")
  high = int(row[1])
  low  = int(row[3])
except ValueError:
  print(current_date,'missingdate')#打印错误消息后循环接着处理下一行
else:
  dates.append(current_date)
  highs.append(high)
  lows.append(low)
  
