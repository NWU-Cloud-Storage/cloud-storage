'''
Share 检查器
'''
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import ParseError
from rest_framework.exceptions import PermissionDenied

from share.models import Share

def check_exist_share(url):
    share = get_object_or_404(Share, url=url)
    return share

def check_password(pwd, share):
    if not pwd == share.password:
        raise ParseError('密码错误')
