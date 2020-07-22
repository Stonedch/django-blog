from . import models

from django.shortcuts import render
from django.shortcuts import get_object_or_404


def post_list(request):
    posts = models.Post.published.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(models.Post, slug=post, status="published", publish__year=year, publish__month=month, publish__day=day)
    return render(request, "blog/post/detail.html", {"post": post})
