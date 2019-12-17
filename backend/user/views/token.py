'''
登入视图
'''
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

import requests

from my_utils.checker import check_are_same

from user.models import User

class MyTmpAuthToken(ObtainAuthToken):
    '''
    临时账号密码登入
    '''
    def post(self, request, *args, **kwargs):
        '''
        临时账号密码登入
        '''
        response = super().post(request, *args, **kwargs)
        response.set_cookie('token', response.data['token'])
        return response

class OAuthToken(APIView):
    '''
    code转token登入
    '''
    permission_classes = ()

    ACCESS_TOKEN_URL = 'http://authserver.nwu.edu.cn/authserver/oauth2.0/accessToken'
    PROFILE_URL = 'http://authserver.nwu.edu.cn/authserver/oauthApi/user/profile'

    @staticmethod
    def post(request, code):
        '''
        code转token登入
        '''
        params = {
            'grant_type': 'authorization_code',
            'client_id': 'sfxzTU6D',
            'client_secret': 'aIZr2NC1Weg7b7OeY04jhEFOjjwm0OPL',
            'code': code,
            'redirect_uri': 'http://localhost/'
        }
        token_req = requests.post(OAuthToken.ACCESS_TOKEN_URL, params=params)
        check_are_same(token_req.status_code, 200)
        access_token = token_req.json()['access_token']

        profile_req = requests.post(OAuthToken.PROFILE_URL, params={'access_token': access_token})
        check_are_same(profile_req.status_code, 200)
        profile = profile_req.json()
        username = profile['id']
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            nickname = profile['attributes']['cn']
            password = User.objects.make_random_password()
            user = User.objects.create_user(username=username, nickname=nickname, password=password)
        token = Token.objects.get(user=user)
        # token.save() # 更新token值
        response = Response({'token': token.key})
        response.set_cookie('token', response.data['token'])
        return response
