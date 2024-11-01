from rest_framework import status , permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.authentication import SessionAuthentication 
from .serializer import UserRegistrationSerializer, UserLoginSerializer
from .models import Register
from django.contrib.auth import login, logout

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Registration page"}, status=status.HTTP_200_OK)

    def post(self , request):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : 'User registered successfully'} , status = status.HTTP_201_CREATED)
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self , request):
        serializer = UserRegistrationSerializer(request.user)
        return Response({'user' : serializer.data} , status = status.HTTP_200_OK)

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
