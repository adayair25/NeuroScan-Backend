from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializer import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import JSONParser

# Create your views here.

class UserAPI(APIView):
    permission_classes = [permissions.AllowAny]
    def get (self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if User.objects.filter(username=request.data.get('username')).exists():
            return Response(status=status.HTTP_409_CONFLICT)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class LoginAPI(APIView):
    parser_classes = [JSONParser]
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token)
                    })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
