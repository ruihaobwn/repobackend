from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework import status, viewsets
from django.contrib.auth.models import User
from common.serializers import UserSerializer
from rest_framework.decorators import action


class BaseResponse(object):
    def __init__(self):
        self.code = 1000
        self.msg = ""
        self.data=None
        self.token = ""

    @property
    def dict(self):
        return self.__dict__


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


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # 自定义返回结果的格式
        ret = BaseResponse()
        # 从request中获取数据, 数据格式必须为 {"username":"用户名","password":"密码"}
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            # 获取user对象
            user = serializer.validated_data['user']
            # 每次用户登录时先删除Token再重新生成Token
            Token.objects.filter(user=user).delete()
            # 生成新的Token
            token, created = Token.objects.get_or_create(user=user)
            # 自定义返回内容
            ret.msg = "登录成功！"
            # 编写好User对象的序列化器
            ret.token = token.key
        else:
            # 登录失败时返回的内容
            ret.code = 1013
            ret.msg = "登录失败！用户名或密码错！"
        return Response(ret.dict)


class LogoutView(APIView):

    def get(self, request):
        ret = BaseResponse()
        try:
            # 退出时删除用户登录时生成的Token
            Token.objects.filter(user=request.user).delete()
            ret.msg = "退出成功！"
        except Exception as e:
            ret.code = 1013
            ret.msg = str(e)
        return Response(ret.dict)


