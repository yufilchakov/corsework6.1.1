from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=100, verbose_name='Заголовок', help_text='Введите заголовок')
    contents_article = models.TextField(max_length=100, verbose_name='Содержимое статьи')
    image = models.ImageField(upload_to="image/blog", blank=True, null=True, verbose_name='Изображения',
                              help_text='Загрузите изображение')
    number_views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров',
                                               help_text="Укажите количество просмотров")
    date_publication = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Статья блога'
        verbose_name_plural = 'Статьи блога'
