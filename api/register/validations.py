# validations.py
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email
from django.core.validators import RegexValidator
import re

def custom_validation(data):
    # چک کردن فرمت ایمیل
    email = data.get("email")
    if email:
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_regex, email):
            raise ValidationError("قالب ایمیل نامعتبر است")

    # چک کردن طول پسورد
    password = data.get("password")
    if password and len(password) < 8:
        raise ValidationError("رمز عبور باید حداقل 8 کاراکتر باشد")

    # چک کردن تکرار پسورد
    confirm_password = data.get("confirm_password")
    if password != confirm_password:
        raise ValidationError("گذرواژه ها مطابقت ندارند")

    # اگر تمام چک‌ها موفقیت‌آمیز بود، داده‌های تمیز را برمی‌گرداند
    return data

def validate_email(data):
    try:
        django_validate_email(data.get('email'))
        return True
    except ValidationError:
        raise ValidationError("قالب ایمیل نامعتبر است.")

def validate_password(data):
    password = data.get('password')
    if len(password) < 8:
        raise ValidationError("رمز عبور باید حداقل 8 کاراکتر باشد.")
    return True

def validate_phone_number(phone_number):
    """
    اعتبار سنجی شماره موبایل
    """
    phone_regex = r'^(\+98|0)?9\d{9}$'
    if not re.match(phone_regex , phone_number):
        raise ValidationError("لطفا شماره تلفن صحیح را وارد کنید")
    return True
