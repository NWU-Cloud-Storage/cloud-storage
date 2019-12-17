'''
share 相关接口的视图
'''
from rest_framework.response import Response
from rest_framework.views import APIView

from my_utils.checker import check_are_same, check_not_same
from my_utils.checker import check_is_int

from user.serializers import TheOtherSerializer

from storage.checker import check_exist_catalogue
from storage.checker import check_is_ancestor
from storage.serializers import CatalogueSerializer
from storage.serializers import BreadcrumbsSerializer

from share.models import Share as ShareModel
from share.checker import check_exist_share
from share.checker import check_password
from share.serializers import ShareSerializer

class ShareToPublic(APIView):
    '''
    share-to-public
    '''
    @staticmethod
    def post(request, src_id):
        '''
        新建一个分享
        '''
        user = request.user.user
        cata = check_exist_catalogue(src_id)
        my_root = user.storage
        check_not_same(my_root, cata)
        check_are_same(my_root, cata.get_root())
        days = request.data.get('duration', None)
        pwd = request.data.get('password', None)
        days = check_is_int(days)

        share = ShareModel.objects.create_by_user(user, cata, days, pwd)
        serializer = ShareSerializer(share)
        return Response(serializer.data)


def _check_session(request, share):
    request.session.clear_expired()
    url = share.url
    # request.session.clear()
    if request.session.get(url, None) is None:
        pwd = request.data.get('password', None)
        check_password(pwd, share)
        request.session[url] = url
    request.session.set_expiry(300)

class Share(APIView):
    '''
    share
    '''
    @staticmethod
    def get(request, url, cata_id=None):
        '''
        查看分享内文件
        '''
        share = check_exist_share(url)
        _check_session(request, share)
        share_root = share.catalogue
        cata = share_root
        if cata_id is not None:
            cata = check_exist_catalogue(cata_id)
        ancestors = check_is_ancestor(share_root, cata)

        the_other_serializer = TheOtherSerializer(share.user)
        share_serializer = ShareSerializer(share)
        bread_serializer = BreadcrumbsSerializer(ancestors, many=True)
        cata_serializer = CatalogueSerializer(cata.get_children(), many=True)
        res = {'breadcrumbs': [], 'content': []}
        res.update(the_other_serializer.data)
        res.update(share_serializer.data)
        breadcrumbs = res['breadcrumbs']
        content = res['content']
        for data in cata_serializer.data:
            content.append(dict(data))
        for data in bread_serializer.data:
            breadcrumbs.append(dict(data))
        return Response(res)

class ShareToMe(APIView):
    '''
    share-to-me
    '''
    @staticmethod
    def post(request, url, src_id, des_id=None):
        '''
        保存分享中的内容到本地
        '''
        share = check_exist_share(url)
        _check_session(request, share)
        share_cata = check_exist_catalogue(src_id)
        check_is_ancestor(share.catalogue, share_cata)

        my_root = request.user.user.storage
        my_cata = my_root
        if des_id is not None:
            my_cata = check_exist_catalogue(des_id)
            check_is_ancestor(my_root, my_cata)

        share_cata.copy_to(my_cata)
        return Response()
