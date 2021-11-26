from django.contrib.auth import views
from django.conf.urls import url
from django.urls import path
from .views import (
    ArticleList,
    ArticleCreate,
    ArticleUpdate,
    ArticleDelete,
    ProfileView,
    UserList
)

app_name = 'account'
urlpatterns = [
    path('', ArticleList.as_view(), name='home'),
    path('article/create', ArticleCreate.as_view(), name='article_create'),
    path('article/update/<int:pk>', ArticleUpdate.as_view(), name='article_update'),
    path('article/delete/<int:pk>', ArticleDelete.as_view(), name='article_delete'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('users', UserList.as_view(), name='user_list')
]