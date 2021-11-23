from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from blog.models import Article


class FieldMixin:
    def dispatch(self, request, *args, **kwargs):
        self.fields = [
            "title",
            "category",
            "imgage",
            "subtitle",
            "describtion",
            "slug",
            "modified",
            'is_special',
            "situation"
        ]
        if request.user.is_superuser:
            self.fields.append('author')

        return super().dispatch(request, *args, **kwargs)


class FormValidMixin:
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user

        if not self.object.situation == 'i':
            self.object.situation = 'd'

        return super().form_valid(form)


class AuthorAccessMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user and article.situation in ['b', 'd'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('اجازه دیدن این صفحه را ندارید!')


class AuthorsAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect('account:profile')
        else:
            return redirect('login')


class SuperUserAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
