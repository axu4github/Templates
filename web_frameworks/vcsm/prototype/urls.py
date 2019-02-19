from django.conf.urls import url, include
from rest_framework import routers

from prototype.views import TenantViewSet, UserViewSet

app_name = "prototype"

router = routers.DefaultRouter()
router.register(r'tenants', TenantViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
