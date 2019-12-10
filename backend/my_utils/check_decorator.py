'''
通用检查装饰器
'''
from rest_framework import status
from rest_framework.response import Response

from my_utils.utils import detail

def check_add_request_post(func):
    '''
    从request中获取request_post\n
    需要 request\n
    新加 request_post\n
    '''
    def inner(request, **kwargs):
        request_post = request.POST
        return func(
            request=request,
            request_post=request_post,
            **kwargs
        )
    return inner

def check_serializer_is_valid(instance_name: str, serializer_cls: type, data_name: str):
    '''
    检查需要序列化的数据是否合法\n
    参数 instance_name, serializer_cls, data_name\n
    含义 model实例名, 序列化类, 表单数据名\n
    新加 [model实例名]_serializer\n
    '''
    def middle(func):
        def inner(**kwargs):
            serializer = serializer_cls(kwargs[instance_name], data=kwargs[data_name])
            if not serializer.is_valid():
                return Response(
                    detail("数据不合法。", serializer.errors),
                    status.HTTP_400_BAD_REQUEST
                )
            kwargs[instance_name+'_serializer'] = serializer
            return func(**kwargs)
        return inner
    return middle

def check_keys_are_in_dict(keys: list, dict_name: list):
    '''
    检查dict中是否拥有全部的keys\n
    参数 keys_name, dict_name\n
    含义 keys列表, dict名\n
    新加 所有[dict_name]_[str(key)]\n
    '''
    def middle(func):
        def inner(**kwargs):
            a_dict = kwargs[dict_name]
            for key in keys:
                if not a_dict.__contains__(key):
                    return Response(
                        detail("数据不合法。"),
                        status.HTTP_400_BAD_REQUEST
                    )
                kwargs[dict_name+'_'+str(key)] = a_dict[key]
            return func(**kwargs)
        return inner
    return middle

def check_a_not_eq_b(a_name: str, b: str, error_msg=None):
    '''
    检查 not a == b\n
    参数 a_name, b_name, error_msg\n
    含义 a变量名, b变量名, 报错信息
    '''
    if not error_msg:
        error_msg = "数据不合法。"
    def middle(func):
        def inner(**kwargs):
            a = kwargs[a_name]
            if a == b:
                return Response(
                    detail(error_msg),
                    status.HTTP_400_BAD_REQUEST
                )
            return func(**kwargs)
        return inner
    return middle
