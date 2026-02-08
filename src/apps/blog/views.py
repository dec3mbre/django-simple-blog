import math

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from apps.core.models import Subscriber
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
    category_slug = request.GET.get('category', '')

    articles = Article.objects.filter(
        status=Article.Status.PUBLISHED
    ).order_by('-created_at')

    if query:
        articles = articles.filter(title__icontains=query)

    if category_slug:
        articles = articles.filter(category__slug=category_slug)

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
        'current_category': category_slug,
        'search_query': query,
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


@require_POST
def subscribe(request):
    """Подписка на рассылку (AJAX)."""
    email = request.POST.get('email', '').strip()
    if not email:
        return JsonResponse({'ok': False, 'error': 'Email обязателен.'}, status=400)

    _, created = Subscriber.objects.get_or_create(email=email)
    if created:
        return JsonResponse({'ok': True, 'message': 'Вы успешно подписались!'})
    return JsonResponse({'ok': True, 'message': 'Вы уже подписаны.'})