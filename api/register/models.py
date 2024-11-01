from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class Register(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    username = models.CharField(max_length = 50 , unique = True)
    email = models.EmailField(max_length = 254 , unique = True)
    password = models.CharField(max_length = 128 )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # هش کردن رمز عبور قبل از ذخیره‌سازی
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super(Register, self).save(*args, **kwargs)
