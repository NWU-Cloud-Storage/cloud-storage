from rest_framework.authtoken.views import ObtainAuthToken

class MyTmpAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.set_cookie('token', response.data['token'])
        return response
