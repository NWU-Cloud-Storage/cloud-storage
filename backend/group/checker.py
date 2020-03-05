"""
Group 检查器
"""
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import ParseError
from rest_framework.exceptions import PermissionDenied

from group.models import Group, MembershipTmp, Intention


def check_exist_group(group_id):
    """根据group_id查找group"""
    group = get_object_or_404(Group, id=group_id)
    return group


def check_user_in_group(user, group):
    """检查user在group里面"""
    membership = get_object_or_404(MembershipTmp, group=group, user=user)
    return membership


def check_user_not_in_group(user, group):
    """检查user不再group里面"""
    try:
        MembershipTmp.objects.get(user=user, group=group)
    except ObjectDoesNotExist:
        return
    raise ParseError()


def check_user_is_master_or_manager(membership):
    """检查user是群主或管理员"""
    if not membership.permission in ('master', 'manager'):
        raise PermissionDenied()


def check_user_is_master(membership):
    """检查user是群主"""
    if not membership.permission == 'master':
        raise PermissionDenied()


def check_higher_permission(ms1, ms2):
    """检查ms1权限应该大于ms2"""
    if not ms1 > ms2:
        raise PermissionDenied()


def check_exist_intention(user, group):
    intention = get_object_or_404(Intention, user=user, group=group)
    return intention
