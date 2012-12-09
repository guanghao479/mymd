from django import template

register = template.Library()

@register.simple_tag
def jsrender(tags):
    if tags:
        return """{{%s}}""" % (tags)
    else:
        return ""
