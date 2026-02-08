from django import forms
from django.utils.text import slugify
from unidecode import unidecode

from .models import Article, Category


class ArticleForm(forms.ModelForm):
    """Форма создания и редактирования статьи."""

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        empty_label='Выберите категорию',
        widget=forms.Select(attrs={
            'class': 'rounded-lg border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-white/70 focus:border-emerald-300/50 focus:outline-none transition-colors appearance-none cursor-pointer',
        }),
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'hidden',
            'id': 'image-upload',
            'accept': 'image/*',
        }),
    )

    class Meta:
        model = Article
        fields = ['title', 'description', 'category', 'image', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Заголовок статьи',
                'class': 'w-full bg-transparent text-4xl font-semibold placeholder-white/30 border-none focus:ring-0 focus:outline-none',
            }),
            'description': forms.TextInput(attrs={
                'placeholder': 'Краткое описание (опционально)',
                'class': 'w-full bg-transparent text-lg text-white/70 placeholder-white/30 border-none focus:ring-0 focus:outline-none',
            }),
            'content': forms.Textarea(attrs={
                'id': 'editor',
                'class': 'editor-content mono w-full bg-transparent text-base text-white/90 placeholder-white/30 resize-none border-none focus:ring-0 focus:outline-none',
                'placeholder': 'Начните писать...\n\nПоддерживается Markdown:\n# Заголовок\n**жирный** и *курсив*\n- списки\n> цитаты\n`код` и блоки кода',
                'rows': 20,
            }),
        }

    def generate_unique_slug(self):
        """Генерирует уникальный slug из title."""
        base_slug = slugify(unidecode(self.cleaned_data['title']))
        if not base_slug:
            base_slug = 'article'
        slug = base_slug
        counter = 1
        while Article.objects.filter(slug=slug).exclude(pk=self.instance.pk if self.instance.pk else None).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        return slug
