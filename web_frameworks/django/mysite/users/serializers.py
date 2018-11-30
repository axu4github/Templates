
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('tenant', 'owner', 'created', 'modified')


class UserSerializer(serializers.ModelSerializer):

    userprofile = UserProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'userprofile')

    def create(self, validated_data):
        tenant = validated_data.pop('userprofile')["tenant"]
        user = User.objects.create(**validated_data)
        try:
            UserProfile.objects.create(tenant=tenant, user=user)
        except Exception as e:
            user.delete()
            raise e

        return user
