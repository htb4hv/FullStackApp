from django import template

register = template.Library()

@register.filter(name='range')
def filter_range(value):
    # Ensure value is an integer
    try:
        return range(int(value))
    except (TypeError, ValueError):
        return range(0)