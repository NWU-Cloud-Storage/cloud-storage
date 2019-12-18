'''
my-storage相关接口的视图
'''
from rest_framework.views import APIView
from rest_framework.response import Response

from my_utils.checker import check_are_same
from my_utils.checker import check_is_none
from my_utils.checker import check_is_int, check_all_int
from my_utils.checker import check_serializer_is_valid

from storage.models import Catalogue
from storage.checker import check_exist_catalogue
from storage.checker import check_not_root
from storage.checker import check_are_siblings_and_in_root
from storage.checker import check_des_not_src_children
from storage.serializers import CatalogueSerializer, BreadcrumbsSerializer

class MyStorage(APIView):
    '''
    my-storage相关接口的视图类
    '''
    @staticmethod
    def get(request, src_cata_id=None):
        '''
        获取个人仓库内容，
        src_cata_id为None时，获取根目录。
        '''
        myself = request.user.user
        my_root = myself.storage
        src_cata = my_root
        ancestors = [my_root]
        if src_cata_id:
            src_cata = check_exist_catalogue(src_cata_id)
            ancestors = src_cata.get_ancestors(include_self=True)
            check_are_same(ancestors.first(), my_root)

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
    def delete(request, src_cata_id=None):
        '''
        删除个人仓库某文件（夹）。
        '''
        check_is_none(src_cata_id)
        cata_ids = request.data.getlist('id', None)
        if not cata_ids:
            return Response()
        cata_ids = check_all_int(cata_ids)
        check_are_siblings_and_in_root(cata_ids, request.user.user.storage)

        Catalogue.objects.filter(pk__in=cata_ids).delete()

        return Response()

    @staticmethod
    def post(request, src_cata_id=None):
        '''
        新建个人仓库文件（夹）。
        '''
        myself = request.user.user
        my_root = myself.storage
        ancestor = my_root
        if src_cata_id:
            ancestor = check_exist_catalogue(src_cata_id)
            check_are_same(ancestor.get_root(), my_root)
        if request.data.get('name') is not None:
            name = request.data['name']
        else:
            name = '新建文件夹'
        new_cata = Catalogue(name=name)
        new_cata.insert_at(ancestor, 'first-child', save=True)
        serializer = CatalogueSerializer(new_cata)
        return Response(serializer.data)

    @staticmethod
    def put(request, src_cata_id):
        '''
        修改个人仓库文件（夹），主要是改名。
        '''
        myself = request.user.user
        my_root = myself.storage
        cata = check_exist_catalogue(src_cata_id)
        check_not_root(cata)
        check_are_same(my_root, cata.get_root())
        serializer = check_serializer_is_valid(CatalogueSerializer, cata, request.data)

        serializer.save()
        return Response(serializer.data)

def _move_or_copy_check(request):

    my_root = request.user.user.storage

    src_ids = request.data.getlist('source_id', None)
    if not src_ids:
        return Response()
    src_ids = check_all_int(src_ids)
    src_catas = check_are_siblings_and_in_root(src_ids, my_root)

    des_id = request.data.get('destination_id', None)
    des_cata = my_root
    if des_id:
        des_id = check_is_int(des_id)
        des_cata = check_exist_catalogue(des_id)
    check_are_same(des_cata.get_root(), my_root)

    check_des_not_src_children(src_catas, des_cata)

    return src_catas, des_cata

class MyStorageMove(APIView):
    '''
    my-storage/move/ 相关接口的视图类
    '''
    @staticmethod
    def put(request):
        '''
        移动个人仓库文件（夹）。
        '''
        src_catas, des_cata = _move_or_copy_check(request)

        # Catalogue.objects.filter(pk__in=src_ids).update(parent=des_cata)
        # 内部应该是有signal导致无法批量修改parent，也不能使用move_to方法。
        # 可优化
        for cata in src_catas:
            cata.copy_to(des_cata)
            cata.delete()

        return Response()

class MyStorageCopy(APIView):
    '''
    my-storage/copy/ 相关接口的视图类
    '''
    @staticmethod
    def put(request):
        '''
        拷贝个人仓库文件（夹）。
        '''
        src_catas, des_cata = _move_or_copy_check(request)

        for cata in src_catas:
            cata.copy_to(des_cata)
        return Response()
