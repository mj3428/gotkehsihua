#创建Die类
from random import randint
class Die():
  """表示一个骰子的类"""
  def __init__(self,num_sides=6):
    """骰子默认为6面"""
    self.num_sides = num_sides
  def roll(self):
    """返回一个位于1和骰子面数之间的随机值"""
    return randint(1,self.num_sides)#也就是1到6的随机整数

#开始掷骰子
from die import Die
die = Die()
results = []
for roll in range(100):
  result = die.roll()
  results.append(result)
print(results)

#分析结果
--snip--
results = []
for roll in range(1000):
  result = die.roll()
  results.append(result)
#分析
frequencies = []
for value in range(1,die.num_sides+1):
  frequency = results.count(value)#统计次数
  frequencies.append(frequency)
print(frequencies)

#绘制直方图
#导包
import pygal
--snip--
#分析
frequencies = []
for value in range(1,die.num_sides+1):
  frequency = results.count(value)#统计次数
  frequencies.append(frequency)
#结果可视化
hist = pygal.Bar()#创建条形图

hist.title = "Results of rolling one D6 1000 times."
hist.xlabels = ['1','2','3','4','5','6']
hist.x_title = "Result"
hist.y_title = "Frequency of Result"

hist.add('D6',frequencies)#添加标签
hist.render_to_file('dice_visual.svg')#图表渲染为svg文件

#同时掷两个不同面数的不同的骰子
from die import Die
import pygal
die_1 = Die()
die_2 = Die(10)
#掷骰子多次
results = []
for roll in range(1000):
  result = die_1.roll()+die_2.roll()
  results.append(result)
#分析
--snip--
#可视化结果
hist = pygal.Bar()
hist.title = "Results of rolling one D6 1000 times."
hist.xlabels = ['2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
hist.x_title = "Result"
hist.y_title = "Frequency of Result"

hist.add('D6+D10',frequencies)#添加标签
hist.render_to_file('dice_visual.svg')#图表渲染为svg文件
