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

