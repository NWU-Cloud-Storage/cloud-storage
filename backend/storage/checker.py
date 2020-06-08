"""
Storage 检查器
"""
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import ParseError, PermissionDenied, ValidationError

from storage.models import Identifier, Storage, Membership
from user.models import User
from typing import List


READ = 'read'
READ_WRITE = 'read_write'
OWNER = 'owner'
PERMISSIONS = {READ: 1, READ_WRITE: 2, OWNER: 3}


def check_permission(user: User, storage: Storage, permission):
    """
    检查用户的存储库权限
    """
    assert permission in PERMISSIONS
    try:
        m = Membership.objects.get(user=user, storage=storage)
        if PERMISSIONS[permission] > PERMISSIONS[m.permission]:
            raise PermissionDenied()
    except ObjectDoesNotExist:
        raise PermissionDenied()


def get_storage_or_403(storage_id):
    """
    根据 id 获取存储库
    出于安全性上的考虑, 将无权访问和无此存储库统一返回 403
    """
    try:
        return Storage.objects.get(id=storage_id)
    except ObjectDoesNotExist:
        raise PermissionDenied()


def check_exist_catalogue(cata_id):
    """
    检查应存在该目录。
    """
    catalogue = get_object_or_404(Identifier, id=cata_id)
    return catalogue


def check_exist_catalogues(cata_ids):
    """
    检查存在这些目录。
    """
    catalogues = get_list_or_404(Identifier, id__in=cata_ids)
    return catalogues


def check_not_root(catalogue):
    """
    检查目录非根。
    """
    if catalogue.is_root_node():
        raise ParseError()


def check_identifier_belong_to_storage(storage: Storage, identifier: Identifier):
    """检查目录属于该存储库"""
    if not identifier.get_root() == storage.root_identifier:
        raise ValidationError()


def check_are_siblings(catas):
    """
    检查这些目录是兄弟结点。
    """
    tmp_ancestor = None
    for cata in catas:
        ancestor = cata.parent
        if ancestor is None:
            raise ParseError()
        if tmp_ancestor is not None:
            if not tmp_ancestor == ancestor:
                raise ParseError()
        tmp_ancestor = ancestor


def check_des_not_src_children(src_catas, des_cata):
    """
    检查目的结点不是源结点的后代。
    """
    for ancestor in des_cata.get_ancestors():
        if ancestor in src_catas:
            raise ParseError()


def check_are_children(identifiers: List[Identifier], parent_identifier: Identifier):
    for i in identifiers:
        if not i.parent == parent_identifier:
            raise ValidationError()


def check_are_siblings_and_in_root(cata_ids, root):
    """
    检查这些目录是兄弟结点，并且是这个根的后代。
    """
    catas = check_exist_catalogues(cata_ids)
    if not catas[0].get_root() == root:
        raise ParseError()
    check_are_siblings(catas)
    return catas


def check_is_ancestor(ancestor, cata):
    """
    检查ancestor是cata的祖先。
    """
    ret = list()
    all_ancestors = cata.get_ancestors(ascending=True, include_self=True)
    for an_ancestor in all_ancestors:
        ret.append(an_ancestor)
        if ancestor == an_ancestor:
            break
    else:
        raise ParseError()
    return ret[::-1]
