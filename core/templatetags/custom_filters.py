from django import template

register = template.Library()

@register.filter
def mod(value, arg):
    return value % arg

@register.filter
def div(value, arg):
    return value // arg