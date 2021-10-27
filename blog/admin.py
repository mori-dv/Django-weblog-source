from django.contrib import admin, messages
from .models import Article, Category
from django.utils.translation import ngettext

# admin actions
admin.site.disable_action('delete_selected')


@admin.action(description='پست های انتخاب شده منتشر شود')
def make_published(modeladmin, request, queryset):
    updated = queryset.update(situation='p')
    modeladmin.message_user(request, ngettext(
        ' %d مقاله منتشر شد ',
        ' %d مقاله منتشر شدند ',
        updated
    ) % updated, messages.SUCCESS)


@admin.action(description='پست های انتخابی پیش‌نویس شود')
def make_draft(modeladmin, request, queryset):
    updated = queryset.update(situation='d')
    modeladmin.message_user(request, ngettext(
        ' %d مقاله پیش‌نویس شد ',
        ' %d مقاله پیش‌نویس شدند ',
        updated
    ) % updated, messages.SUCCESS)


# Register your models here.
class AdminInterface(admin.ModelAdmin):
    list_display = ('image_tag', 'title', 'category_to_str', 'jmodified', 'author', 'situation')
    actions = [make_published, make_draft]

    def category_to_str(self, obj):
        return ",".join([category.title for category in obj.category.active()])
    category_to_str.short_description = 'دسته‌بندی'


@admin.action(description='دسته‌بندی انتخاب شده نمایش داده شود')
def make_available(modeladmin, request, queryset):
    updated = queryset.update(situation=True)
    modeladmin.message_user(request, ngettext(
        ' %d دسته‌بندی نمایش داده شد ',
        ' %d دسته‌بندی نمایش داده شدند ',
        updated
    ) % updated, messages.SUCCESS)


@admin.action(description='دسته‌بندی انتخاب شده نمایش داده نشود')
def make_unavailable(modeladmin, request, queryset):
    updated = queryset.update(situation=False)
    modeladmin.message_user(request, ngettext(
        ' %d دسته‌بندی از دسترس خارج شد ',
        ' %d دسته‌بندی از دسترس خارج شدند ',
        updated
    ) % updated, messages.SUCCESS)


class CategoryInterface(admin.ModelAdmin):
    list_display = ('position', 'title', 'parent', 'slug', 'situation',)
    actions = [make_available, make_unavailable]


admin.site.register(Article, AdminInterface)
admin.site.register(Category, CategoryInterface)
