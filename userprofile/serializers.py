from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from userprofile.models import UserProfile, SocialAccount
from django.contrib.auth.models import User


class SocialMediaConnectSerializer(serializers.ModelSerializer):
    """
    * Here we create a User using Social Media Credentials (e.g. Facebook, Google+, Twitter)
    """
    class Meta:
        model = UserProfile
        exclude = ("user", "social_account")

    def create(self, validated_data):
        social_id = validated_data["social_id"]
        network_name = validated_data["network_name"]
        username = validated_data["username"]

        try:
            client = UserProfile.objects.get(social_account__network_id=social_id)
            if validated_data["username"] == validated_data["social_id"]:
                username = client.user.username
        except ObjectDoesNotExist:
            pass

        email = validated_data.get("email", "")
        first_name = validated_data("first_name", "")
        last_name = validated_data("last_name", "")

        if email == "":
            email = client.user.email if client.user.email else ""
        if first_name == "":
            first_name = client.user.first_name if client.user.first_name else ""
        if last_name == "":
            last_name = client.user.last_name if client.user.last_name else ""

        # Check if User already exists.
        try:
            """
            Check if Client Social ID already exists (in case Username has been changed).
            If Social ID exists, change the User's 'old' username into 'current' username.
            Then proceed storing Client's data.
            """
            get_client_social_id = UserProfile.objects.get(social_account__network_id=social_id)
            client_username = get_client_social_id.user.username

            user = User.objects.get(username=client_username)
            get_current_username = username
            user.username = get_current_username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            social_id, is_created = SocialAccount.objects.get_or_create(network_id=social_id,
                                                                        network_name=network_name)
            client = UserProfile.objects.create(user=user,
                                                social_account=social_id.id)
            client.save()

            Token.objects.get_or_create(user=user)

            return user

        # Else, create a new User and save his credentials.
        except ObjectDoesNotExist:
            # Check if username already exists. Then continue saving User's data.
            # Or proceed with default.
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                user = User.objects.create(email=email,
                                           username=username,
                                           first_name=first_name,
                                           last_name=last_name)
                user.set_unusable_password()
                user.save()
            social_id = SocialAccount.objects.create(network_id=social_id,
                                                     network_name=network_name)
            social_id.save()
            client = UserProfile.objects.create(user=user,
                                                social_account=social_id)
            client.save()
            Token.objects.get_or_create(user=user)
            return user


class LoginSerializer(serializers.ModelSerializer):
    """
    * Checks if logged in User has a token. Creates a token for the User if none exists.
    """
    class Meta:
        model = UserProfile

    def create(self, validated_data):
        try:
            user = User.objects.get(username=validated_data["username"])
            Token.objects.get_or_create(user=user)
            return user
        except ObjectDoesNotExist:
            pass


class ManualRegisterSerializer(serializers.ModelSerializer):
    """
    * Here we create a User from the default registration form
    """
    class Meta:
        model = UserProfile
        exclude = ("user", "social_account")

    def create(self, validated_data):
        username = validated_data["username"]       # required
        password = validated_data["password"]       # required
        email = validated_data["email"]             # required
        first_name = validated_data["first_name"].title()   # required
        last_name = validated_data["last_name"].title()     # required
        social_id = ""                              # ignored
        network_name = ""                           # ignored

        try:
            user = User.objects.create(email=email,
                                       username=username,
                                       first_name=first_name,
                                       last_name=last_name)
            user.set_password(password)
            user.check_password(password)
            user.save()

            social_id = SocialAccount.objects.create(network_id=social_id,
                                                     network_name=network_name)
            social_id.save()

            client = UserProfile.objects.create(user=user,
                                                social_account=social_id)
            client.save()

            Token.objects.get_or_create(user=user)
            return user
        except ObjectDoesNotExist:
            pass
