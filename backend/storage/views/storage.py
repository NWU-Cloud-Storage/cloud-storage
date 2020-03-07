"""
storage相关接口的视图
"""
from rest_framework.views import APIView
from rest_framework.response import Response

from my_utils.checker import check_are_same
from my_utils.checker import check_is_none
from my_utils.checker import get_int
from my_utils.checker import check_serializer_is_valid

from storage.models import Identifier, File, Storage, Membership
from user.models import User
from storage.checker import check_exist_catalogue
from storage.checker import check_not_root
from storage.checker import check_are_siblings_and_in_root
from storage.checker import check_des_not_src_children
from storage.checker import check_read_permission, check_write_permission, get_storage_or_403
from storage.serializers import CatalogueSerializer, BreadcrumbsSerializer, StorageSerializer

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user

from rest_framework.exceptions import ValidationError


class StorageAPI(APIView):
    """
    存储库相关接口的视图类
    """

    @staticmethod
    def get(request, storage_id=None, identifier_id=None):
        """
        获取存储仓库内容，
        """
        myself = request.user

        # storage_id为None时，获取用户所有仓库列表。
        if not storage_id:
            storage_list = Storage.objects.filter(users=myself)
            storage_serializer = StorageSerializer(storage_list, many=True)
            return Response(storage_serializer.data)

        storage = get_storage_or_403(storage_id)
        check_read_permission(myself, storage)
        root_identifier = storage.root_identifier

        # identifier_id为None时，获取根目录的内容
        if not identifier_id:
            identifier_id = root_identifier.id

        identifier = check_exist_catalogue(identifier_id)
        ancestors = identifier.get_ancestors(include_self=True)
        check_are_same(ancestors.first(), root_identifier)

        bread_serializer = BreadcrumbsSerializer(ancestors, many=True)
        cata_serializer = CatalogueSerializer(identifier.get_children(), many=True)
        res = {'breadcrumbs': [], 'content': []}
        breadcrumbs = res['breadcrumbs']
        content = res['content']
        for data in cata_serializer.data:
            content.append(dict(data))
        for data in bread_serializer.data:
            breadcrumbs.append(dict(data))
        return Response(res)

    @staticmethod
    def delete(request, storage_id):
        """
        删除个人仓库某文件（夹）。
        """
        user = request.user
        storage = get_storage_or_403(storage_id)
        check_write_permission(user, storage)

        cata_ids = request.data.get('id', None)
        if not cata_ids:
            raise ValidationError()
        cata_ids = get_int(cata_ids)
        check_are_siblings_and_in_root(cata_ids, storage.root_identifier)

        Identifier.objects.filter(pk__in=cata_ids).delete()

        return Response()

    @staticmethod
    def post(request, storage_id, src_cata_id=None):
        """
        新建个人仓库文件（夹）。
        """
        user = request.user.user
        storage = get_storage_or_403(storage_id)
        check_write_permission(user, storage)

        root_identifier = storage.root_identifier
        ancestor = root_identifier
        if src_cata_id:
            ancestor = check_exist_catalogue(src_cata_id)
            check_are_same(ancestor.get_root(), root_identifier)
        if request.data.get('name') is not None:
            name = request.data['name']
        else:
            name = '新建文件夹'
        new_cata = Identifier(name=name, owner=user)
        new_cata.insert_at(ancestor, 'first-child', save=True)
        serializer = CatalogueSerializer(new_cata)
        return Response(serializer.data)

    @staticmethod
    def put(request, storage_id, identifier_id):
        """
        修改个人仓库文件（夹），主要是改名。
        """
        user = request.user
        storage = get_storage_or_403(storage_id)
        check_write_permission(user, storage)
        root_identifier = storage.root_identifier

        cata = check_exist_catalogue(identifier_id)
        check_not_root(cata)
        check_are_same(root_identifier, cata.get_root())
        serializer = check_serializer_is_valid(CatalogueSerializer, cata, request.data)

        serializer.save()
        return Response(serializer.data)


def _move_or_copy_check(request, storage_id):
    user = request.user
    storage = get_storage_or_403(storage_id)
    check_read_permission(user, storage)
    root_identifier = storage.root_identifier

    src_ids = request.data.get('source_id', None)
    if not src_ids:
        raise ValidationError()
    src_ids = get_int(src_ids)
    src_catas = check_are_siblings_and_in_root(src_ids, root_identifier)

    des_storage_id = request.data.get('destination_storage_id', None)
    des_storage = get_storage_or_403(des_storage_id)
    check_write_permission(user, des_storage)

    des_id = request.data.get('destination_id', None)
    des_root = des_storage.root_identifier
    if des_id:
        des_id = get_int(des_id)
        des_root = check_exist_catalogue(des_id)
    check_are_same(des_root.get_root(), des_storage.root_identifier)

    check_des_not_src_children(src_catas, des_root)

    return src_catas, des_root


class MyStorageMove(APIView):
    """
    my-storage/move/ 相关接口的视图类
    """

    @staticmethod
    def put(request, storage_id):
        """
        移动个人仓库文件（夹）。
        """
        src_catas, des_cata = _move_or_copy_check(request, storage_id)

        # Catalogue.objects.filter(pk__in=src_ids).update(parent=des_cata)
        # 内部应该是有signal导致无法批量修改parent，也不能使用move_to方法。
        # 可优化
        for cata in src_catas:
            cata.copy_to(des_cata)
            cata.delete()

        return Response()


class MyStorageCopy(APIView):
    """
    my-storage/copy/ 相关接口的视图类
    """

    @staticmethod
    def put(request, storage_id):
        """
        拷贝个人仓库文件（夹）。
        """
        src_catas, des_cata = _move_or_copy_check(request, storage_id)

        for cata in src_catas:
            cata.copy_to(des_cata)
        return Response()


class MyStorageFiles(APIView):
    permission_classes = ()
    """
    上传文件
    """

    @staticmethod
    def post(request, storage_id, identifier_id=None):
        user = request.user
        storage = get_storage_or_403(storage_id)
        check_write_permission(user, storage)
        root_identifier = storage.root_identifier
        ancestor = root_identifier
        if identifier_id:
            ancestor = check_exist_catalogue(identifier_id)
            check_are_same(ancestor.get_root(), root_identifier)
        file = request.FILES['file']
        new_file = File(file=file, size=file.size)
        new_file.save()
        user.used_size += file.size
        user.save()
        new_cata = Identifier(name=file.name, extension=file.content_type, my_file=new_file, is_file=True)
        new_cata.insert_at(ancestor, 'first-child', save=True)
        serializer = CatalogueSerializer(new_cata)
        return Response(serializer.data)

    @staticmethod
    def get(request, src_cata_id, group_id=None):
        from django.http import StreamingHttpResponse

        # myself = request.user.user
        # my_root = myself.storage
        # cata = check_exist_catalogue(src_cata_id)
        # check_are_same(cata.get_root(), my_root)
        cata = check_exist_catalogue(src_cata_id)

        file_path = cata.my_file.file.path

        def file_iterator(file_name, chunk_size=512):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(cata.name)
        response['Content-Length'] = cata.my_file.size

        return response
