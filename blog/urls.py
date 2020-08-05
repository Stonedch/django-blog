from . import views
from .apps import BlogConfig

from django.urls import path

app_name = BlogConfig.name

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("tag/<slug:tag_slug>/", views.PostListView.as_view(), name="post_list_by_tag"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/", views.post_detail, name="post_detail"),
    path("<int:post_id>/share/", views.PostShareView.as_view(), name="post_share"),
]
