from django.urls import reverse
from django.db import models
from recipes.models import Recipes
from organizations.models import Cities


class Products(models.Model):
    image = models.ImageField(upload_to='static/image/%Y/%m/%d/', verbose_name='Изображение')
    product_name = models.CharField(max_length=50, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    short_description = models.CharField(max_length=35, verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, verbose_name='Рецепт')
    shelf_life = models.ForeignKey('ShelfLife', on_delete=models.CASCADE, verbose_name='Срок годности')
    price = models.IntegerField(verbose_name='Цена')
    cities = models.ManyToManyField(Cities, verbose_name='Города обслуживания')
    menu_categories = models.ManyToManyField('MenuCategories', verbose_name='Категория блюда')
    queue = models.IntegerField(editable=False, default=0, verbose_name='Рейтинг')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Обнавлено')
    publication = models.BooleanField(default=True, verbose_name='Опубликовано')

    class Meta:
        db_table = 'products'
        verbose_name = 'блюда'
        verbose_name_plural = 'Блюда'
        ordering = ['id']

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('product', kwargs={'post_slug': self.slug})


class MenuCategories(models.Model):
    categorie = models.CharField(max_length=20, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    queue = models.IntegerField(verbose_name='Очередность')

    class Meta:
        db_table = 'menu_categories'
        verbose_name = 'категорию '
        verbose_name_plural = 'Категории блюд'

    def __str__(self):
        return self.categorie

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class ShelfLife(models.Model):
    shelf_life = models.CharField(max_length=50, verbose_name='Срок годности')

    class Meta:
        db_table = 'shelf_life'
        verbose_name = 'срок годности'
        verbose_name_plural = 'сроки годности'

    def __str__(self):
        return self.shelf_life
