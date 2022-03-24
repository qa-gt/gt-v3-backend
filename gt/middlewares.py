from rest_framework.exceptions import AuthenticationFailed


class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Methods'] = "*"
        response['Access-Control-Allow-Headers'] = "*"
        return response


class GtMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check UA
        if not request.headers.get("User-Agent") or not any(
                i in request.headers["User-Agent"]
                for i in ['Chrome', 'Safari', 'Mozilla', 'Firefox']):
            raise AuthenticationFailed({
                'status': 'forbidden',
                'detail': '爬虫行为已被禁止'
            })
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
        # print(request.headers)
        response = self.get_response(request)
        return response
