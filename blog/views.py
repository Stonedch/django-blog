from . import models
from . import forms
from django_blog import settings

from django.core import mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.views import generic
from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404


class PostListView(generic.ListView):
    queryset = models.Post.published.all()
    context_object_name = "posts"
    paginate_by = 2
    template_name = "blog/post/list.html"


def post_detail(request, year, month, day, post):
    post = get_object_or_404(models.Post, slug=post, status="published", publish__year=year, publish__month=month, publish__day=day)
    return render(request, "blog/post/detail.html", {"post": post})


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
