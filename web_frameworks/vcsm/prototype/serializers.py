from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers

from prototype.models import Tenant, Profile


def is_chinese(char):
    """ 字符是中文 """
    return u"\u4e00" <= char <= u"\u9fff"


def contain_chinese(chars):
    """ 字符中包含中文 """
    for char in chars:
        if is_chinese(char):
            return True

    return False


def validate_contain_chinese(value):
    """ 校验包含中文 """
    if contain_chinese(value):
        raise serializers.ValidationError("can not contain chinese.")

    return value


class BaseSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(BaseSerializer, self).__init__(*args, **kwargs)


class TenantSerializer(BaseSerializer):

    name = serializers.CharField()
    code = serializers.CharField(
        default="",
        validators=[validate_contain_chinese]
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
