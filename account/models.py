from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    is_author = models.BooleanField(default=False, verbose_name='وضعیت‌ نویسندگی')
    vip_user = models.DateTimeField(default=timezone.now, verbose_name="مدت زمان کاربر ویژه")

    def is_vip_user(self):
        if self.vip_user >= timezone.now():
            return True
        else:
            return False
    is_vip_user.short_description = 'عضو ویژه'
    is_vip_user.boolean = True


