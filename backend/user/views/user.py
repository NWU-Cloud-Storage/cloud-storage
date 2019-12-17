'''
user相关接口的视图
'''
from rest_framework.response import Response
from rest_framework.views import APIView

from user.checker import check_exist_user
from user.serializers import UserSerializer, TheOtherSerializer

from my_utils.utils import sub_dict
from my_utils.checker import check_serializer_is_valid
from my_utils.checker import check_is_none

class User(APIView):
    '''
    user相关接口的视图类
    '''
    @staticmethod
    def get(request, username=None):
        '''
        获取用户资料
        '''
        if username:
            return User._get_someone(username)

        return User._get_myself(request.user.user)

    @staticmethod
    def put(request, username=None):
        '''
        修改个人资料
        '''
        check_is_none(username)
        serializer = check_serializer_is_valid(UserSerializer, request.user.user, request.POST)

        serializer.save()
        return Response(serializer.data)

    @staticmethod
    def _get_someone(username):
        '''
        获取某用户资料
        '''
        user = check_exist_user(username)

        serializer = TheOtherSerializer(user)
        return Response(serializer.data)

    @staticmethod
    def _get_myself(myself):
        '''
        获取个人全部资料
        '''
        serializer = UserSerializer(myself)
        return Response(serializer.data)
