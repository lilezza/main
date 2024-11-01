from rest_framework import serializers
from .models import Register
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)

    class Meta :
        model = User
        fields = ["first_name" , "last_name" , "username" , "email" , "password" , "confirm_password"]

    def validate(self ,data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("password do not match!")
        return data

    def create(self , validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            first_name = validated_data ['first_name'],
            last_name = validated_data ['last_name'],
            username = validated_data ['username'] ,
            email = validated_data ['email'] ,
            password =validated_data ['password'] ,
        )
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']

        # پیدا کردن کاربر با ایمیل
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        # بررسی رمز عبور
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect credentials.")

        return user
