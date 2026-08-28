from django import template

register = template.Library()

@register.filter(name='make_list_split')
def make_list_split(value, delimiter=','):
    if not value:
        return []
    return [x.strip() for x in value.split(delimiter) if x.strip()]
