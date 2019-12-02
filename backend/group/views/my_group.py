'''
my-group相关接口的视图
'''
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from my_utils.check_decorator import check_add_request_post
from my_utils.check_decorator import check_serializer_is_valid

from user.check_decorator import check_add_myself

from group.serializers import GroupSerializer
from group.serializers import MyGroupSerializer
from group.serializers import GroupMemberSerializer
from group.check_decorator import check_exist_group
from group.check_decorator import check_i_am_in_group
from group.check_decorator import check_i_am_master_or_manager


class MyGroup(APIView):
    '''
    my-group相关接口的视图类
    '''
    @staticmethod
    @check_add_myself
    def get(myself, group_id=None, **kwargs):
        '''
        获取群组
        '''
        if group_id:
            return MyGroup._get_group_detail(myself=myself, group_id=group_id, **kwargs)
        return MyGroup._get_my_groups(myself=myself, group_id=group_id, **kwargs)

    @staticmethod
    @check_add_myself
    @check_exist_group
    @check_i_am_in_group
    @check_i_am_master_or_manager
    @check_add_request_post
    @check_serializer_is_valid('group', GroupSerializer, 'request_post')
    def put(request, group_serializer, **kwargs):
        '''
        修改群组资料
        '''
        group_serializer.save()
        return Response(group_serializer.data, status.HTTP_200_OK)

    @staticmethod
    @check_add_myself
    def post(myself, **kwargs):
        '''
        新建群组
        '''
        my_group = myself.create_a_group()
        serializer = GroupSerializer(my_group)
        return Response(serializer.data, status.HTTP_200_OK)

    @staticmethod
    @check_add_myself
    @check_exist_group
    @check_i_am_in_group
    def delete(group, my_membership, **kwargs):
        '''
        解散/退出群组
        '''
        if my_membership.permission == 'master': # 解散群组
            group.delete()
        else: # 退出群组
            my_membership.delete()

        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def _get_my_groups(myself, **kwargs):
        '''
        获取个人全部群组
        '''
        groups = myself.membership_set
        serializer = MyGroupSerializer(groups, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @staticmethod
    @check_exist_group
    @check_i_am_in_group
    def _get_group_detail(group, **kwargs):
        '''
        获取某群组详细信息
        '''
        memberships = group.membership_set
        group_serializer = GroupSerializer(group)
        membership_serializer = GroupMemberSerializer(memberships, many=True)
        rtn = dict(group_serializer.data)
        rtn['members'] = membership_serializer.data
        return Response(rtn, status.HTTP_200_OK)
