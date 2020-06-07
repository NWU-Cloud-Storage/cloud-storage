from rest_framework import viewsets
from rest_framework.views import APIView
from storage.models import Identifier, File, Storage, Membership, User
from storage.checker import check_read_permission, check_read_write_permission
from storage.serializers import StorageMemberSerializer
from rest_framework.response import Response


class StorageMemberManageAPI(APIView):
    """仓库成员管理API"""
    def get(self, request, storage_id):
        """获取成员列表"""
        storage = Storage.objects.get(id=storage_id)
        check_read_permission(request.user, storage)
        membership = Membership.objects.filter(storage=storage)
        serializer = StorageMemberSerializer(membership, many=True)
        return Response(serializer.data)

    def put(self, request, storage_id):
        storage = Storage.objects.get(id=storage_id)
        check_read_write_permission(request.user, storage)
        username = request.data['username']
        user = User.objects.get(username=username)
        Membership.objects.create(user=user, storage=storage, permission='write')
