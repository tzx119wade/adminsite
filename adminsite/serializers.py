from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework import serializers



class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(min_length=6,max_length=20)
    password = serializers.CharField(min_length=6,max_length=20)

    class Meta:
        model = User
        fields = "__all__"


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
        depth = 1

class GeneralSerializers(serializers.Serializer):
    username = serializers.CharField(min_length=6, max_length=20)
    password = serializers.CharField(min_length=6, max_length=20)
    email = serializers.EmailField()
    CHOOSE = [
        ('author','author'),
        ('normal','normal'),
    ]
    identity = serializers.ChoiceField(choices=CHOOSE, allow_blank=False)

class UserInfoSerializers(serializers.Serializer):
    username = serializers.CharField(min_length=6, max_length=20)
    password = serializers.CharField(min_length=6, max_length=20)
    profile_image = serializers.CharField()
    nick_name = serializers.CharField()
