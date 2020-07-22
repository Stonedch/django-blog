from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="draft", verbose_name="Статус публикации")

    class Meta:
        ordering = ("-publish", )
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
    
    def __str__(self):
        return self.title
