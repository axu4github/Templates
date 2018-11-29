
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class UserProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
