'''
group-storage相关接口的视图
'''
from rest_framework.views import APIView
from rest_framework.response import Response

from my_utils.checker import check_are_same
from my_utils.checker import check_is_none
from my_utils.checker import check_is_int, check_all_int
from my_utils.checker import check_serializer_is_valid

from group.checker import check_exist_group
from group.checker import check_user_in_group

from storage.models import Catalogue
from storage.checker import check_exist_catalogue
from storage.checker import check_not_root
from storage.checker import check_are_siblings_and_in_root
from storage.checker import check_des_not_src_children
from storage.serializers import CatalogueSerializer, BreadcrumbsSerializer

def _get_group_root(request, group_id):
    myself = request.user.user
    group = check_exist_group(group_id)
    check_user_in_group(myself, group)
    return group.storage

class GroupStorage(APIView):
    '''
    group-storage相关接口的视图类
    '''
    @staticmethod
    def get(request, group_id, src_cata_id=None):
        '''
        获取群组仓库内容，
        src_cata_id为None时，获取根目录。
        '''
        group_root = _get_group_root(request, group_id)
        src_cata = group_root
        ancestors = [group_root]
        if src_cata_id:
            src_cata = check_exist_catalogue(src_cata_id)
            ancestors = src_cata.get_ancestors(include_self=True)
            check_are_same(ancestors.first(), group_root)

        bread_serializer = BreadcrumbsSerializer(ancestors, many=True)
        cata_serializer = CatalogueSerializer(src_cata.get_children(), many=True)
        res = {'breadcrumbs': [], 'content': []}
        breadcrumbs = res['breadcrumbs']
        content = res['content']
        for data in cata_serializer.data:
            content.append(dict(data))
        for data in bread_serializer.data:
            breadcrumbs.append(dict(data))
        return Response(res)

    @staticmethod
    def delete(request, group_id, src_cata_id=None):
        '''
        删除群组仓库某文件（夹）。
        '''
        check_is_none(src_cata_id)
        cata_ids = request.POST.getlist('id', None)
        if not cata_ids:
            return Response()

        group_root = _get_group_root(request, group_id)
        cata_ids = check_all_int(cata_ids)
        check_are_siblings_and_in_root(cata_ids, group_root)

        Catalogue.objects.filter(pk__in=cata_ids).delete()
        return Response()

    @staticmethod
    def post(request, group_id, src_cata_id=None):
        '''
        新建群组仓库文件（夹）。
        '''
        group_root = _get_group_root(request, group_id)
        ancestor = group_root
        if src_cata_id:
            ancestor = check_exist_catalogue(src_cata_id)
            check_are_same(ancestor.get_root(), group_root)

        new_cata = Catalogue(name='新建文件夹')
        new_cata.insert_at(ancestor, 'first-child', save=True)
        serializer = CatalogueSerializer(new_cata)
        return Response(serializer.data)

    @staticmethod
    def put(request, group_id, src_cata_id):
        '''
        修改群组仓库文件（夹），主要是改名。
        '''
        group_root = _get_group_root(request, group_id)
        cata = check_exist_catalogue(src_cata_id)
        check_not_root(cata)
        check_are_same(group_root, cata.get_root())
        serializer = check_serializer_is_valid(CatalogueSerializer, cata, request.POST)

        serializer.save()
        return Response(serializer.data)

def _move_or_copy_check(request, group_id):

    src_ids = request.POST.getlist('source_id', None)
    if not src_ids:
        return Response()

    group_root = _get_group_root(request, group_id)
    src_ids = check_all_int(src_ids)
    src_catas = check_are_siblings_and_in_root(src_ids, group_root)

    des_id = request.POST.get('destination_id', None)
    des_cata = group_root
    if des_id:
        des_id = check_is_int(des_id)
        des_cata = check_exist_catalogue(des_id)
    check_are_same(des_cata.get_root(), group_root)

    check_des_not_src_children(src_catas, des_cata)

    return src_catas, des_cata

class GroupStorageMove(APIView):
    '''
    group-storage/move/ 相关接口的视图类
    '''
    @staticmethod
    def put(request, group_id):
        '''
        移动群组仓库文件（夹）。
        '''
        src_catas, des_cata = _move_or_copy_check(request, group_id)

        # Catalogue.objects.filter(pk__in=src_ids).update(parent=des_cata)
        # 内部应该是有signal导致无法批量修改parent，也不能使用move_to方法。
        # 可优化
        for cata in src_catas:
            # cata.move_to(des_cata, 'first-child')
            cata.copy_to(des_cata)
            cata.delete()

        return Response()

class GroupStorageCopy(APIView):
    '''
    group-storage/copy/ 相关接口的视图类
    '''
    @staticmethod
    def put(request, group_id):
        '''
        拷贝群组仓库文件（夹）。
        '''
        src_catas, des_cata = _move_or_copy_check(request, group_id)

        for cata in src_catas:
            cata.copy_to(des_cata)
        return Response()
