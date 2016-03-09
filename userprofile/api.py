from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework import status
from django.contrib.auth.models import User

from userprofile.models import UserProfile


class UserProfileSerializer(ModelSerializer):

    class Meta:
        model = UserProfile


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]


class ListModelViewSet(ViewSet):
    permission_classes = [IsAdminUser]

    @staticmethod
    def list(request):
        models = [
            {"user": "/v1/admin/user/"},
        ]
        return Response(models, status=status.HTTP_200_OK)


class AdminLoginViewSet(ViewSet):

    @staticmethod
    def create(request):

        username = request.data.get("username", "")
        password = request.data.get("password", "")

        user = User.objects.get(username=username)
        password_valid = user.check_password(password)

        context = {
            "status": "FORBIDDEN",
            "data": {}
        }

        if password_valid:
            if user.is_superuser:
                context["status"] = "GRANTED"
                context["data"] = {
                    "username": user.username,
                    "password": password,
                    "user_id": user.id
                }

        return Response(context, status=status.HTTP_200_OK)