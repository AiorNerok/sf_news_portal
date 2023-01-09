from django import template


register = template.Library()


@register.filter()
def censor(v):
    return str(v).replace('t', '*')