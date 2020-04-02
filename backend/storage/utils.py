from user.models import User
from .models import Identifier, Membership, Storage
from guardian.shortcuts import assign_perm


def create_storage(user: User, name: str = "文件", is_personal_storage: bool = False):
    identifier = Identifier.objects.create(name=name, owner=user)
    storage = Storage.objects.create(root_identifier=identifier, is_personal_storage=is_personal_storage)
    Membership.objects.create(user=user, storage=storage)
    assign_perm('read', user, storage)
    assign_perm('write', user, storage)
    if not is_personal_storage:
        assign_perm('add_user', user, storage)
        assign_perm('remove_user', user, storage)
        assign_perm('modify_user_permission', user, storage)