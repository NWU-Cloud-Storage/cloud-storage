from rest_framework.views import APIView


class WebDAVAPI(APIView):
    http_method_names = APIView.http_method_names + \
                        ['propfind', 'proppatch', 'lock', 'unlock', 'copy', 'move', 'mkcol']