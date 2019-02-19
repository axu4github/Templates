from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from prototype.models import Tenant
from prototype.serializers import TenantSerializer, UserSerializer


class BaseViewSet(viewsets.ModelViewSet):
    """ 基础视图管理（为了分离接口和业务建立） """

    def __init__(self, *args, **kwargs):
        super(BaseViewSet, self).__init__(*args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     request_data = request.data
    #     self.pre_create(request_data)
    #     controller = self.get_controller()
    #     response_data = controller.create(request_data)
    #     self.post_create(request_data, response_data)
    #     return Response(response_data, status=status.HTTP_201_CREATED)


class TenantViewSet(BaseViewSet):
    """ 租户视图 """
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    # def create(self, request, *args, **kwargs):
    #     request_data = request.data
    #     serializer = self.get_serializer(data=request_data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(
    #         serializer.data,
    #         status=status.HTTP_201_CREATED,
    #         headers=headers)


class UserViewSet(BaseViewSet):
    """ 用户视图 """
    queryset = User.objects.all()
    serializer_class = UserSerializer
