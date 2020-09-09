from django import template
from django.templatetags.static import static

register = template.Library()
@register.filter(name='ifUrlelseStatic')
def ifUrlelseStatic(value, staticUrl):
    if value:
        return value
    return static(staticUrl)


@register.filter(name='split')
def split(value, seprater):
    return value.split(seprater)


@register.filter(name='index')
def index(value, index):
    return value[index]