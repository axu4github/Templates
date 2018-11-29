from rest_framework import viewsets

from .serializers import UserProfileSerializer
from .models import UserProfile


class UserViewSet(viewsets.ModelViewSet):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
