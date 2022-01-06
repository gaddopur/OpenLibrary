from rest_framework import serializers

from .models import BookUser, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BookUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookUser
        fields = '__all__'