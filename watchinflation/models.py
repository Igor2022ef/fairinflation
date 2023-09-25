from django.db import models
from django.urls import reverse


class Articles(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    photo = models.ImageField(blank=True, upload_to="photos/%Y/%m/%d/", verbose_name='Рисунок графика')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория', null=True)
    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        ordering = ['id']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('category', kwargs={'cat_id': self.pk})
        return reverse('category', kwargs={'cat_slug': self.slug})



class Buildgraph(models.Model):
    date_numb = models.DateField(auto_now=False, auto_now_add=False)
    name_product = models.CharField(max_length=150)
    av_cost = models.PositiveIntegerField(null=True)
    av_qantity = models.PositiveIntegerField(null=True)
    sum_money = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name_product


# class Buildgraph(models.Model):
#     name_product = models.DateField(auto_now=False, auto_now_add=False)
#     cost = models.PositiveIntegerField(null=True)
#     weight = models.CharField(max_length=150)
#     date = models.DateField(auto_now=False, auto_now_add=False)
#     shop = models.TextField(blank=True)
#
#     def __str__(self):
#         return self.name_product




