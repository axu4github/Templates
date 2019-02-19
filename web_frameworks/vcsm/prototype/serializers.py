from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from prototype.models import Tenant, Profile


class BaseSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(BaseSerializer, self).__init__(*args, **kwargs)


class TenantSerializer(BaseSerializer):

    name = serializers.CharField()
    code = serializers.CharField(
        default=""
    )

    class Meta:
        model = Tenant
        fields = "__all__"


class ProfileSerializer(BaseSerializer):

    class Meta:
        model = Profile
        fields = "__all__"


class UserSerializer(BaseSerializer):
    userprofile = ProfileSerializer(many=False)
    password = serializers.CharField(
        style={"input_type": "password"},
        default=settings.DEFAUT_USER_PASSWORD,
    )

    class Meta:
        model = User
        fields = ("username", "password", "profile")
        extra_kwargs = {
            "id": {"read_only": True}
        }
