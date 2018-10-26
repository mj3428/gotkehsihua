
import mysql.connector
import numpy as np
import pandas as pd
import time

raw_data = pd.read_csv('./data/zjnad_data.csv', encoding='gbk', names=['用户', 'ID', '事件', '位置', '内容', '级别',
                                                        '预警次数', '状态', '时间', '详情', '数据', '处理'])
#na_col = raw_data.isnull().any(axis=0) #查看每列是否有缺失值
#print (na_col) #没有缺失值

#设置要写的库的表名
table_name = '2018Sep'
#配置数据库的基本信息
config = {'host': '127.0.0.1',
          'user': 'root',
          'password': '****',
          'port': 3306,
          'database': '*****',
          'charset': 'gbk'
          }
con = mysql.connector.connect(**config)
cursor = con.cursor()

def judge():
    #查找数据库是否存在目标表，如果没有则新建
    cursor.execute('show tables')
    table_object = cursor.fetchall() #通过fetchall方法获得所有数据

    table_list = [] #创建库列表
    for t in table_object:
        table_list.append(t[0])
    print (table_list)


    if table_name not in table_list: #如果目标表没有创建
        cursor.execute('''
        CREATE TABLE %s (
        id         int (10),
        user       VARCHAR (50),
        uid        VARCHAR (20),
        events     VARCHAR (20),
        place      VARCHAR (50),
        content    VARCHAR (50),
        rank       VARCHAR (10),
        freq       int (5),
        state      VARCHAR (10),
        time       VARCHAR (10),
        details    VARCHAR (10),
        data       VARCHAR (10),
        solve      VARCHAR (10)
        )ENGINE=InnoDB DEFAULT  CHARSET=gb2312
        ''' %table_name) #创建新表

id = raw_data.index
print (raw_data.shape[0])
#timestamp = time.strftime('%Y-%m-%d',time.localtime(time.time()))
for i in range(raw_data.shape[0]):
    if "%" in raw_data['内容'].iloc[i]:
        raw_data['内容'].iloc[i].replace("%","%%")
    insert_sql = "INSERT INTO `%s` VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s', '%s', '%s', '%s', '%s')" % \
                 (table_name, id[i], raw_data['用户'].iloc[i], raw_data['ID'].iloc[i],
                  raw_data['事件'].iloc[i], raw_data['位置'].iloc[i], raw_data['内容'].iloc[i],
                  raw_data['级别'].iloc[i], raw_data['预警次数'].iloc[i], raw_data['状态'].iloc[i],
                  raw_data['时间'].iloc[i], raw_data['详情'].iloc[i], raw_data['数据'].iloc[i], raw_data['处理'].iloc[i],
                  )
    cursor.execute(insert_sql) #执行SQL语句，execute函数里面要用双引号
    con.commit() #提交命令
cursor.close() #关闭游标
con.close() #关闭数据库连接
#print ('Finish inserting,total records is : %d'% (i+1))
