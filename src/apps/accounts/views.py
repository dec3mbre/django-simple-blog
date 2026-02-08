from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from apps.blog.models import Article
from apps.core.models import UserProfile

from .forms import LoginForm, ProfileForm, SignupForm


def login_view(request):
    """Вход в аккаунт."""
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            next_url = request.GET.get('next', 'accounts:profile')
            return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def signup_view(request):
    """Регистрация нового пользователя."""
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создаём профиль для нового пользователя
            UserProfile.objects.create(user=user)
            # Автоматически входим после регистрации
            auth.login(request, user)
            return redirect('accounts:profile')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile_view(request):
    """Страница профиля пользователя."""
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            # Обновляем данные пользователя
            user.first_name = form.cleaned_data['first_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Обновляем профиль
            profile.bio = form.cleaned_data['bio']
            profile.github = form.cleaned_data['github']
            profile.twitter = form.cleaned_data['twitter']
            profile.website = form.cleaned_data['website']
            profile.save()

            # Смена пароля (если заполнены оба поля)
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            if old_password and new_password:
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    # Повторно авторизуем, чтобы сессия не сбросилась
                    auth.update_session_auth_hash(request, user)
                    messages.success(request, 'Пароль успешно изменён.')
                else:
                    messages.error(request, 'Текущий пароль указан неверно.')

            messages.success(request, 'Профиль обновлён.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(initial={
            'first_name': user.first_name,
            'email': user.email,
            'bio': profile.bio,
            'github': profile.github,
            'twitter': profile.twitter,
            'website': profile.website,
        })

    published_articles = Article.objects.filter(
        author=user, status=Article.Status.PUBLISHED
    ).order_by('-created_at')

    draft_articles = Article.objects.filter(
        author=user, status=Article.Status.DRAFT
    ).order_by('-updated_at')

    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile,
        'published_articles': published_articles,
        'draft_articles': draft_articles,
        'published_count': published_articles.count(),
    })


@login_required
@require_POST
def logout_view(request):
    """Выход из аккаунта."""
    auth.logout(request)
    return redirect('blog:index')
