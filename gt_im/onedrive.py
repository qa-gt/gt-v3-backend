import datetime
import json

import pytz
from django.conf import settings
from django.core.cache import cache
from requests import get, post


def get_access_token(file_policy):
    tz = pytz.timezone(settings.TIME_ZONE)
    if file_policy.update_time + datetime.timedelta(
            seconds=file_policy.expires_in) > datetime.datetime.now(tz):
        return file_policy.access_token
    r = post(
        'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        data={
            'client_id': file_policy.client_id,
            'client_secret': file_policy.client_secret,
            'redirect_uri': file_policy.redirect_uri,
            'refresh_token': file_policy.refresh_token,
            'grant_type': 'refresh_token',
        },
    ).json()
    file_policy.access_token = r['access_token']
    file_policy.refresh_token = r['refresh_token']
    file_policy.expires_in = r['expires_in'] - 60
    file_policy.save()
    return file_policy.access_token


def create_upload_session(path, policy):
    r = post(
        f'https://graph.microsoft.com/v1.0/me/drive/root:{path}:/createUploadSession',
        headers={
            'Authorization': 'Bearer ' + get_access_token(policy),
            'Content-Type': 'application/json'
        },
        data=json.dumps({
            'item': {
                '@microsoft.graph.conflictBehavior': 'rename',
            },
        }),
    ).json()
    return r.get('uploadUrl')


def get_download_url(file):
    cache_key = f'gt_im_file:{file.id}'
    r = cache.get(cache_key)
    if r:
        return r
    r = get(
        f'https://graph.microsoft.com/v1.0/me/drive/items/root:{file.source_name}:',
        headers={
            'Authorization': 'Bearer ' + get_access_token(file.policy),
        },
    ).json()
    cache.set(cache_key, r['@microsoft.graph.downloadUrl'], 1800)
    return r['@microsoft.graph.downloadUrl']


if __name__ == '__main__':
    ...
