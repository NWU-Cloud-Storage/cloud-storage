"""
通用检查器
"""
from rest_framework.exceptions import ParseError

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

def check_is_int(num):
    """
    检查参数是否可转化为整数\n
    合格则返回转化后的整数\n
    """
    try:
        return int(num)
    except:
        raise ParseError()

def check_all_int(ls):
    """
    检查列表内是否全部都可转化为整数\n
    合格则返回转化后的整数列表\n
    """
    ret = list()
    for item in ls:
        try:
            ret.append(int(item))
        except:
            raise ParseError()
    return ret
