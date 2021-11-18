from django.http import Http404
from django.shortcuts import get_object_or_404
from blog.models import Article


class FieldMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = [
                "title",
                "category",
                "author",
                "imgage",
                "subtitle",
                "describtion",
                "slug",
                "modified",
                'is_special',
                "situation"
            ]
        elif request.user.is_author:
            self.fields = [
                "title",
                "category",
                "imgage",
                "subtitle",
                "describtion",
                "slug",
                "modified"
            ]
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin:
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.situation = 'd'
        return super().form_valid(form)


class AuthorAccessMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user and article.situation in ['b', 'd'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404


class SuperUserAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
