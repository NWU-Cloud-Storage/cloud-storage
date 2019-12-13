'''
intention相关接口的视图
'''
from rest_framework.response import Response
from rest_framework.views import APIView

from my_utils.checker import check_is_none

from user.checker import check_exist_user

from group.models import Intention as IntentionModel
from group.checker import check_exist_group
from group.checker import check_user_in_group
from group.checker import check_user_not_in_group
from group.checker import check_user_is_master_or_manager
from group.checker import check_exist_intention
from group.serializers import IntentionSerializer, GroupMemberSerializer

class Intention(APIView):
    '''
    intention相关接口的视图类
    '''
    @staticmethod
    def get(request, group_id, username=None):
        '''
        获取某群请求加入列表
        '''
        check_is_none(username)

        myself = request.user.user
        group = check_exist_group(group_id)
        my_membership = check_user_in_group(myself, group)
        check_user_is_master_or_manager(my_membership)

        intentions = my_membership.group.intention_set
        serializer = IntentionSerializer(intentions, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, group_id, username=None):
        '''
        如果username为None 则是请求加入一个群
        否则是同意某人的加入
        '''
        myself = request.user.user
        group = check_exist_group(group_id)
        if username: # 同意某人加入
            return Intention._consent_intention(myself, group, username)
        return Intention._new_intention(myself, group)

    @staticmethod
    def _new_intention(myself, group):
        '''
        请求加入一个群
        '''
        check_user_not_in_group(myself, group)

        intention, created = IntentionModel.objects.get_or_create(group=group, user=myself)
        if not created:
            intention.save() # 更新时间
        serializer = IntentionSerializer(intention)
        return Response(serializer.data)

    @staticmethod
    def _consent_intention(myself, group, username):
        '''
        同意某人的加群申请
        '''
        the_other = check_exist_user(username)
        others_intention = check_exist_intention(the_other, group)

        my_membership = check_user_in_group(myself, group)
        check_user_is_master_or_manager(my_membership)

        membership = others_intention.consent()
        serializer = GroupMemberSerializer(membership)
        return Response(serializer.data)

    @staticmethod
    def delete(request, group_id, username):
        '''
        拒绝某人的加群申请
        '''
        myself = request.user.user
        group = check_exist_group(group_id)

        the_other = check_exist_user(username)
        others_intention = check_exist_intention(the_other, group)

        my_membership = check_user_in_group(myself, group)
        check_user_is_master_or_manager(my_membership)

        others_intention.reject()
        return Response()
