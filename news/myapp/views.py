import requests
from django.shortcuts import render

from .auth import TokenAuthenticate
from .models import Articles
from django.http import JsonResponse
from .models import Users, Articles, Comments
from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import create_jwt


# 测试json获取,返回全部的内容信息
def test(request):
    return render(request, 'index.html')


def index(request):
    all_articles = Articles.objects.all()
    article_data = list(all_articles.values())  # 将查询集对象转换为字典列表
    return JsonResponse(article_data, safe=False)


class TokenView(APIView):
    def get(self, request):
        js_code = request.query_params.get('code')
        # TODO: 环境变量
        appid = ''
        secret = ''
        url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={js_code}&grant_type=authorization_code'
        res = requests.get(url)
        errcode = res.json().get('errcode')
        if errcode is None:
            openid = res.json().get('openid')
            return Response({'code': 0, 'msg': '获取成功', 'data': {'token': create_jwt(openid)}})
        match errcode:
            case 40029:
                return Response({'code': errcode, 'msg': 'code无效'})
            case 40163:
                return Response({'code': errcode, 'msg': 'code已被使用'})
            case 45011:
                return Response({'code': errcode, 'msg': 'API频率限制'})
            case 40226:
                return Response({'code': errcode, 'msg': '高风险等级用户，小程序登录拦截'})
            case _:
                return Response({'code': errcode, 'msg': '未知错误'})


class CommentView(APIView):
    authentication_classes = [TokenAuthenticate]

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
        user_id = request.user.user_id
        article_id = data.get('article_id')
        comment = Comments.objects.create(comment=comment, user_id=user_id, article_id=article_id)
        return Response({'msg': '创建成功', 'data': comment.comment_id})

    def delete(self, request):
        comment_id = request.data.get('comment_id')
        comment = Comments.objects.get(comment_id=comment_id)
        if comment.user_id != request.user.user_id:
            return Response({'msg': '无权删除', 'data': comment_id})
        comment.delete()
        return Response({'msg': '删除成功', 'data': comment_id})

    def put(self, request):
        comment_id = request.data.get('comment_id')
        comment = Comments.objects.get(comment_id=comment_id)
        comment.comment = request.data.get('comment')
        comment.save()
        return Response({'msg': '修改成功', 'data': comment_id})
