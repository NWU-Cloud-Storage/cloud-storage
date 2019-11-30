from django.http import JsonResponse

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
            data = serializer.data
            keys = ['username', 'nickname', 'max_size', 'used_size', 'date_last_opt']
            ret = sub_dict(data, keys)
            return Response(ret, status=status.HTTP_200_OK)

    def put(self, request):
        '''
        修改个人资料
        '''
        keys = ['nickname',]
        data = sub_dict(request.POST, keys)
        user = request.user.user
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
