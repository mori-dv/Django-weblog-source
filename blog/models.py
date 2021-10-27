from django.db import models
from django.utils.html import format_html
from django.utils import timezone
from .extentions.utils import jalali_time


# my managers
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(situation='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(situation=True)


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان دسته‌بندی')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='children',
        null=True,
        blank=True,
        default=None,
        verbose_name='زیردسته'
    )
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس دسته‌بندی')
    situation = models.BooleanField(default=True, verbose_name='آیا نمایش ٔداده شود؟')
    position = models.IntegerField(verbose_name='موقعیت')
    objects = CategoryManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی ها'
        ordering = ['parent__id', 'position']


class Article(models.Model):
    CHOICES = (
        ('d', 'پیش‌نویس'),
        ('p', 'منتشرشده'),
    )
    title = models.CharField(max_length=100, verbose_name='سرتیتر')
    category = models.ManyToManyField(Category, verbose_name='دسته‌بندی', related_name='article')
    imgage = models.ImageField('تصویر')
    subtitle = models.TextField(verbose_name="چکیده مطلب")
    describtion = models.TextField(verbose_name="مقاله")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="آدرس پست")
    modified = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    created = models.DateTimeField(auto_now_add=True, verbose_name="زمان تولید")
    update = models.DateTimeField(auto_now=True, verbose_name="زمان ویرایش")
    author = models.CharField(max_length=100, verbose_name="نوشته شده توسط")
    situation = models.CharField(max_length=1, choices=CHOICES, verbose_name="وضعیت پست")
    
    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = 'مقالات'
        ordering = ['title', 'situation']

    def jmodified(self):
        return jalali_time(self.modified)
    jmodified.short_description = "زمان انتشار"

    def image_tag(self):
        return format_html("<img src='{}' width=80 height=60 style='border-radius: 6px;'>".format(self.imgage.url))
    image_tag.short_description = 'تصویر مقاله'

    def __str__(self):
        return self.title
    
    objects = ArticleManager()
