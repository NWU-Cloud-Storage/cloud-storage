'''
跨仓库相关接口的视图
'''
from rest_framework.views import APIView
from rest_framework.response import Response

from my_utils.checker import check_are_same
from my_utils.checker import check_not_none
from my_utils.checker import check_all_int

from group.checker import check_exist_group
from group.checker import check_user_in_group

from storage.checker import check_exist_catalogue
from storage.checker import check_are_siblings_and_in_root

def _check_src_ids(src_ids):
    check_not_none(src_ids)
    return check_all_int(src_ids)

def _check_src_and_des(src_root, src_ids, des_root, des_id):

    des_cata = des_root
    if des_id:
        des_cata = check_exist_catalogue(des_id)
    check_are_same(des_cata.get_root(), des_root)

    src_catas = check_are_siblings_and_in_root(src_ids, src_root)

    return src_catas, des_cata

class SaveToMe(APIView):
    '''
    save-to-me 相关接口的视图类
    '''
    @staticmethod
    def put(request, group_id, des_id=None):
        '''
        将群组仓库内文件保存到个人仓库。
        '''
        my_self = request.user.user
        group = check_exist_group(group_id)
        check_user_in_group(my_self, group)

        my_root = my_self.storage
        group_root = group.storage
        src_ids = _check_src_ids(request.data.getlist('id', None))
        src_catas, des_cata = _check_src_and_des(group_root, src_ids, my_root, des_id)

        for cata in src_catas:
            cata.copy_to(des_cata)
        return Response()

class UploadToGroup(APIView):
    '''
    upload-to-group 相关接口的视图类
    '''
    @staticmethod
    def put(request, group_id, des_id=None):
        '''
        将个人仓库内文件保存到群组仓库。
        '''
        my_self = request.user.user
        group = check_exist_group(group_id)
        check_user_in_group(my_self, group)

        my_root = my_self.storage
        group_root = group.storage
        src_ids = _check_src_ids(request.data.getlist('id', None))
        src_catas, des_cata = _check_src_and_des(my_root, src_ids, group_root, des_id)

        for cata in src_catas:
            cata.copy_to(des_cata)
        return Response()
