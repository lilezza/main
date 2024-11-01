# validations.py
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email
import re

def custom_validation(data):
    # چک کردن فرمت ایمیل
    email = data.get("email")
    if email:
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_regex, email):
            raise ValidationError("Invalid email format")

    # چک کردن طول پسورد
    password = data.get("password")
    if password and len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")

    # چک کردن تکرار پسورد
    confirm_password = data.get("confirm_password")
    if password != confirm_password:
        raise ValidationError("Passwords do not match")

    # اگر تمام چک‌ها موفقیت‌آمیز بود، داده‌های تمیز را برمی‌گرداند
    return data

def validate_email(data):
    try:
        django_validate_email(data.get('email'))
        return True
    except ValidationError:
        raise ValidationError("Invalid email format.")

def validate_password(data):
    password = data.get('password')
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    return True
