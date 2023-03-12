from django import template

register = template.Library()

@register.filter(name='round_by_2')
def round_by_2(value):
    return round(value,2)