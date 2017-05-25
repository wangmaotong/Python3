# coding=utf-8

import pymongo

# 连接到 MongoDB 数据库
connection = pymongo.MongoClient()

# 创建一个名为 TestDB 的数据库
tdb = connection.TestDB

# 创建一个名为 test 的表
post_info = tdb.test

# 声明一个字典
person = {'name': 'Jack', 'age': '25', 'tel': '18895330799'}

# 将名为 person 的字典存进数据库
post_info.insert_one(person).inserted_id