from django import template

register = template.Library()

@register.simple_tag
def calculate_precent(item):
    """Сalculate precent for sale"""

    return int((item.price - item.sale_price) * 100 / item.price)

