from django.contrib.auth.models import User
from rest_framework import serializers, permissions

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        permissions_classes = [permissions.AllowAny]

    def create(self, validated_data):
        print(validated_data)
        user = User(
            email = validated_data['email'],
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user 