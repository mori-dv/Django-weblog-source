from django.urls import path
from .views import ArticleListView, category, ArticleDetailView
app_name = 'blog'
urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('page/<int:page>', ArticleListView.as_view(), name='home'),
    path('article/<slug:slug>', ArticleDetailView.as_view(), name='article_detail'),
    path('category/<slug:slug>', category, name='category'),
    path('category/<slug:slug>/page/<int:page>', category, name='category'),
]
