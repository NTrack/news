需要提前自定义数据库，并在django的settings中使用

# 创建数据库

django使用模型进行定义数据库内容关系

迁移信息

```python
python manage.py makemigrations

python manage.py migrate
```



# 任务

获取最新的新闻

按分类获取新闻

用户评论

用户收藏

## 任务一、二

**获取最新的新闻**和**按分类获取新闻**

终端执行目录：news/pacongYS

```
python getdata.py
```

- 使用爬虫获取网页的相关内容

  项目位置：news/pacongYS

- 使用逻辑回归算法进行分析内容并设置分类

  分类：财经, 房产, 股票, 家居, 教育, 科技, 社会, 时尚, 时政, 体育, 游戏, 娱乐

  项目位置：news/categorize

  

任务一、二目的是通过爬虫和数据分析将目的信息获取到数据库中，配置只需要修改pachongYS下的db_control。因为数据表和字段由django的模型进行迁移生成，所以不再设置。

爬虫优化：**初始获取一次数据大概需要12分钟。添加自动任务，每天午夜获取一次数据**

## 任务三

用户评论



## 任务四

用户收藏
