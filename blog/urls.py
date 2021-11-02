from django.urls import path
from .views import ArticleListView, CategoryList, ArticleDetailView, AuthorList
app_name = 'blog'
urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('page/<int:page>', ArticleListView.as_view(), name='home'),
    path('article/<slug:slug>', ArticleDetailView.as_view(), name='article_detail'),
    path('category/<slug:slug>', CategoryList.as_view(), name='category'),
    path('category/<slug:slug>/page/<int:page>', CategoryList.as_view(), name='category'),
    path('author/<slug:username>', AuthorList.as_view(), name='author'),
    path('author/<slug:username>/page/<int:page>', AuthorList.as_view(), name='author'),
]
