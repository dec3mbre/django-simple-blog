from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Article


def article_list(request):
    articles = Article.objects.filter(status=Article.Status.PUBLISHED)

    return render(request, 'blog/article_list.html', {
        'articles': articles
    })

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status=Article.Status.PUBLISHED)

    return render(request, 'blog/article_detail.html', {
        'article': article
    })