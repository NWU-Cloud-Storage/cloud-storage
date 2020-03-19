"""
登入视图
"""
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

import requests
import yaml

from my_utils.checker import check_are_same

from user.models import User


class MyTmpAuthToken(ObtainAuthToken):
    """
    临时账号密码登入
    """

    def post(self, request, *args, **kwargs):
        """
        临时账号密码登入
        """
        response = super().post(request, *args, **kwargs)
        response.data['token'] = 'Token ' + response.data['token']
        response.set_cookie('token', response.data['token'])
        return response


class OAuthLogin(APIView):
    """
    登录类
    """
    permission_classes = ()

    @staticmethod
    def post(request, code):
        """
        登录
        """
        stream = open('oauth_settings.yml', 'r')
        settings = yaml.load(stream, yaml.SafeLoader)
        params = {
            'grant_type': 'authorization_code',
            'client_id': settings['client_id'],
            'client_secret': settings['client_secret'],
            'code': code,
            'redirect_uri': settings['redirect_uri']
        }
        token_req = requests.post(settings['access_token_url'], params=params)
        check_are_same(token_req.status_code, 200)
        access_token = token_req.json()['access_token']

        profile_req = requests.post(settings['profile_url'], params={'access_token': access_token})
        check_are_same(profile_req.status_code, 200)
        profile = profile_req.json()
        username = profile['id']
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            nickname = profile['attributes']['cn']
            password = User.objects.make_random_password()
            user = User.objects.create_user(username=username, nickname=nickname, password=password)
        login(request, user)
        return Response(status=status.HTTP_200_OK)


class Logout(APIView):
    """
    登出类
    """

    @staticmethod
    def post(request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
