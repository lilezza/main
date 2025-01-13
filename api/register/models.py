from django.contrib.auth.models import AbstractUser , BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model


# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    shop_name = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return self.shop_name if self.shop_name else self.username

class Register(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE , null=True , blank=True)
    shop_name = models.CharField(max_length = 50 , unique = True)
    email = models.EmailField(max_length = 254 , unique = True)
    password = models.CharField(max_length = 128 )
    phone_number = models.CharField(max_length = 13 , unique = True)

    def __str__(self):
        return self.shop_name

    def check_password(self, raw_password):
        # مقایسه پسورد با پسورد هش‌شده
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        # هش کردن رمز عبور قبل از ذخیره‌سازی
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super(Register, self).save(*args, **kwargs)


# def save(self, *args, **kwargs):
#     if not self.password.startswith('pbkdf2_'):
#         self.password = make_password(self.password)
#     print(f"Hashed password: {self.password}")  # چاپ هش پسورد
#     super(Register, self).save(*args, **kwargs)
