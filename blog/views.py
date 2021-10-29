from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.core.paginator import Paginator
# Create your views here.


# home page
class ArticleListView(ListView):
    model = Article
    queryset = Article.objects.published()
    paginate_by = 3


# each article's page
class ArticleDetailView(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(), slug=slug)


# each category's page
# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, situation=True)
#     article_list = category.article.published()
#     paginator = Paginator(article_list, 3)
#     pages = paginator.get_page(page)
#     context = {
#         'category': category,
#         'articles': pages
#     }
#     return render(request, 'blog/category.html', context)

class CategoryList(ListView):
    paginated_by = 2
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        global category 
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), situation=True, slug=slug)
        return category.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context

class AuthorList(ListView):
    paginated_by = 2
    template_name = 'blog/authorList.html'

    def get_queryset(self):
        global author 
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context