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
    highs.append(row[1])#遍历文件中余下的各行，循环从第二行开始，若为非数值型，进行int
  print(highs)
  
  highs = []
  for row in reader:
    high = int(row[1])
    highs.append(high)
  print(highs)
