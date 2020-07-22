from . import views
from .apps import BlogConfig

from django.urls import path

app_name = BlogConfig.name

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/", views.post_detail, name="post_detail"),
]
