import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="markdown")
def markdown_format(text):
    """Convert Markdown text to HTML."""
    return mark_safe(
        markdown.markdown(
            text,
            extensions=[
                "fenced_code",
                "codehilite",
                "tables",
                "nl2br",
                "smarty",
                "toc",
            ],
            extension_configs={
                "codehilite": {"css_class": "highlight", "linenums": False},
            },
        )
    )
