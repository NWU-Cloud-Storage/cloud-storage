'''
User 检查器
'''
from django.shortcuts import get_object_or_404

from user.models import User

def check_exist_user(username):
    '''根据username查找user'''
    user = get_object_or_404(User, username=username)
    return user
