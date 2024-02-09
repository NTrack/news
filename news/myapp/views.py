import requests
from django.shortcuts import render
from .models import Articles
from django.http import JsonResponse
from .models import Users,Articles,Comments
from rest_framework.views import APIView
from rest_framework.response import Response

# 测试json获取,返回全部的内容信息
def test(request):
    return render(request, 'index.html')
def index(request):
    all_articles = Articles.objects.all()
    article_data = list(all_articles.values())  # 将查询集对象转换为字典列表
    return JsonResponse(article_data, safe=False)


# 下面是项目内容







