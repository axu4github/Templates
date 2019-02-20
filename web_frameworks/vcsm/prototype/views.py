from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from prototype.models import Tenant
from prototype.serializers import TenantSerializer, UserSerializer


class BaseViewSet(viewsets.ModelViewSet):
    """ 基础视图管理（为了分离接口和业务建立） """

    def __init__(self, *args, **kwargs):
        super(BaseViewSet, self).__init__(*args, **kwargs)

    def pre_create(self, request):
        """ 对象创建前 """
        return request.data

    def post_create(self, request, response):
        """ 对象创建后 """
        return response.data

    def create(self, request, *args, **kwargs):
        """ 对象创建 """
        request_data = self.pre_create(request)
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = self.post_create(request, serializer)
        return Response(response_data, status=status.HTTP_201_CREATED)


class TenantViewSet(BaseViewSet):
    """ 租户视图 """
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer


class UserViewSet(BaseViewSet):
    """ 用户视图 """
    queryset = User.objects.all()
    serializer_class = UserSerializer
