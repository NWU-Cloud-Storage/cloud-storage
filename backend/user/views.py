from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from my_utils.utils import sub_dict

from .models import User as UserModel
from .serializers import UserSerializer


# Create your views here.

class User(APIView):

    def get(self, request, username=None):
        '''
        获取用户资料
        '''
        if username: # 获取某用户资料
            user = UserModel.objects.get(username=username)
            serializer = UserSerializer(user)
            data = serializer.data
            keys = ['username', 'nickname']
            ret = sub_dict(data, keys)
            return Response(ret, status=status.HTTP_200_OK)

        if username is None: # 获取个人全部资料
            user = request.user.user
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        '''
        修改个人资料
        '''
        user = request.user.user
        serializer = UserSerializer(user, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
