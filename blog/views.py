from . import models

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import generic
from django.shortcuts import render
from django.shortcuts import get_object_or_404


class PostListView(generic.ListView):
    queryset = models.Post.published.all()
    context_object_name = "posts"
    paginate_by = 2
    template_name = "blog/post/list.html"


def post_detail(request, year, month, day, post):
    post = get_object_or_404(models.Post, slug=post, status="published", publish__year=year, publish__month=month, publish__day=day)
    return render(request, "blog/post/detail.html", {"post": post})
