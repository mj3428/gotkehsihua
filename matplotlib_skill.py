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


