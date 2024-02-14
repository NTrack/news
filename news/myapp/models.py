from django.db import models

# Create your models here.

# myapp/models.py
"""
文章数据表	articles
id：文章主键
url：文章的url
title：文章标题
content：文章内容
image_url：文章封面图片url
date：文章日期
type：文章类别


用户数据表	users
userid：用户主键
username：用户名字


评论数据表  comments
comment_id (主键)
comment：用户评论	（参照用户主键）
create_time：评论时间
user_id (外键参考用户表中的userid)
article_id (外键参考文章表中的articleid)


用户收藏数据 favorites
id：默认主键
user_id (外键参考用户表中的userid)
article_id (外键参考文章表中的articleid)
user_favorite：用户收藏数量
"""


class Users(models.Model):
    user_id = models.CharField(primary_key=True,max_length=100)
    username = models.CharField(max_length=100)
    session_key = models.CharField(max_length=100,null=True)


class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    imgurl = models.URLField()
    date = models.DateField()
    type = models.CharField(max_length=20)


class Comments(models.Model):
    objects = models.Manager()
    comment_id = models.AutoField(primary_key=True)
    comment = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # 参照Users表的外键、级联删除，如果用户注销则评论自动删除
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)  # 同理，如果文章被删除，则评论自动删除


class Favorites(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    user_favorite = models.IntegerField()

    class Meta:
        unique_together = ('user', 'article')  # 同一个用户对同一篇文章只有一个收藏记录


