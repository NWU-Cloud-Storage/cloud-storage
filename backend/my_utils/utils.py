"""
工具方法
"""
import random
import string
import datetime
from django.utils import timezone


def sub_dict(src: dict, keys):
    """
    求交集，获取子字典
    """
    return {key: value for key, value in src.items() if key in keys}


def detail(msg, others=None):
    """
    把报错信息包装一下
    """
    rtn = {'detail': msg}
    if others:
        rtn['others'] = others
    return rtn


def gen_url(length):
    """
    生成由数字和字符组成的随机字符串，可用于url，传入参数是字符串长度
    """
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


def after_n_days(n):
    """
    返回一个n天以后的datetime
    """
    now_time = timezone.now()
    return now_time + datetime.timedelta(days=n)
