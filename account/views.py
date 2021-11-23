from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .mixins import (
    FieldMixin,
    FormValidMixin,
    AuthorAccessMixin,
    SuperUserAccessMixin,
    AuthorsAccessMixin
)
from .models import User
from .forms import ProfileForm
from blog.models import Article


# Create your views here.
class ArticleList(AuthorsAccessMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(AuthorsAccessMixin, FieldMixin, FormValidMixin, CreateView):
    model = Article
    template_name = 'registration/article_create_update.html'


class ArticleUpdate(AuthorAccessMixin, FieldMixin, FormValidMixin, UpdateView):
    model = Article
    template_name = 'registration/article_create_update.html'


class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = 'registration/article_delete.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)
    
    def get_form_kwargs(self):
        kwargs = super(ProfileView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')