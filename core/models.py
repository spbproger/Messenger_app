from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.html import format_html


class Author(AbstractUser):
    phone = models.BigIntegerField(verbose_name="Номер телефона", null=True, blank=True)
    birthday = models.DateField(verbose_name="День рождения", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    edited = models.DateTimeField(auto_now=True, verbose_name="Дата последнего редактирования")

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.fullname}'


class Publication(models.Model):
    heading = models.CharField(max_length=30, verbose_name="Заголовок публикации")
    pdescription = models.TextField(verbose_name="Текст публикации")
    img = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True, verbose_name="Изображение")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    comment = models.ManyToManyField('Comment', blank=True, related_name="comments", verbose_name="Комментарий")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    edited = models.DateTimeField(auto_now=True, verbose_name="Дата последнего редактирования")

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def author_link(self):
        author = self.author
        url = reverse("admin:core_author_changelist") + str(author.pk)
        return format_html(f'<a href="{url}">{author}</a>')

    author_link.short_description = "Автор"

    def __str__(self):
        return self.pdescription[:30]


class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    cdescription = models.TextField(verbose_name="Текст комментария")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    edited = models.DateTimeField(auto_now=True, verbose_name="Дата последнего редактирования")

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('edited', 'author')

    def author_link(self):
        author = self.author
        url = reverse("admin:core_author_changelist") + str(author.pk)
        return format_html(f'<a href="{url}">{author}</a>')

    author_link.short_description = "Автор"

    @property
    def author_comment(self):
        return f'{self.author}: {self.cdescription[:20]}...'

    def __str__(self):
        return f'{self.author_comment}'
