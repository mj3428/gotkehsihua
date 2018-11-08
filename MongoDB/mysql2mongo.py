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
import json
import pandas as pd
import funcy as fy
from pandas import DataFrame


table_names = ['2018sep']
#配置数据库的基本信息
config = {'host': '127.0.0.1',
          'user': 'root',
          'password': '*****',
          'port': 3306,
          'database': '****',
          'charset': 'gbk'
          }
con = mysql.connector.connect(**config)
cursor = con.cursor()

sql = 'select * from %s'%(table_names[0])
cursor.execute(sql)
column_names = [d[0] for d in cursor.description]
rows = cursor.fetchall()
#用pymysql可以这样用，如果是engine可以用pandas直接读取
row_frame = DataFrame(list(rows),columns=column_names)
#print(rows) 显示为数列，里面包含元组
cursor.close()
print(column_names) #表头

#pymongo
class MongodbConfig(object):
    #配置数据库
    host = 'localhost'
    port = 27017
    id = 'id'
    user = 'user'
    uid = 'uid'
    events = 'events'
    place = 'place'
    content = 'content'
    rank = 'rank'
    freq = 'freq'
    state = 'state'
    time = 'time'

    def __init__(self, database, collection, host=None, port=None):
        self.host = host if host else self.host
        self.port = port if port else self.port
        self.database = database
        self.collection = collection

    def _set_collection(self):
        """设置数据库"""
        client = pymongo.MongoClient(host=self.host, port=self.port)
        db = client[self.database]
        Collection = db[self.collection]

        return Collection

    def __load_dataframe(self):
        """读取CSV"""
        df = row_frame
        j = df.to_json()
        data = json.loads(j)
        return data

    def _combine_and_insert(self, data):
        """整合并插入数据"""
        # 构造 index 列表
        name_list = [self.id, self.user, self.uid, self.events, self.place,
                     self.content, self.rank, self.freq, self.state, self.time]
        # 删除 None

        for i in range(len(name_list)):
            if None in name_list:
                name_list.remove(None)

        def process_data(n):
            # 返回单个数据的字典，key为index，若无index则返回 None
            single_data = {index.lower(): data[index].get(str(n))
                           for index in name_list}

            return single_data

        lenth = len(data[self.id])  # 总长度
        coll = self._set_collection()

        # 插入数据

        for i in range(lenth):
            bar = process_data(i)
            coll.insert_one(bar)
            print('Inserting ' + str(i) + ', Total: ' + str(lenth))

    def __get_dups_id(self, data):
        """获得重复数据的id"""
        data['dups'].pop(0)

        return data['dups']

    def _drop_duplicates(self):
        """删除重复数据"""
        coll = self._set_collection()
        c = coll.aggregate([{"$group":
                                 {"_id": {'date': '$date'},
                                  "count": {'$sum': 1},
                                  "dups": {'$addToSet': '$_id'}}},
                            {'$match': {'count': {"$gt": 1}}}
                            ]
                           )
        data = [i for i in c]
        duplicates = fy.walk(self.__get_dups_id, data)
        dups_id_list = fy.cat(duplicates)

        for i in dups_id_list:
            coll.delete_one({'_id': i})
        # print("OK, duplicates droped! Done!")

    def data_to_db(self):
        """数据导入数据库"""
        data = self.__load_dataframe()
        self._combine_and_insert(data)
        self._drop_duplicates()

MGDB = MongodbConfig(database='****',collection='2018sep')
MGDB.data_to_db()
