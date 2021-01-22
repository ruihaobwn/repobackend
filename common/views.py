from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view
from rest_framework.views import APIView
from rest_framework import exceptions
from django.contrib.auth import login, logout, authenticate
from rest_framework.authentication import BaseAuthentication
from rest_framework import status, viewsets
from django.contrib.auth.models import User
from common.serializers import UserSerializer
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['get'])
    def current_user(self, request):
        user = request.user
        results = {}
        results['name'] = user.first_name
        results['avatar'] = "https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png"
        return Response(results)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    print('1')
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"status":"ok", "currentAuthority": "guest"})
    else:
        return Response(status=401, data={"currentAuthority": "guest"})


@api_view()
def logout_view(request):
    logout(request)
    return Response()
