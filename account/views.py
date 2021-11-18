from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import (
    FieldMixin,
    FormValidMixin,
    AuthorAccessMixin,
    SuperUserAccessMixin
)
from .models import User
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from blog.models import Article
from django.contrib.auth import logout


# Create your views here.
class ArticleList(LoginRequiredMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(LoginRequiredMixin, FieldMixin, FormValidMixin, CreateView):
    model = Article
    template_name = 'registration/article_create_update.html'


class ArticleUpdate(AuthorAccessMixin, FieldMixin, FormValidMixin, UpdateView):
    model = Article
    template_name = 'registration/article_create_update.html'


class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = 'account:home'
    template_name = 'registration/article_delete.html'


class ProfileView(UpdateView):
    model = User
    template_name = 'registration/profile.html'
    fields = [
        'username',
        'email',
        'first_name',
        'last_name',
        'vip_user',
        'is_author'
    ]
    success_url = 'account:profile'

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)
