from user.models import User
from .models import Identifier, Membership, Storage
from datetime import datetime

def create_storage(user: User, name: str="文件", is_personal_storage: bool=False):
    identifier = Identifier.objects.create(name=name, owner=user)
    storage = Storage.objects.create(root_identifier=identifier)
    Membership.objects.create(user=user, storage=storage, is_personal_storage=is_personal_storage)