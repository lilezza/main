from django.conf import settings
from rest_framework import serializers
from .models import Register
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import requests


class RecaptchaV3Validator:
    def __call__(self , value):
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data = {
                'secret' : settings.RECAPTCHA_PRIVATE_KEY ,
                'response' : value
            }
        )
        result = response.json()
        if not result.get('success') or result.get('score' , 0) < settings.RECAPTCHA_REQUIRED_SCORE:
            raise serializers.ValidationError('reCAPTCHA validation failed')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)
    recaptcha = serializers.CharField(write_only = True , validators = [RecaptchaV3Validator()])

    class Meta :
        model = User
        fields = ["first_name" , "last_name" , "username" , "email" , "password" , "confirm_password" , "recaptcha"]

    def validate(self ,data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("password do not match!")
        return data

    def create(self , validated_data):
        validated_data.pop('confirm_password')
        validated_data.pop('recaptcha')
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
