from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from apps.core.models import UserProfile

User = get_user_model()


class LoginForm(AuthenticationForm):
    """Форма входа в аккаунт."""
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'placeholder': 'username',
            'class': 'w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-white/30 focus:border-emerald-300/50 focus:outline-none transition-colors',
        }),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-white/30 focus:border-emerald-300/50 focus:outline-none transition-colors',
        }),
    )


class SignupForm(UserCreationForm):
    """Форма регистрации нового пользователя."""
    first_name = forms.CharField(
        label='Имя',
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ваше имя',
            'class': 'w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-white/30 focus:border-emerald-300/50 focus:outline-none transition-colors',
        }),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'you@example.com',
            'class': 'w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-white/30 focus:border-emerald-300/50 focus:outline-none transition-colors',
        }),
    )

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'username',
            'class': 'w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-white/30 focus:border-emerald-300/50 focus:outline-none transition-colors',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Минимум 8 символов',
            'class': 'w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-white/30 focus:border-emerald-300/50 focus:outline-none transition-colors',
        })
        # Убираем password2 — используем только одно поле пароля (как в шаблоне)
        del self.fields['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email


class ProfileForm(forms.Form):
    """Форма редактирования профиля."""
    first_name = forms.CharField(
        label='Имя',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-white focus:border-emerald-300/50 focus:outline-none transition-colors',
        }),
    )
    email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-white focus:border-emerald-300/50 focus:outline-none transition-colors',
        }),
    )
    bio = forms.CharField(
        label='О себе',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Расскажите о себе',
            'class': 'w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-white focus:border-emerald-300/50 focus:outline-none transition-colors resize-none',
        }),
    )
    github = forms.CharField(
        label='GitHub',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'username',
            'class': 'flex-1 rounded-r-lg border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-white/30 focus:border-emerald-300/50 focus:outline-none transition-colors',
        }),
    )
    twitter = forms.CharField(
        label='Twitter',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'username',
            'class': 'flex-1 rounded-r-lg border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-white/30 focus:border-emerald-300/50 focus:outline-none transition-colors',
        }),
    )
    website = forms.URLField(
        label='Сайт',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://yoursite.com',
            'class': 'w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-white/30 focus:border-emerald-300/50 focus:outline-none transition-colors',
        }),
    )
    old_password = forms.CharField(
        label='Текущий пароль',
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-white/30 focus:border-emerald-300/50 focus:outline-none transition-colors',
        }),
    )
    new_password = forms.CharField(
        label='Новый пароль',
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Минимум 8 символов',
            'class': 'w-full rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-white/30 focus:border-emerald-300/50 focus:outline-none transition-colors',
        }),
    )
