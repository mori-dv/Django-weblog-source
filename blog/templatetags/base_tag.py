from django import template
from django.db.models import Count, Q
from ..models import Category, Article
from datetime import datetime, timedelta
register = template.Library()


@register.simple_tag
def title():
    return "وبلاگ من"


@register.inclusion_tag('blog/partials/category_navbar.html')
def category_navbar():
    return {
        'category': Category.objects.all().filter(situation=True)
    }


@register.inclusion_tag('registration/paretials/link.html')
def active_link(request, link_name, content, classes):
    return {
        'request': request,
        'link_name': link_name,
        'link': 'account:{}'.format(link_name),
        'content': content,
        'classes': classes
    }


@register.inclusion_tag('blog/partials/popular_posts.html')
def popular_posts():
    last_month = datetime.today() - timedelta(days=30)
    return {
        'popular_posts': Article.objects.published().annotate(
            count=Count('hits', filter=Q(articlehit__date__gt=last_month))
        ).order_by('-count', '-modified')
    }