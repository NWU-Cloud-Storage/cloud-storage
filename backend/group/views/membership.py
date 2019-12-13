'''
membership相关接口的视图
'''
from rest_framework.response import Response
from rest_framework.views import APIView

from my_utils.checker import check_not_same
from my_utils.checker import check_in_list
from my_utils.checker import check_serializer_is_valid

from user.checker import check_exist_user

from group.checker import check_exist_group
from group.checker import check_user_in_group
from group.checker import check_user_is_master
from group.checker import check_higher_permission
from group.serializers import MyGroupSerializer

class Membership(APIView):
    '''
    membership相关接口的视图类
    '''

    @staticmethod
    def put(request, group_id, username):
        '''
        修改成员权限
        '''
        myself = request.user.user
        the_other = check_exist_user(username)
        check_not_same(myself, the_other)   # 不可修改自己的权限
        group = check_exist_group(group_id)
        my_membership = check_user_in_group(myself, group)
        others_membership = check_user_in_group(the_other, group)
        check_user_is_master(my_membership)
        # 只可以修改权限为manager或member
        check_in_list(request.POST.get('permission', None), ('manager', 'member'))
        serializer = check_serializer_is_valid(MyGroupSerializer, others_membership, request.POST)

        serializer.save()
        return Response(serializer.data)



    @staticmethod
    def delete(request, group_id, username):
        '''
        移出成员
        '''
        myself = request.user.user
        the_other = check_exist_user(username)
        check_not_same(myself, the_other)   # 不可移出自己
        group = check_exist_group(group_id)
        my_membership = check_user_in_group(myself, group)
        others_membership = check_user_in_group(the_other, group)
        check_higher_permission(my_membership, others_membership)

        others_membership.delete()
        return Response()
