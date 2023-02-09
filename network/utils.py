from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post


def paginatePosts(request, posts, results):

    page = request.GET.get('page')

    paginator = Paginator(posts, results)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)

    left_index = (int(page) - 4) if (int(page) > 4) else 1
    right_index = (int(page) + 5) if (int(page) < paginator.num_pages - 5) else paginator.num_pages + 1
    custom_paginator = range(left_index, right_index)

    return posts, custom_paginator