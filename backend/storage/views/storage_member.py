from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from storage.models import Identifier, File, Storage, Membership, User
from storage.checker import check_permission
from storage.checker import READ, READ_WRITE, OWNER
from storage.serializers import StorageMemberSerializer, MembershipSerializer


class StorageMemberManageAPI(APIView):
    """仓库成员管理API"""

    def get(self, request, storage_id):
        """获取成员列表"""
        storage = Storage.objects.get(id=storage_id)
        check_permission(request.user, storage, READ)
        membership = Membership.objects.filter(storage=storage)
        serializer = StorageMemberSerializer(membership, many=True)
        return Response(serializer.data)

    def put(self, request, storage_id, username=None):
        """添加一个成员或修改一个成员的权限"""
        storage = Storage.objects.get(id=storage_id)
        check_permission(request.user, storage, OWNER)
        if username is None:
            username = request.data['username']
            user = get_object_or_404(User, username=username)
            request.data.update({'user': user, 'storage': storage.id,
                                 'permission': storage.default_permission})
            serializer = MembershipSerializer(data=request.data)
            serializer.is_valid()
            serializer.save()
        else:
            permission = request.data['permission']
            membership = Membership.objects.get(user__username=username, storage=storage)
            membership.permission = permission
            membership.save()
        return Response()

    def delete(self, request, storage_id, username):
        """删除一个成员"""
        storage = Storage.objects.get(id=storage_id)
        check_permission(request.user, storage, READ)
        membership = Membership.objects.get(user__username=username, storage=storage)
        membership.delete()
        return Response()
