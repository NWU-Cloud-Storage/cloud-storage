'''
User相关检查装饰器
'''
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response

from my_utils.utils import detail

from user.models import User

def check_add_myself(func):
    '''
    向关键字中加入 myself = request.user.user ,
    防止后面多次使用 request.user.user 造成资源浪费\n
    需要 request\n
    新加 myself\n
    '''
    def inner(request, **kwargs):
        myself = request.user.user
        return func(
            request=request,
            myself=myself,
            **kwargs
        )
    return inner

def check_exist_the_other(func):
    '''
    根据username检查the_other是否存在\n
    需要 username\n
    新加 the_other\n
    '''
    def inner(username, **kwargs):
        try:
            the_other = User.objects.get(Q(username=username))
        except ObjectDoesNotExist:
            return Response(
                detail("不存在该用户。"),
                status.HTTP_400_BAD_REQUEST
            )
        return func(
            username=username,
            the_other=the_other,
            **kwargs
        )
    return inner

def check_i_am_not_the_other(func):
    '''
    检查我和对方不是同一个人\n
    需要 myself, the_other\n
    '''
    def inner(myself, the_other, **kwargs):
        if myself == the_other:
            return Response(
                detail("不能对自己使用此操作。"),
                status.HTTP_400_BAD_REQUEST
            )
        return func(
            myself=myself, the_other=the_other,
            **kwargs
        )
    return inner
