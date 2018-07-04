from django.core.paginator import Paginator


def handle_pagination(request, data_to_paginate, count=6):
    paginator = Paginator(data_to_paginate, count)
    page = request.GET.get('page')
    paginated_page = paginator.get_page(page)

    return paginated_page
