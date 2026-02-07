from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Article


def article_list(request):
    query = request.GET.get('q', '')
    if query:
        articles = Article.objects.filter(
            status=Article.Status.PUBLISHED,
            title__icontains=query
        ).order_by('-created_at')
    else:
        articles = Article.objects.filter(status=Article.Status.PUBLISHED).order_by('-created_at')

    paginator = Paginator(articles, 6)  # Показывать по 6 статей на странице
    page: int = request.GET.get('page')
    articles = paginator.get_page(page)
    
    return render(request, 'blog/article_list.html', {
        'articles': articles
    })

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status=Article.Status.PUBLISHED)

    return render(request, 'blog/article_detail.html', {
        'article': article
    })