from . import models
from . import forms
from django_blog import settings

from django.core import mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.views import generic
from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404

from taggit.models import Tag


class PostListView(generic.View):
    def get(self, request, tag_slug=None):
        page_number = request.GET.get("page", 1)
        object_list = models.Post.published.all()

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            object_list = object_list.filter(tags__in=[tag])

        paginator = Paginator(object_list, 3)
        page = paginator.get_page(page_number)

        context = {
            "page": page,
        }

        return render(request, "blog/post/list.html", context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(models.Post, slug=post, status="published", publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = None

    if request.method == "POST":
        comment_form = forms.CommentPostForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        else:
            comment_form = forms.CommentPostForm()
    
    context = {
        "post": post,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
    }

    return render(request, "blog/post/detail.html", context)


class PostShareView(generic.View):
    template_name = "blog/post/share.html"

    def get(self, request, post_id):
        post = get_object_or_404(models.Post, id=post_id, status="published")
        form = forms.EmailPostForm()

        context = {
            "post": post,
            "form": form,
        }

        return render(request, self.template_name, context)

    def post(self, request, post_id):
        post = get_object_or_404(models.Post, id=post_id, status="published")
        form = forms.EmailPostForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            message = f"\"{post.title}\" was succesfuly sent to {cleaned_data['to']}."
            self.__send_mail(request, post, cleaned_data)
            messages.add_message(request, messages.INFO, message)

        return redirect(reverse("blog:post_share", args=[post_id]))
    
    def __send_mail(self, request, post, cleaned_data):
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cleaned_data['name']} ({cleaned_data['email']}) recommendsyou reding {post.title}"
            body = f"Read \"{post.title}\" at {post_url}\n\n{cleaned_data['name']}'s comments: {cleaned_data['comments']}."
            mail.send_mail(subject, body, settings.EMAIL_HOST_USER, [cleaned_data["to"]])
