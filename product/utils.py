from django.core.paginator import Paginator
from django.db.models import F

from product.models import Item


def handle_pagination(request, data_to_paginate):
    paginator = Paginator(data_to_paginate, 6)
    page = request.GET.get('page')
    paginated_page = paginator.get_page(page)

    return paginated_page


def queryset_with_locale(request):
    """Get Item queryset based on locale.

    :param request - request obj
    :return QuerySet obj based on locale
    """

    locale = request.LANGUAGE_CODE

    return Item.objects.annotate(title=F('title_' + locale), description=F('description_' + locale))
