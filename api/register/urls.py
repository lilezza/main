from django.urls import path
from .views import UserRegistrationView , UserProfileView , UserLoginView ,UserLogoutView , ProtectedView , MyTokenObtainPairView , MyTokenRefreshView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('' , UserRegistrationView.as_view() , name = 'register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('login/' , UserLoginView.as_view() , name = 'login') ,
    path('logout/' , UserLogoutView.as_view() , name = 'logout'),
    # path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    # path('api/protected/' , ProtectedView.as_view() , name = 'protected_view'),


]
