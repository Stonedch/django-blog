from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Черновой вариант"),
        ("published", "Опубликованный"),
    )
    title = models.CharField(max_length=256, verbose_name="Загаловок")
    slug = models.SlugField(max_length=256, unique_for_date="publish", verbose_name="Семантический URL")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", verbose_name="Автор")
    body = models.TextField(verbose_name="Содержание")
    publish = models.DateTimeField(default=timezone.now, verbose_name="Дата и время публикации статьи")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания статьи")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата и время обновления статьи")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="draft", verbose_name="Статус публикации")

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ("-publish", )
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    def __str__(self):
        return self.title
