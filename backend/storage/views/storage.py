"""
storage相关接口的视图
"""
from rest_framework.views import APIView
from rest_framework.response import Response

from my_utils.checker import check_are_same
from my_utils.checker import check_is_none
from my_utils.checker import get_int
from my_utils.checker import check_serializer_is_valid

from storage.models import Identifier, File, Storage, Membership, PERMISSIONS
from user.models import User
from storage.checker import check_exist_catalogue, check_identifier_belong_to_storage, check_are_children
from storage.checker import check_not_root
from storage.checker import check_are_siblings_and_in_root
from storage.checker import check_des_not_src_children
from storage.checker import check_permission, get_storage_or_403
from storage.checker import READ, READ_WRITE, OWNER
from storage.serializers import CatalogueSerializer, BreadcrumbsSerializer, StorageSerializer

from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user

from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from ..utils import create_storage


class StorageAPI(APIView):
    """
    存储库相关接口的视图类
    """

    @staticmethod
    def get(request, storage_id, identifier_id=None):
        """
        获取存储仓库内容，
        """
        storage = get_storage_or_403(storage_id)
        check_permission(request.user, storage, READ)
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
    def delete(request, storage_id, identifier_id):
        """
        删除个人仓库某文件（夹）。
        """
        user = request.user
        storage = get_storage_or_403(storage_id)
        check_permission(user, storage, READ_WRITE)

        cata_ids = request.data.get('id', None)
        if not cata_ids:
            raise ValidationError()
        cata_ids = get_int(cata_ids)
        check_are_siblings_and_in_root(cata_ids, storage.root_identifier)

        Identifier.objects.filter(pk__in=cata_ids).delete()

        return Response()

    @staticmethod
    def post(request, storage_id, identifier_id=None):
        """
        新建个人仓库文件（夹）。
        """
        user = request.user.user
        storage = get_storage_or_403(storage_id)
        check_permission(user, storage, READ_WRITE)

        root_identifier = storage.root_identifier
        ancestor = root_identifier
        if identifier_id:
            ancestor = check_exist_catalogue(identifier_id)
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
        check_permission(user, storage, READ_WRITE)
        root_identifier = storage.root_identifier

        cata = check_exist_catalogue(identifier_id)
        check_not_root(cata)
        check_are_same(root_identifier, cata.get_root())
        serializer = check_serializer_is_valid(CatalogueSerializer, cata, request.data)

        serializer.save()
        return Response(serializer.data)


def _move_or_copy_check(request, storage_id, identifier_id):
    user = request.user
    src_storage = get_storage_or_403(storage_id)
    check_permission(user, src_storage, READ)
    root_identifier = src_storage.root_identifier

    parent_identifier = Identifier.objects.get(id=identifier_id)
    check_identifier_belong_to_storage(src_storage, parent_identifier)

    src_ids = request.data.get('source_id', None)
    if not src_ids:
        raise ValidationError()
    src_ids = get_int(src_ids)
    src_identifiers = get_list_or_404(Identifier, id__in=src_ids)
    check_are_children(src_identifiers, parent_identifier)

    des_storage_id = request.data.get('destination_storage_id', None)
    des_storage = get_storage_or_403(des_storage_id)
    check_permission(user, des_storage, READ_WRITE)

    des_id = request.data.get('destination_directory_id', None)
    des_root = des_storage.root_identifier
    if des_id:
        des_id = get_int(des_id)
        des_root = check_exist_catalogue(des_id)
    check_are_same(des_root.get_root(), des_storage.root_identifier)

    check_des_not_src_children(src_identifiers, des_root)

    return src_identifiers, des_root


class MyStorageMove(APIView):
    """
    my-storage/move/ 相关接口的视图类
    """

    @staticmethod
    def put(request, storage_id, identifier_id):
        """
        移动个人仓库文件（夹）。
        """
        src_catas, des_cata = _move_or_copy_check(request, storage_id, identifier_id)

        # Catalogue.objects.filter(pk__in=src_ids).update(parent=des_cata)
        # 内部应该是有signal导致无法批量修改parent，也不能使用move_to方法。
        # 可优化 --from zjb
        # 可能这个 bug 修好了? --from cjc
        for cata in src_catas:
            cata.move_to(des_cata)

        return Response()


class MyStorageCopy(APIView):
    """
    my-storage/copy/ 相关接口的视图类
    """

    @staticmethod
    def put(request, storage_id, identifier_id):
        """
        拷贝个人仓库文件（夹）。
        """
        src_catas, des_cata = _move_or_copy_check(request, storage_id, identifier_id)

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
        check_permission(user, storage, READ_WRITE)
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


class StorageManageViewSet(viewsets.GenericViewSet):
    serializer_class = StorageSerializer
    queryset = Storage.objects.all()
    lookup_url_kwarg = "storage_id"

    def list(self, request):
        storage_list = self.get_queryset().filter(users=request.user)  # reverse relationship
        serializer = StorageSerializer(storage_list, many=True)
        return Response(serializer.data)

    def create(self, request):
        # seems that request.user is AuthUser, so we need explicitly query a user
        user = User.objects.get(pk=request.user.id)
        storage = create_storage(user, name=request.data['name'])
        serializer = StorageSerializer(storage)
        return Response(serializer.data)

    def retrieve(self, request, storage_id):
        storage = self.get_object()
        check_permission(request.user, storage, READ)
        serializer = self.get_serializer(storage)
        return Response(serializer.data)

    def put(self, request, storage_id):
        storage = self.get_object()
        check_permission(request.user, storage, READ_WRITE)
        serializer = self.get_serializer(storage, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

    def delete(self, request, storage_id):
        check_permission(request.user, self.get_object(), READ_WRITE)
        self.get_object().delete()
        return Response()


class GetPermissionsAPI(APIView):
    def get(self, request):
        rtn = []
        for permission in PERMISSIONS:
            rtn.append({"name": permission[1], "value": permission[0]})
        return Response(rtn)
