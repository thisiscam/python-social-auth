"""
@author: Cambridge Yang
"""

import json

from social.utils import parse_qs
from social.backends.oauth import BaseOAuth2


class WechatOAuth2(BaseOAuth2):
    name = 'wechat'
    ID_KEY = 'openid'
    AUTHORIZATION_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    OPENID_URL = 'https://api.weixin.qq.com/sns/userinfo'
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('nickname', 'username'),
        ('headimgurl', 'avatar'),
        ('gender', 'gender')
    ]

    def get_user_details(self, response):
        return {
            'username': response.get('nickname', '')
        }

    def user_data(self, access_token, *args, **kwargs):
        openid = (kwargs.get("response") or {}).get("openid",None)
        response = self.get_json(
                self.OPENID_URL, 
                params={
                    'access_token': access_token,
                    'openid': openid,
                    'lang': 'zh_CN'
                }
        )
        response['openid'] = openid
        return response

    def request_access_token(self, url, data, *args, **kwargs):
        response = self.request(url, params=data, *args, **kwargs)
        return parse_qs(response.content)
