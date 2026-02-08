from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
import math
from .models import Article, Category


def _reading_time(text):
    """Calculate reading time in minutes (avg 200 wpm)."""
    return max(1, math.ceil(len(text.split()) / 200))


def index(request):
    """Главная страница с featured-статьёй и последними постами."""
    published = Article.objects.filter(
        status=Article.Status.PUBLISHED
    ).order_by('-created_at')

    featured = published.first()
    articles = published.exclude(pk=featured.pk)[:6] if featured else published[:6]

    # Annotate reading time
    for article in articles:
        article.reading_time = _reading_time(article.content)
    if featured:
        featured.reading_time = _reading_time(featured.content)

    return render(request, 'blog/index.html', {
        'featured': featured,
        'articles': articles,
        'total_articles': published.count(),
        'total_categories': Category.objects.count(),
        'total_authors': published.values('author').distinct().count(),
    })


def article_list(request):
    """Все статьи с поиском и фильтрацией по категориям."""
    query = request.GET.get('q', '')
    if query:
        articles = Article.objects.filter(
            status=Article.Status.PUBLISHED,
            title__icontains=query
        ).order_by('-created_at')
    else:
        articles = Article.objects.filter(
            status=Article.Status.PUBLISHED
        ).order_by('-created_at')

    categories = Category.objects.all()

    paginator = Paginator(articles, 9)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    # Annotate reading time
    for article in page_obj:
        article.reading_time = _reading_time(article.content)

    return render(request, 'blog/article_list.html', {
        'articles': page_obj,
        'page_obj': page_obj,
        'categories': categories,
    })


def article_detail(request, slug):
    """Страница отдельной статьи с похожими постами."""
    article = get_object_or_404(
        Article, slug=slug, status=Article.Status.PUBLISHED
    )
    article.reading_time = _reading_time(article.content)

    # Похожие статьи: из той же категории, кроме текущей
    related_articles = Article.objects.filter(
        status=Article.Status.PUBLISHED,
        category=article.category,
    ).exclude(pk=article.pk).order_by('-created_at')[:2] if article.category else []

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'related_articles': related_articles,
    })