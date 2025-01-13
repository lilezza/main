from rest_framework import status , permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics , serializers
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.authentication import SessionAuthentication
from .serializer import UserRegistrationSerializer, UserLoginSerializer , UserProfileSerializer
from django.contrib.auth import authenticate
from .models import Register
from django.contrib.auth.models import User
from django.contrib.auth import login, logout , get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from register.models import CustomUser , Register

#################
#past code
# class UserRegistrationView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         return Response({"message": "Registration page"}, status=status.HTTP_200_OK)

#     def post(self , request):
#         serializer = UserRegistrationSerializer(data = request.data)
#         if serializer.is_valid():
#             # ذخیره‌سازی کاربر جدید
#             user = serializer.save()

#             # ایجاد JWT توکن برای کاربر
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)

#             # ارسال توکن و اطلاعات کاربر به فرانت‌اند
#             return Response(
#                 {
#                     "access_token": access_token,
#                     "refresh_token": str(refresh),
#                     "message": "User registered successfully",
#                     "user": {
#                         "email": user.email,
#                         "username": user.username
#                     }
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         # در صورتی که داده‌های وارد شده معتبر نباشند
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
########################

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # ساخت یوزر در مدل CustomUser
            custom_user = CustomUser.objects.create_user(
                username=serializer.validated_data['email'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                shop_name=serializer.validated_data['shop_name']
            )

            # ذخیره پروفایل Register
            Register.objects.create(
                user=custom_user,
                shop_name=serializer.validated_data['shop_name'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],  # هش‌شده
                phone_number=serializer.validated_data['phone_number']
            )

            # تولید توکن JWT
            refresh = RefreshToken.for_user(custom_user)
            return Response(
                {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "message": "User registered successfully",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




##########################
#past code
# class UserProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         token = request.headers.get('Authorization').split(' ')[1]
#         decoded_token = AccessToken(token)
#         user_id = decoded_token['user_id']
#         try:
#             # ابتدا جستجو در مدل Register
#             user = Register.objects.get(id=user_id)
#         except Register.DoesNotExist:
#             try:
#                 # اگر در Register نبود، جستجو در مدل CustomUser
#                 user = CustomUser.objects.get(id=user_id)
#             except CustomUser.DoesNotExist:
#                 return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

#         # بعد از پیدا کردن کاربر، داده‌ها را ارسال می‌کنیم
#         serializer = UserRegistrationSerializer(user)
#         return Response({'user': serializer.data}, status=status.HTTP_200_OK)
#######################

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # استفاده از پروفایل مرتبط
            profile = Register.objects.get(user=request.user)
        except Register.DoesNotExist:
            return Response(
                {"detail": "User not found", "code": "user_not_found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserRegistrationSerializer(profile)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)









################################
#past code
# User = get_user_model()
# class UserLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         # دریافت ایمیل و پسورد از درخواست
#         email = request.data.get('email')
#         password = request.data.get('password')

#         # بررسی وجود ایمیل و پسورد
#         if not email:
#             return Response({"error": "Email is required."}, status=400)
#         if not password:
#             return Response({"error": "Password is required."}, status=400)

#         # ابتدا تلاش برای پیدا کردن کاربر از مدل Register
#         try:
#             user = Register.objects.get(email=email)
#         except Register.DoesNotExist:
#             # اگر در مدل Register پیدا نشد، تلاش برای پیدا کردن در مدل User
#             try:
#                 user = User.objects.get(email=email)
#             except User.DoesNotExist:
#                 return Response({"error": "Invalid credentials"}, status=400)

#         # بررسی رمز عبور برای هر دو مدل
#         if not user.check_password(password):
#             return Response({"error": "Invalid credentials"}, status=400)

#         # تولید توکن JWT برای کاربر
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)

#         # ارسال توکن JWT همراه با پیام موفقیت
#         return Response({
#             "message": "Login successful",
#             "access_token": access_token,
#             "refresh_token": str(refresh)
#         })
######################################################

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=400)

        try:
            custom_user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid credentials."}, status=400)

        if not custom_user.check_password(password):
            return Response({"error": "Invalid credentials."}, status=400)

        # تولید توکن JWT
        refresh = RefreshToken.for_user(custom_user)
        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "message": "Login successful",
            },
            status=status.HTTP_200_OK,
        )









class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)



# class ProtectedView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self , request):
#         return Response({"message" : "this is a protected view"})


@method_decorator(csrf_exempt, name='dispatch')
class MyTokenObtainPairView(TokenObtainPairView):
    pass

@method_decorator(csrf_exempt, name='dispatch')
class MyTokenRefreshView(TokenRefreshView):
    pass
