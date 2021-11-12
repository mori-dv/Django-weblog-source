from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


UserAdmin.fieldsets[2][1]['fields'] = (
    'is_active',
    'is_staff',
    'is_superuser',
    'is_author',
    'vip_user',
    'groups',
    'user_permissions'
)
UserAdmin.list_display += ('is_author', 'is_vip_user')
UserAdmin.ordering = ['-is_staff', '-is_author', '-vip_user', 'first_name']
UserAdmin.list_filter += ('is_author',)
admin.site.register(User, UserAdmin)
