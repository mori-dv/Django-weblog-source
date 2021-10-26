from django.views.generic import ListView, DetailView
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
def category(request, slug, page=1):
    category = get_object_or_404(Category, slug=slug, situation=True)
    article_list = category.article.published()
    paginator = Paginator(article_list, 3)
    pages = paginator.get_page(page)
    context = {
        'category': category,
        'articles': pages
    }
    return render(request, 'blog/category.html', context)
