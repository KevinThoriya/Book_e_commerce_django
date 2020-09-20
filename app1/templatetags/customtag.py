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


@register.filter(name='range_for_carousel')
def range_for_carousel(total_length, divider):
    total_length = int(total_length)
    divider = int(divider)
    print(total_length, divider)
    full_caro = (total_length % divider)
    extra_caro = 1 if (total_length - divider*full_caro) else 0
    print(range(full_caro + extra_caro))
    return range(full_caro + extra_caro)
