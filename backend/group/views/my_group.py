'''
my-group相关接口的视图
'''
from rest_framework.response import Response
from rest_framework.views import APIView

from my_utils.checker import check_serializer_is_valid
from my_utils.checker import check_is_none

from group.checker import check_exist_group
from group.checker import check_user_in_group
from group.checker import check_user_is_master_or_manager
from group.serializers import GroupSerializer
from group.serializers import MyGroupSerializer
from group.serializers import GroupMemberSerializer

class MyGroup(APIView):
    '''
    my-group相关接口的视图类
    '''
    @staticmethod
    def get(request, group_id=None):
        '''
        获取群组
        '''
        myself = request.user.user
        if group_id:
            return MyGroup._get_group_detail(myself, group_id)
        return MyGroup._get_my_groups(myself)

    @staticmethod
    def put(request, group_id=None):
        '''
        修改群组资料
        '''
        myself = request.user.user
        group = check_exist_group(group_id)
        membership = check_user_in_group(myself, group)
        check_user_is_master_or_manager(membership)
        serializer = check_serializer_is_valid(GroupSerializer, group, request.data)

        serializer.save()
        return Response(serializer.data)

    @staticmethod
    def post(request, group_id=None):
        '''
        新建群组
        '''
        from group.models import Group, Membership
        check_is_none(group_id)

        myself = request.user.user
        name = request.data.get('name')
        my_group = Group.objects.create(name=name)
        Membership.objects.create(group=my_group, user=myself, permission='master')
        serializer = GroupSerializer(my_group)
        return Response(serializer.data)

    @staticmethod
    def delete(request, group_id=None):
        '''
        解散/退出群组
        '''
        myself = request.user.user
        group = check_exist_group(group_id)
        membership = check_user_in_group(myself, group)

        if membership.permission == 'master': # 解散群组
            group.delete()
        else: # 退出群组
            membership.delete()

        return Response()

    @staticmethod
    def _get_my_groups(myself):
        '''
        获取个人全部群组
        '''
        groups = myself.membership_set
        serializer = MyGroupSerializer(groups, many=True)
        return Response(serializer.data)

    @staticmethod
    def _get_group_detail(myself, group_id):
        '''
        获取某群组详细信息
        '''
        group = check_exist_group(group_id)
        check_user_in_group(myself, group)

        memberships = group.membership_set
        group_serializer = GroupSerializer(group)
        membership_serializer = GroupMemberSerializer(memberships, many=True)
        rtn = dict(group_serializer.data)
        rtn['members'] = membership_serializer.data
        return Response(rtn)
