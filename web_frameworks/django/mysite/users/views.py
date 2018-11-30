from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User

from .serializers import UserSerializer, UserProfileSerializer
from .models import UserProfile


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        self.request_data = request.data.dict()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = serializer.data
        response_data.update(self.profile)
        headers = self.get_success_headers(response_data)
        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        try:
            profile_serializer = UserProfileSerializer(data={
                "user": user.id,
                "tenant": self.request_data.get("tenant")
            })
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()
            self.profile = profile_serializer.data
        except Exception as e:
            user.delete()
            raise e
