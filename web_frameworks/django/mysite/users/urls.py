from django.conf.urls import url, include
from rest_framework import routers

from . import views

app_name = 'users'
router = routers.DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
