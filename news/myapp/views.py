import requests
from django.shortcuts import render
from .models import Articles
from django.http import JsonResponse
from .models import Users, Articles, Comments
from rest_framework.views import APIView
from rest_framework.response import Response


# 测试json获取,返回全部的内容信息
def test(request):
    return render(request, 'index.html')


def index(request):
    all_articles = Articles.objects.all()
    article_data = list(all_articles.values())  # 将查询集对象转换为字典列表
    return JsonResponse(article_data, safe=False)


class CommentView(APIView):
    def get(self, request):
        if request.query_params.get('article_id') is not None:
            article_id = request.query_params.get('article_id')
            all_comments = Comments.objects.filter(article_id=article_id)
            comment_data = list(all_comments.values())
            return Response(status=200, data=comment_data)
        if request.query_params.get('comment_id') is not None:
            comment_id = request.query_params.get('comment_id')
            all_comments = Comments.objects.filter(comment_id=comment_id)
            comment_data = list(all_comments.values())
            return Response(status=200, data=comment_data)
        all_comments = Comments.objects.all()
        comment_data = list(all_comments.values())
        return Response({'msg': '获取成功', 'data': comment_data})

    def post(self, request):
        data = request.data
        comment = data.get('comment')
        user_id = data.get('user_id')
        article_id = data.get('article_id')
        comment = Comments.objects.create(comment=comment, user_id=user_id, article_id=article_id)
        return Response({'msg': '创建成功', 'data': comment.comment_id})

    def delete(self, request):
        comment_id = request.data.get('comment_id')
        comment = Comments.objects.get(comment_id=comment_id)
        comment.delete()
        return Response({'msg': '删除成功', 'data': comment_id})

    def put(self, request):
        comment_id = request.data.get('comment_id')
        comment = Comments.objects.get(comment_id=comment_id)
        comment.comment = request.data.get('comment')
        comment.save()
        return Response({'msg': '修改成功', 'data': comment_id})

# 下面是项目内容
