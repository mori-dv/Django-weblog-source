from django.views.generic import ListView, DetailView
from account.models import User
from account.mixins import AuthorAccessMixin
from django.shortcuts import get_object_or_404
from .models import Article, Category
# Create your views here.


# home page
class ArticleListView(ListView):
    model = Article
    queryset = Article.objects.published()
    paginate_by = 3


class ArticleDetailView(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(), slug=slug)


class ArticlePreviewView(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


class CategoryList(ListView):
    paginate_by = 2
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        global category 
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.article.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    template_name = 'blog/author_list.html'
    paginate_by = 3

    def get_queryset(self):
        global author 
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context
