from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def handle_pagination(request, data_to_paginate):
    paginator = Paginator(data_to_paginate, 6)
    page = request.GET.get('page')
    paginated_page = paginator.get_page(page)

    return paginated_page
