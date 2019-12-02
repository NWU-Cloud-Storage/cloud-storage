'''
intention相关接口的视图
'''
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.check_decorator import check_add_myself
from user.check_decorator import check_exist_the_other

from group.check_decorator import check_exist_group
from group.check_decorator import check_i_am_in_group
from group.check_decorator import check_i_am_not_in_group
from group.check_decorator import check_i_am_master_or_manager
from group.check_decorator import check_exist_intention
from group.serializers import IntentionSerializer, GroupMemberSerializer
from group.models import Intention as IntentionModel

class Intention(APIView):
    '''
    intention相关接口的视图类
    '''
    @staticmethod
    @check_add_myself
    @check_exist_group
    @check_i_am_in_group
    @check_i_am_master_or_manager
    def get(my_membership, **kwargs):
        '''
        获取某群请求加入列表
        '''
        intentions = my_membership.group.intention_set
        serializer = IntentionSerializer(intentions, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @staticmethod
    @check_add_myself
    @check_exist_group
    def post(username=None, **kwargs):
        '''
        如果username为None 则是请求加入一个群
        否则是同意某人的加入
        '''
        if username:
            return Intention._consent_intention(username=username, **kwargs)
        return Intention._new_intention(username=username, **kwargs)

    @staticmethod
    @check_i_am_not_in_group
    def _new_intention(group, myself, **kwargs):
        '''
        请求加入一个群
        '''
        intention, created = IntentionModel.objects.get_or_create(group=group, user=myself)
        if not created:
            intention.save() # 更新时间
        serializer = IntentionSerializer(intention)
        return Response(serializer.data, status.HTTP_200_OK)

    @staticmethod
    @check_exist_the_other
    @check_exist_intention
    @check_i_am_in_group
    @check_i_am_master_or_manager
    def _consent_intention(others_intention, **kwargs):
        '''
        同意某人的加群申请
        '''
        membership = others_intention.consent()
        serializer = GroupMemberSerializer(membership)
        return Response(serializer.data, status.HTTP_200_OK)

    @staticmethod
    @check_add_myself
    @check_exist_group
    @check_exist_the_other
    @check_exist_intention
    @check_i_am_in_group
    @check_i_am_master_or_manager
    def delete(others_intention, **kwargs):
        '''
        拒绝某人的加群申请
        '''
        others_intention.reject()
        return Response(status=status.HTTP_200_OK)
