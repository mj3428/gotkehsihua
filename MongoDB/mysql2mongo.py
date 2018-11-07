#!/usr/bin/env python
# encoding: utf-8
'''
@author: miaojue
@contact: major3428@foxmail.com
@software: pycharm
@file: mysql2mongo.py
@time: 2018-11-7 下午 3:19
@desc:
'''
import mysql.connector
import pymongo

#mongo配置
MONGO_URL = 'localhost'
MONGO_DB = 'zjnad'
MONGO_COLLECTION = '2018sep'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


table_names = ['2018sep','2018Oct']
#配置数据库的基本信息
config = {'host': '127.0.0.1',
          'user': 'root',
          'password': 'mj3428',
          'port': 3306,
          'database': 'zjnad',
          'charset': 'gbk'
          }
con = mysql.connector.connect(**config)
cursor = con.cursor()

sql = 'select * from %s'%(table_names[0])
cursor.execute(sql)
rows = cursor.fetchall()
column_names = [d[0] for d in cursor.description]

#定义一个继承自dict的类
class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

#定义导入mongo
def save_to_mongo(result):
    """
    保存至MongoDB
    :param result: 结果
    """
    try:
        if db[MONGO_COLLECTION].insert_many(result):
            print('=success insert into mongodb')
    except Exception:
        print('fail')

#将数据转换成json格式：
items = [Row(zip(column_names, row)) for row in rows]
for item in items:
    #########没写完，有问题########
