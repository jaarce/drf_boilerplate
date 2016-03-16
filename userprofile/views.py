from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from django.contrib.auth.models import  User

from userprofile.models import UserProfile
from userprofile.serializers import SocialMediaConnectSerializer, LoginSerializer, ManualRegisterSerializer


class ManualLogin(viewsets.ViewSet):

    @list_route(methods=["post"])
    def form(self, request):
        """
        * Endpoint for manual User Login via username and password.
        :param request:
        :return Response():
        """
        login_data = request.data
        # Try to get username and check if password is correct.
        try:
            user = User.objects.get(username=login_data.get("username"))
            password_valid = user.check_password(login_data.get("password"))
            # If password is correct, get access token.
            if password_valid:
                serializer = LoginSerializer(data=request.data)
                user_data = serializer.create(request.data)
                access_token, is_created = Token.objects.get_or_create(user=user_data)
                return Response({"user_id": user_data.id, "access_token": access_token.key}, status=status.HTTP_202_ACCEPTED)
            # Else, throw exception.
            else:
                return Response({"error": "Wrong Login Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": "Wrong Login Credentials"}, status=status.HTTP_404_NOT_FOUND)


class ManualRegister(viewsets.ViewSet):

    @list_route(methods=["post"])
    def form(self, request):
        """
        * Endpoint for manual registration via email & password
        :param request:
        :return Response():
        """
        user_data = request.data
        is_first = False
        # Check if username or email already exists. If yes, return Error response.
        try:
            try:
                User.objects.get(email=user_data.get("email"))
                return Response({"error": "Email is not available"}, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist as e:
                print("Error: \nDetails: {0}".format(e))

            try:
                User.objects.get(username=user_data.get("username"))
                return Response({"error": "Username is not available"}, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist as e:
                print("Error: \nDetails: {0}".format(e))

        except ObjectDoesNotExist:
            is_first = True

        serializer = ManualRegisterSerializer(data=request.data)
        if serializer.is_valid():
            client_data = serializer.create(request.data)

            try:
                access_token = Token.objects.get(user=client_data)
                return Response({
                    "user_id": client_data.id,
                    "access_token": access_token.token,
                    "is_first": is_first}, status=HTTP_201_CREATED)
            except ObjectDoesNotExist:
                return Response({"error": "HTTP_400_BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=["post"])
    def check(self, request):
        """
        * Endpoint for checking if username exists
        :param request:
        :return Response():
        """
        user_data = request.data
        is_email_existing = False
        is_username_existing = False

        try:
            try:
                User.objects.get(email=user_data.get("email"))
                is_email_existing=True
            except ObjectDoesNotExist as e:
                print("Error: \nDetails: {0}".format(e))

            try:
                User.objects.get(username=user_data.get("username"))
                is_username_existing=True
            except ObjectDoesNotExist as e:
                print("Error: \nDetails: {0}".format(e))
        except ObjectDoesNotExist:
            is_email_existing = False
            is_username_existing = False

        return Response({"is_email_existing": is_email_existing,
                         "is_username_existing": is_username_existing}, status=status.HTTP_200_OK)


class SocialMediaConnectViewSet(viewsets.ViewSet):

    @list_route(methods=["post"])
    def connect(self, request):
        """
        * Endpoint for connecting to social media
        :param request:
        :return Response():
        """
        social_data = request.data
        is_first = False
        # Try to get username and GET or CREATE access token.
        # Then proceed returning user_id and access token.
        try:
            client = UserProfile.objects.get(social_account__network_id=social_data.get("social_id"))
            Token.objects.get_or_create(user=client.user)
        except ObjectDoesNotExist:
            is_first = True

        serializer = SocialMediaConnectSerializer(data=request.data)
        if serializer.is_valid():
            client_data = serializer.create(request.data)
            try:
                # GET Access Token of newly created user
                new_access_token, is_created = Token.objects.get_or_create(user=client_data)
                # upload_avatar(request=request, key=new_access_token)
                return Response({
                    "user_id": new_access_token.user.id,
                    "access_token": new_access_token.key,
                    "is_first": is_first}, status=HTTP_201_CREATED)
            except ObjectDoesNotExist:
                try:
                    # GET Access Token of already existing user
                    client_token = Token.objects.get(user=client.user)
                    return Response({
                        "user_id": client_token.user.id,
                        "access_token": client_token.key,
                        "is_first": is_first}, status=status.HTTP_201_CREATED)
                except ObjectDoesNotExist:
                    return Response({"error": "HTTP_400_BAD_REQUEST"}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=["post"])
    def check_social_id(self, request):
        """
        * Endpoint for checking social ID
        :param request:
        :return Response():
        """
        social_data = request.data
        is_first = False

        try:
            UserProfile.objects.get(social_account__network_id=social_data.get("social_id"))
        except ObjectDoesNotExist:
            is_first = True

        return Response({"is_first": is_first}, status=status.HTTP_200_OK)

    @list_route(methods=["post"])
    def check_username(self, request):
        """
        * Endpoint for checking username
        :param request:
        :return Response():
        """
        social_data = request.data
        is_existing = False

        try:
            UserProfile.objects.get(user__username=social_data.get("username"))
            is_existing = True
        except ObjectDoesNotExist as e:
            print("Error: \nDetails: {0}".format(e))

        return Response({"is_existing": is_existing}, status=status.HTTP_200_OK)

