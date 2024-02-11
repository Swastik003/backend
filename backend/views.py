from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .serializers import FileSerializer,UserSignupSerializer,EmailVerificationSerializer,FileDownloadSerializer
from .models import File,Member
from django.conf import settings
from cryptography.fernet import Fernet
from django.urls import reverse 
import random
import string
from django.core.mail import send_mail


class Login(APIView):

    def post(self, request):
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)

                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class Upload(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):

        member = request.user.person.get() 
        is_ops_user = member.is_ops_user 
        print(is_ops_user,member)
        if request.user.is_authenticated and is_ops_user:    
            serializer = FileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
             return Response({"error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Signup(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            encrypted_url = self.encrypt_url(request, user)
            return Response({'encrypted_url': encrypted_url}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def encrypt_url(self, request, user):
        key = settings.ENCRYPTION_KEY  
        cipher_suite = Fernet(key)
        url = "/user/{}/".format(user.id) 
        encrypted_url = cipher_suite.encrypt(url.encode()).decode()
        return encrypted_url
       
class EmailVerification(APIView):
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            verification_code = self.generate_verification_code()
            self.send_verification_code( email,verification_code)
            return Response({"message": "Verification code sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_verification_code(self):

        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def send_verification_code(self,email, verification_code):

        subject = 'Verification code '
        message = f'Your verification code is: {verification_code}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [email]
        send_mail(subject, message, from_email, to_email) 
class Download(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        member = request.user.person.get() 
        is_ops_user = member.is_ops_user 
        print(is_ops_user,member)
        serializer = FileDownloadSerializer(data=request.data)
        if serializer.is_valid() and is_ops_user==False:
            file_id = serializer.validated_data['file_id']
            file_obj = get_object_or_404(File, id=file_id)
            file_path = file_obj.file.path
            print(file_path)

            encrypted_url = self.encrypt_url(file_path)
            return Response({"encrypted_url": encrypted_url}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def encrypt_url(self, url):
        key = settings.ENCRYPTION_KEY  
        cipher_suite = Fernet(key)
        encrypted_url = cipher_suite.encrypt(url.encode()).decode()
        return encrypted_url    
      
class FileList(APIView):

    def get(self, request):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)          