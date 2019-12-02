from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from my_utils.utils import sub_dict, detail

from .models import User as UserModel
from .serializers import UserSerializer

class User(APIView):

    def get(self, request, username=None):
        '''
        获取用户资料
        '''
        if username:
            return self.get_someone(username)

        return self.get_myself(request.user.user)

    def put(self, request):
        '''
        修改个人资料
        '''
        user = request.user.user
        serializer = UserSerializer(user, data=request.POST)
        if not serializer.is_valid():
            return Response(detail("数据不合法。", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_someone(self, username):
        '''
        获取某用户资料
        '''
        try:
            user = UserModel.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response(detail("该用户不存在。"), status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        data = serializer.data
        keys = ['username', 'nickname']
        ret = sub_dict(data, keys)
        return Response(ret, status=status.HTTP_200_OK)

    def get_myself(self, user):
        '''
        获取个人全部资料
        '''
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
