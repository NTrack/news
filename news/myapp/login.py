import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework_jwt.settings import api_settings
from django.http import JsonResponse
from .models import Users

AppID = "wx0bdf8f7709eae150"
AppSecret = "d2c96c9a82c8144f0c58e68b342689f5"

def get_user_info_func(js_code):
    api_url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'
    get_url = api_url.format(AppID, AppSecret, js_code)
    r = requests.get(get_url)
    return r.json()


@require_http_methods(['POST'])
@csrf_exempt
def user_login_func(request):
    try:
        js_code = request.POST.get('js_code')
        if js_code == None:
            json_data = json.loads(request.body)
            js_code = json_data['js_code']
    except:
        return JsonResponse({'status': 500, 'error': '请输入完整数据'})
    try:
        json_data = get_user_info_func(js_code)
        if 'errcode' in json_data:
            return JsonResponse({'status': 500, 'error': '验证错误：' + json_data['errmsg']})
        res = login_or_create_account(json_data)
        return JsonResponse(res)
    except:
        return JsonResponse({'status': 500, 'error': '无法与微信验证端连接'})

def login_or_create_account(json_data):
    # 这个是可以的.set类型
    openid = json_data['openid']
    session_key = json_data['session_key']

    # 无法创建
    try:
        user = Users.objects.get(user_id=openid)
    except:
        user = Users.objects.create(
            username=openid,
            user_id=openid,
        )
    # 保存新session_key
    user.session_key = session_key
    user.save()

    try:
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        res = {
            'status': 200,
            'msg':'获取成功',
            'token': token
        }
    except:
        res = {
            'status': 500,
            'error': 'jwt验证失败'
        }
    return res