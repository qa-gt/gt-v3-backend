import base64
import datetime
from time import time

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse


class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method != 'OPTIONS':
            response = self.get_response(request)
        else:
            response = HttpResponse()
            response['Allow'] = '*'
        return response


class GtCheck:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_exception = any(
            request.path.startswith(i) for i in
            ['/admin/', '/user/wechat_update/', '/user/oauth_callback'])
        if not is_exception:
            # Check UA
            if not request.headers.get('User-Agent') or not any(
                    i in request.headers['User-Agent']
                    for i in ['Chrome', 'Safari', 'Mozilla', 'Firefox']):
                return JsonResponse({
                    'status': 'error',
                    'detail': '非法请求'
                },
                                    status=403)
            if request.method == 'OPTIONS':
                return HttpResponse(status=204)
            if request.method in (
                    'POST', 'PUT',
                    'PATCH') and request.GET.get("ssssign") != 'disable':
                try:
                    raw_data = base64.b64decode(request.body)
                    print(raw_data)
                    cryptor = AES.new(settings.WEBGUARD_KEY, AES.MODE_CBC,
                                      settings.WEBGUARD_IV)
                    decrypted_data = cryptor.decrypt(raw_data)
                    decrypted_data = unpad(decrypted_data, cryptor.block_size)
                    stamp_len = int(decrypted_data[0:3])
                    stamp = int(decrypted_data[3:3 + stamp_len])
                    data = decrypted_data[3 + stamp_len:]
                    if not -5 < int(time()) - stamp < 5:
                        return JsonResponse(
                            {
                                'status': 'error',
                                'detail': '非法请求, 请校对设备时间或稍后再试'
                            },
                            status=403)
                    request.META['CONTENT_TYPE'] = 'application/json'
                    setattr(request, '_body', data)
                except ValueError as e:
                    return JsonResponse({
                        'status': 'error',
                        'detail': '非法请求'
                    },
                                        status=403)
        # Get real IP
        setattr(
            request, 'ip',
            request.headers.get('X-Forwarded-For')
            or request.META['REMOTE_ADDR'])
        response = self.get_response(request)
        return response


class GtLog:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method != 'OPTIONS':
            now = datetime.datetime.now()
            for key in (
                    now.strftime('%Y-%m-%d'),
                    now.strftime('%Y-%m-%d_%H'),
                    now.strftime('%Y-%m-%d_%H:') + str(now.minute // 10 * 10),
            ):
                try:
                    cache.incr("viscnt_" + key)
                except ValueError:
                    cache.set("viscnt_" + key, 1)
        response = self.get_response(request)
        return response
