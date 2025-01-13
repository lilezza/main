from django.contrib import admin

# Register your models here.

from .models import Register ,CustomUser
# from django.contrib.auth.models import User

@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'email', 'phone_number']

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
