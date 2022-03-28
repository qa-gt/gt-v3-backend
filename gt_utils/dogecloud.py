from hashlib import sha1
import hmac
import requests
import json
import urllib

from django.conf import settings


def dogecloud_api(api_path, data={}, json_mode=True):
    """
    调用 DogeCloud API

    :param api_path:    调用的 API 接口地址，包含 URL 请求参数 QueryString，例如：/console/vfetch/add.json?url=xxx&a=1&b=2
    :param data:        POST 的数据，字典，例如 {'a': 1, 'b': 2}，传递此参数表示不是 GET 请求而是 POST 请求
    :param json_mode:   数据 data 是否以 JSON 格式请求，默认为 false 则使用表单形式（a=1&b=2）

    :type api_path: string
    :type data: dict
    :type json_mode bool

    :return dict: 返回的数据
    """

    body = ''
    mime = ''
    if json_mode:
        body = json.dumps(data)
        mime = 'application/json'
    else:
        body = urllib.parse.urlencode(data)
        mime = 'application/x-www-form-urlencoded'
    sign_str = api_path + "\n" + body
    signed_data = hmac.new(settings.DOGE_SECRET.encode('utf-8'),
                           sign_str.encode('utf-8'), sha1)
    sign = signed_data.digest().hex()
    authorization = 'TOKEN ' + settings.DOGE_ACCESS + ':' + sign
    response = requests.post('https://api.dogecloud.com' + api_path,
                             data=body,
                             headers={
                                 'Authorization': authorization,
                                 'Content-Type': mime
                             })
    return response.json()
