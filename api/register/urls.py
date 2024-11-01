from django.urls import path
from .views import UserRegistrationView , UserProfileView , UserLoginView ,UserLogoutView

urlpatterns = [
    path('' , UserRegistrationView.as_view() , name = 'register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('login/' , UserLoginView.as_view() , name = 'login') ,
    path('logout/' , UserLogoutView.as_view() , name = 'logout'),

]