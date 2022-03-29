from django.http import JsonResponse, HttpResponse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import SAFE_METHODS


def validate(stamp, sign):
    stamp = int(stamp)
    encoded = (((stamp + 410427214035) ^ 7417742047104) % 52410424147) >> 3
    return encoded == int(sign)


class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method != 'OPTIONS':
            response = self.get_response(request)
        else:
            response = HttpResponse()
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Methods'] = "*"
        response['Access-Control-Allow-Headers'] = "*"
        response['Access-Control-Allow-Credentials'] = "true"
        response['Access-Control-Max-Age'] = "86400"
        response['Allow'] = "*"
        return response


class GtCheck:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check UA
        if not request.headers.get("User-Agent") or not any(
                i in request.headers["User-Agent"]
                for i in ['Chrome', 'Safari', 'Mozilla', 'Firefox']):
            return JsonResponse({
                'status': 'error',
                'detail': '非法请求'
            },
                                status=403)
        if request.method not in SAFE_METHODS and request.GET.get(
                'ssssign') != 'disable':
            try:
                stamp, sign = request.GET.get('_').split('|')

                if not validate(stamp, sign):
                    raise AuthenticationFailed
            except:
                return JsonResponse({
                    'status': 'error',
                    'detail': '非法请求'
                },
                                    status=403)
        # Get real IP
        request.__setattr__(
            "ip",
            request.headers.get("Ali-CDN-Real-IP")
            or request.META["REMOTE_ADDR"])
        response = self.get_response(request)
        return response


class GtLog:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print(request.GET.dict(), request.body, request.get_full_path())
        response = self.get_response(request)
        return response
