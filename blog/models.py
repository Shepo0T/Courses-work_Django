from django.db import models

from mailings.models import NULLABLE


class Blog(models.Model):
    """Модель блога"""
    title = models.CharField(max_length=50, verbose_name='заголовок')
    text = models.TextField(verbose_name='текст')
    image = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    count_of_view = models.IntegerField(default=0, verbose_name='Просмотры')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')

    def __str__(self):
        return f'{self.title} {self.count_of_view}'