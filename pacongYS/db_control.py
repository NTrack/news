# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import Error
from categorize import categorize

database_name = "project"           # 数据库名
table_name = 'myapp_articles'       # 数据库表名
id = 'id'                           # 新闻的主键
content_url = 'url'                 # 新闻的原始URL
title = 'title'                     # 新闻标题
content = 'content'                 # 新闻的内容
img_url = 'imgurl'                  # 新闻封面的URL
date = 'date'                       # 新闻的发布时间
news_type = 'type'                  # 新闻的类型
# 创建数据库

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='root',
        )

        # 判断数据库是否存在
        db_exists = False
        cursor = connection.cursor()  # 获取游标
        cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
        result = cursor.fetchone()
        db_exists = result is not None

        if not db_exists:
            print("数据库未初始化")

        # 切换数据库
        connection.database = database_name
        cursor.close()  # 关闭游标
        return connection

    except Error as e:
        print("数据库连接错误:", e)
        return None


# 插入内容

def insert_article(connection, datalist):
    flag = 0
    try:
        cursor = connection.cursor()

        for data in datalist:

            new_type = str(categorize.get(data[3]))
            data.append(new_type)
            print(data[6])

            flag = 0
            # 检查主键id是否已经存在
            cursor.execute(f"SELECT `{id}` FROM `{table_name}` WHERE id = {data[0]}")

            existing_id = cursor.fetchone() is not None

            if (existing_id):
                continue

            # 如果id不存在，继续插入
            sql_command = f'''
            INSERT INTO  `{table_name}`({id}, {content_url}, {title}, {content}, {img_url}, {date}, {news_type})
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(sql_command, data)
            connection.commit()
            flag = 1

        if flag:
            print("数据加入成功!")
        return True
    except Error as e:
        print("数据加入数据错误:", e)
        return False
    finally:
        cursor.close()
        connection.close()
