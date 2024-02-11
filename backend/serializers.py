from rest_framework import serializers
from .models import File
from django.contrib.auth.models import User

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'user', 'file', 'uploaded_at']



class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()        
class FileDownloadSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()    