from django import template

register = template.Library()

@register.filter(name='getattr')
def getattr(var, name):
    return u"%s:%s" % (name,var)