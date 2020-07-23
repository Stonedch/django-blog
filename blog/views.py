from . import models

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.shortcuts import get_object_or_404


def post_list(request):
    object_list = models.Post.published.all()
    paginator = Paginator(object_list, 2)
    page = request.GET.get("page")

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "page": page,
        "posts": posts,
    }

    return render(request, "blog/post/list.html", context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(models.Post, slug=post, status="published", publish__year=year, publish__month=month, publish__day=day)
    return render(request, "blog/post/detail.html", {"post": post})
