'''
Storage 检查器
'''
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import ParseError
from rest_framework.exceptions import PermissionDenied

from storage.models import Catalogue

def check_exist_catalogue(cata_id):
    catalogue = get_object_or_404(Catalogue, id=cata_id)
    return catalogue

def check_exist_catalogues(cata_ids):
    catalogues = get_list_or_404(Catalogue, id__in=cata_ids)
    return catalogues

def check_not_root(catalogue):
    if catalogue.is_root_node():
        raise ParseError()

def check_are_siblings(catas):
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
    for ancestor in des_cata.get_ancestors():
        if ancestor in src_catas:
            raise ParseError()

def check_are_siblings_and_in_root(cata_ids, root):
    catas = check_exist_catalogues(cata_ids)
    if not catas[0].get_root() == root:
        raise ParseError()
    check_are_siblings(catas)
    return catas
