from django import template

register = template.Library()

@register.filter
def make_range(num):
    return range(1, num+1)

@register.filter
def make_serial(current_page, index_loop):
    return 5*(current_page-1) + index_loop