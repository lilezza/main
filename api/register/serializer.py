from django.conf import settings
from rest_framework import serializers
from .models import Register , CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
import requests


# class RecaptchaV3Validator:
#     def __call__(self , value):
#         response = requests.post(
#             'https://www.google.com/recaptcha/api/siteverify',
#             data = {
#                 'secret' : settings.RECAPTCHA_PRIVATE_KEY ,
#                 'response' : value
#             }
#         )
#         result = response.json()
#         if not result.get('success') or result.get('score' , 0) < settings.RECAPTCHA_REQUIRED_SCORE:
#             raise serializers.ValidationError('reCAPTCHA validation failed')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)
    # recaptcha = serializers.CharField(write_only = True , validators = [RecaptchaV3Validator()])

    class Meta :
        model = Register
        fields = ["shop_name" , "email" , "password" , "confirm_password" , "phone_number"]

    def validate(self ,data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("password do not match!")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        custom_user = CustomUser.objects.create_user(
        username=validated_data['email'],
        email=validated_data['email'],
        password=validated_data['password'],
        shop_name=validated_data['shop_name'],
    )

    # ذخیره در مدل Register
        Register.objects.create(
            user=custom_user,
            shop_name=validated_data['shop_name'],
            email=validated_data['email'],
            password=validated_data['password'],  # اینجا باید پسورد هش‌شده باشد
            phone_number=validated_data['phone_number']
        )

        return custom_user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # یا مدل مورد نظر شما که به طور سفارشی ساخته شده است
        fields = ['id', 'username', 'email', 'phone_number']


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

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']

        # پیدا کردن کاربر با ایمیل از مدل Register
        try:
            user = Register.objects.get(email=email)
        except Register.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        # بررسی رمز عبور
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect credentials.")

        return user
