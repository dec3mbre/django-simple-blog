import math

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from apps.core.models import Subscriber
from .forms import ArticleForm
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
        articles = articles.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(content__icontains=query)
        )

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
    article = get_object_or_404(Article, slug=slug)

    # Черновики видны только автору
    if article.status != Article.Status.PUBLISHED:
        if not request.user.is_authenticated or request.user != article.author:
            from django.http import Http404
            raise Http404

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

@login_required
def article_create(request):
    """Создание новой статьи."""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.slug = form.generate_unique_slug()
            # Кнопка "Опубликовать" передаёт status=published, иначе — черновик
            article.status = request.POST.get('status', Article.Status.DRAFT)
            article.save()
            if article.status == Article.Status.PUBLISHED:
                return redirect(article.get_absolute_url())
            return redirect('accounts:profile')
    else:
        form = ArticleForm()

    return render(request, 'blog/editor.html', {
        'form': form,
        'editing': False,
    })


@login_required
def article_edit(request, slug):
    """Редактирование существующей статьи (только автор)."""
    article = get_object_or_404(Article, slug=slug, author=request.user)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.status = request.POST.get('status', article.status)
            # Обновляем slug только если заголовок изменился
            if 'title' in form.changed_data:
                article.slug = form.generate_unique_slug()
            article.save()
            if article.status == Article.Status.PUBLISHED:
                return redirect(article.get_absolute_url())
            return redirect('accounts:profile')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'blog/editor.html', {
        'form': form,
        'article': article,
        'editing': True,
    })


@login_required
@require_POST
def article_delete(request, slug):
    """Удаление статьи (только автор, POST)."""
    article = get_object_or_404(Article, slug=slug, author=request.user)
    article.delete()
    messages.success(request, 'Статья удалена.')
    return redirect('accounts:profile')