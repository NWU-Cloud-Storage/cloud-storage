'''
工具方法
'''

def sub_dict(src: dict, keys):
    '''
    求交集，获取子字典
    '''
    return {key: value for key, value in src.items() if key in keys}

def detail(msg, others=None):
    '''
    把报错信息包装一下
    '''
    rtn = {'detail':msg}
    if others:
        rtn['others'] = others
    return rtn
