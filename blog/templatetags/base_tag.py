from django import template
from ..models import Category
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
def active_link(request, link_name, content):
    return {
        'request': request,
        'link_name': link_name,
        'link': 'account:{}'.format(link_name),
        'content': content
    }
