import matplotlib.pyplot as plt
--snip--
plt.tick_params(axis='both',labelsize=14)
plt.show()
#指定的实参将影响x和y轴上的刻度(axis='both'),刻度标记的字号设置为14


#使用scatter绘制散点图并设置其样式
import matplotlib.pyplot as plt
x_values = [1,2,3,4,5]
y_values = [1,4,9,16,25]
plt.scatter(x_values,y_values,s=100)
#设置图表标题并给坐标轴指定标签
plt.title("Square Numbers",fontsize=24)
plt.xlabel("Value",fontsize=14)
plt.ylabel("Square of Value",fontsize=14)
plt.tick_params(axis='both',labelsize=14)
plt.show()


#自动计算
x_values = lsit(range(1,1001))
y_values = [x**2 for x in x_values]
plt.scatter(x_values,y_values,s=40)
#坐标轴设置跳过
--snip--
#坐标轴范围,x轴为0-1100，y轴为0-1100000
plt.axis([0,1100,0,1100000])
plt.show()


#颜色映射，突显数据规律
import matplotlib.pyplot as plt
x_values = lsit(range(1,1001))
y_values = [x**2 for x in x_values]
plt.scatter(x_values,y_values,c=y_values,camp=plt.cm.Blues,edgecolor='none',s=40)
#参数camp告诉pyplot使用何种颜色映射，根据y值的大小决定颜色深浅，越小越浅

#保存
plt.savefig('squares_plot.png',bbox_inches='tight')
#第一个实参选择保存类型，第二个将多余空白区域裁剪掉（默认）


#随机漫步
from random import choice
#创建类
class RandomWalk():
  """ 一个生成随机漫步数据的类"""
  def __init__(self,num_points=5000):
    """ 一个生成随机漫步数据的类"""
    self.num_points = num_points
    #所有随机漫步都始于(0,0)
    self.x_values = [0]
    self.y_values = [0]
#选择方向
def fill_walk(self):
  """ 计算随机漫步包含的所有点"""
  #不断漫步，直到列表达到指定的长度
  while len(self.x_values) < self.num_points:
    #不断漫步，直到列表达到指定的长度
    #决定前进方向以及沿这个方向前进的距离
    x_direction = choice([1,-1]) #要么走1 要么走-1
    x_distance  = choice([0,1,2,3,4]) #随机0-4的整数
    x_step = x_direction * x_distance
    
    y_direction = choice([1,-1])
    y_distance  = choice([0,1,2,3,4])
    y_step = y_direction * y_distance
    #拒绝原地踏步
    if x_step==0 and y_step==0:
      continue
    #计算下一个点的x和y值
    next_x = self.x_values[-1] + x_step
    next_y = self.y_values[-1] + y_step
    self.x_values.append(next_x)
    self.y_values.append(next_y)
#绘图
import matplotlib.pyplot as plt
from random_walk import RandomWalk
rw = RadomWalk #实例化
rw.fill_walk() #调用
plt.scatter(rw.x_values,rw.y_values,s=15)
plt.show()




    
