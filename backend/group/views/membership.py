'''
membership相关接口的视图
'''
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from my_utils.check_decorator import check_add_request_post
from my_utils.check_decorator import check_keys_are_in_dict
from my_utils.check_decorator import check_a_not_eq_b
from my_utils.check_decorator import check_serializer_is_valid

from user.check_decorator import check_add_myself
from user.check_decorator import check_exist_the_other
from user.check_decorator import check_i_am_not_the_other

from group.check_decorator import check_exist_group
from group.check_decorator import check_i_am_in_group
from group.check_decorator import check_the_other_is_in_group
from group.check_decorator import check_i_am_master
from group.check_decorator import check_i_have_higher_permission
from group.serializers import MyGroupSerializer

class Membership(APIView):
    '''
    membership相关接口的视图类
    '''

    @staticmethod
    @check_add_myself
    @check_exist_the_other
    @check_i_am_not_the_other
    @check_exist_group
    @check_i_am_in_group
    @check_the_other_is_in_group
    @check_i_am_master
    @check_add_request_post
    @check_keys_are_in_dict(['permission'], 'request_post')
    @check_a_not_eq_b('request_post_permission', 'master', "不可以修改他人权限为群主。")
    @check_serializer_is_valid('others_membership', MyGroupSerializer, 'request_post')
    def put(others_membership_serializer, **kwargs):
        '''
        修改成员权限
        '''
        others_membership_serializer.save()
        return Response(others_membership_serializer.data, status.HTTP_200_OK)

    @staticmethod
    @check_add_myself
    @check_exist_the_other
    @check_i_am_not_the_other
    @check_exist_group
    @check_i_am_in_group
    @check_the_other_is_in_group
    @check_i_have_higher_permission
    def delete(others_membership, **kwargs):
        '''
        移出成员
        '''
        others_membership.delete()
        return Response(status=status.HTTP_200_OK)
