from django import template

register = template.Library()

@register.filter
def divisibleby(value, arg):
    """Returns the integer division of value by arg"""
    return value // arg

@register.filter
def mod(value, arg):
    """Returns the remainder of value divided by arg"""
    return value % arg
