import requests
# from .models import *

PARTNER = 'qdzx'
LOGIN_URL = f'https://{PARTNER}.yunxiao.com/accountApi/userLogin'
USER_INFO_URL = f'https://{PARTNER}.yunxiao.com/accountApi/school/userInfo'
CAPTCHA_URL = 'https://portal.yunxiao.com/api/v1/verify/captchaCode'


def yx_login(username, password, captcha_code='', captcha_value=''):
    session = requests.Session()
    login_data = {
        'account': username,
        'password': password,
        'captchaCode': captcha_code,
        'captchaValue': captcha_value,
        'rememb': False
    }
    try:
        result = session.post(LOGIN_URL, data=login_data, timeout=5).json()
    except requests.Timeout:
        return {'status': 'timeout', 'msg': '请求超时', 'data': None}
    if result['code'] == '2':
        return {'status': 'error', 'msg': result['msg']}
    elif result['code'] == '3':
        return {
            'status': 'error',
            'msg': result['msg'],
            'captcha_code': result['data']['captchaCode']
        }
    elif result['code'] != '1':
        return {'status': 'error', 'msg': result['msg']}
    try:
        user_info = session.get(USER_INFO_URL, timeout=5).json()['userinfo']
    except requests.Timeout:
        return {'status': 'timeout', 'msg': '请求超时', 'data': None}
    if len(user_info['roles']) != 1:
        return {'status': 'error', 'msg': '该账号无身份信息或身份信息不唯一'}

    # gender = GenderChoices.SECRET
    # role = ''
    # role_data = user_info['roles'][0]
    # if user_info['gender'] == '男':
    #     gender = GenderChoices.MALE
    # elif user_info['gender'] == '女':
    #     gender = GenderChoices.FEMALE
    # if role_data['roleName'] == '学生':
    #     role = YxRoleChoices.STUDENT
    # elif role_data['roleName'] == '老师':
    #     role = YxRoleChoices.TEACHER
    # user_data = {
    #     'real_name': user_info['userName'],
    #     'mobile': user_info['mobile'],
    #     'gender': gender,
    #     'role': role,
    #     'user_id': role_data['idspData']['userId']
    # }
    # return {'status': 'success', 'data': user_data}
    return user_info


def get_captcha_url(captcha_code):
    return f"{CAPTCHA_URL}/{captcha_code}"


if __name__ == '__main__':
    from time import time
    from icecream import ic
    t1 = time()
    ic(yx_login("21081908", "Danny20070601"))
    ic(time() - t1)
