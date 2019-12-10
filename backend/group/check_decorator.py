'''
Group相关的检查装饰器
'''
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response

from my_utils.utils import detail

from group.models import Group, Membership, Intention

def check_exist_group(func):
    '''
    根据group_id检查是否存在这个group\n
    需要 group_id\n
    新加 group\n
    '''
    def inner(group_id, **kwargs):
        try:
            group = Group.objects.get(Q(id=group_id))
        except ObjectDoesNotExist:
            return Response(
                detail("该群组不存在。"),
                status.HTTP_400_BAD_REQUEST
            )

        return func(
            group_id=group_id,
            group=group,
            **kwargs
        )
    return inner

def check_i_am_in_group(func):
    '''
    检查myself是不是group的成员\n
    需要 myself, group\n
    新加 my_membership\n
    '''
    def inner(myself, group, **kwargs):

        try:
            my_membership = Membership.objects.get(Q(group=group)&Q(user=myself))
        except ObjectDoesNotExist:
            return Response(
                detail("您不在该群组。"),
                status.HTTP_403_FORBIDDEN
            )

        return func(
            myself=myself, group=group,
            my_membership=my_membership,
            **kwargs
        )
    return inner

def check_i_am_master_or_manager(func):
    '''
    检查myself是群主或管理员\n
    需要 my_membership\n
    '''
    def inner(my_membership, **kwargs):

        if not my_membership.permission in ('master', 'manager'):
            return Response(
                detail("只有群主或管理员可以进行此操作。"),
                status.HTTP_403_FORBIDDEN
            )

        return func(
            my_membership=my_membership,
            **kwargs
        )
    return inner

def check_the_other_is_in_group(func):
    '''
    检查the_other是不是group的成员\n
    需要 the_other, group\n
    新加 others_membership\n
    '''
    def inner(the_other, group, **kwargs):
        try:
            others_membership = Membership.objects.get(Q(group=group)&Q(user=the_other))
        except ObjectDoesNotExist:
            return Response(
                detail("对方不在该群组。"),
                status.HTTP_400_BAD_REQUEST
            )

        return func(
            the_other=the_other, group=group,
            others_membership=others_membership,
            **kwargs
        )
    return inner

def check_i_am_master(func):
    '''
    检查我是群主\n
    需要 my_membership\n
    '''
    def inner(my_membership, **kwargs):
        if not my_membership.permission == 'master':
            return Response(
                detail("只有群主可以进行此操作。"),
                status.HTTP_403_FORBIDDEN
            )
        return func(
            my_membership=my_membership,
            **kwargs
        )
    return inner

def check_i_have_higher_permission(func):
    '''
    检查 我的权限 > 对方的权限\n
    需要 my_membership, others_membership\n
    '''
    def inner(my_membership, others_membership, **kwargs):
        if not my_membership > others_membership:
            return Response(
                detail("权限不足。"),
                status.HTTP_403_FORBIDDEN
            )
        return func(
            my_membership=my_membership, others_membership=others_membership,
            **kwargs
        )
    return inner

def check_exist_intention(func):
    '''
    检查 存在the_other申请加入group\n
    需要 the_other, group\n
    新增 others_intention\n
    '''
    def inner(the_other, group, **kwargs):
        try:
            others_intention = Intention.objects.get(Q(group=group)&Q(user=the_other))
        except ObjectDoesNotExist:
            return Response(
                detail("该用户没有申请加入此群组。"),
                status.HTTP_400_BAD_REQUEST
            )
        return func(
            the_other=the_other, group=group,
            others_intention=others_intention,
            **kwargs
        )
    return inner

def check_i_am_not_in_group(func):
    '''
    检查 myself不在group里面\n
    需要 myself, group\n
    '''
    def inner(myself, group, **kwargs):
        try:
            Membership.objects.get(Q(group=group)&Q(user=myself))
            return Response(
                detail("您已经在这个群组里面了。"),
                status.HTTP_400_BAD_REQUEST
            )
        except ObjectDoesNotExist:
            pass
        return func(
            myself=myself, group=group,
            **kwargs
        )
    return inner
