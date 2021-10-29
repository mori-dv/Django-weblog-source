from django.urls import path
from .views import ArticleListView, CategoryList, ArticleDetailView, AuthorList
app_name = 'blog'
urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('page/<int:page>', ArticleListView.as_view(), name='home'),
    path('article/<slug:slug>', ArticleDetailView.as_view(), name='article_detail'),
    path('category/<slug:slug>', CategoryList, name='category'),
    path('category/<slug:slug>/page/<int:page>', CategoryList, name='category'),
    path('author/<slug:username>', AuthorList, name='author'),
    path('author/<slug:username>/page/<int:page>', AuthorList, name='author'),
]
