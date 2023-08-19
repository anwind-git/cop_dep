from django import template

register = template.Library()


@register.simple_tag()
def custom_tag():
    value = True
    return value


@register.simple_tag()
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')
