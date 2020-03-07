"""
通用检查器
"""
from rest_framework.exceptions import ParseError
from collections.abc import Iterable


def check_are_same(arg1, arg2):
    """arg1 arg2应该一样"""
    if not arg1 == arg2:
        raise ParseError()


def check_not_same(arg1, arg2):
    """arg1 arg2不应该一样"""
    if arg1 == arg2:
        raise ParseError()


def check_in_list(arg, ls):
    """检查arg应该在ls里"""
    if not arg in ls:
        raise ParseError()


def check_is_none(arg):
    """arg应该为None"""
    if arg is not None:
        raise ParseError()


def check_not_none(arg):
    """arg不应为None"""
    if arg is None:
        raise ParseError()


def check_serializer_is_valid(serializer_cls: type, instance, data):
    """
    检查需要序列化的数据是否合法\n
    合格则返回序列化器\n
    """
    serializer = serializer_cls(instance, data=data)
    if not serializer.is_valid():
        raise ParseError()
    return serializer


def get_int(obj):
    """
    检查参数是否能被转化成整数
    合格则返回转化后的整数或整数列表\n
    """
    if isinstance(obj, Iterable):
        res = list()
        for item in obj:
            try:
                res.append(int(item))
            except ValueError:
                raise ParseError()
    else:
        try:
            return int(obj)
        except ValueError:
            raise ParseError()
