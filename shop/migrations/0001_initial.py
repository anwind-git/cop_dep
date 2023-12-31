# Generated by Django 4.2.1 on 2023-06-06 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorie', models.CharField(db_index=True, max_length=20, verbose_name='Категория')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('queue', models.IntegerField(verbose_name='Очередность')),
            ],
            options={
                'verbose_name': 'категорию ',
                'verbose_name_plural': 'Категории блюд',
                'db_table': 'menu_categories',
            },
        ),
        migrations.CreateModel(
            name='ShelfLife',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shelf_life', models.CharField(max_length=50, verbose_name='Срок годности')),
            ],
            options={
                'verbose_name': 'срок годности',
                'verbose_name_plural': 'сроки годности',
                'db_table': 'shelf_life',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='static/image/%Y/%m/%d/', verbose_name='Изображение')),
                ('product_name', models.CharField(max_length=50, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('short_description', models.CharField(max_length=35, verbose_name='Краткое описание')),
                ('full_description', models.TextField(verbose_name='Полное описание')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('queue', models.IntegerField(default=0, editable=False, verbose_name='Рейтинг')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Обнавлено')),
                ('publication', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('cities', models.ManyToManyField(to='organizations.cities', verbose_name='Города обслуживания')),
                ('menu_categories', models.ManyToManyField(to='shop.menucategories', verbose_name='Категория блюда')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipes', verbose_name='Рецепт')),
                ('shelf_life', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shelflife', verbose_name='Срок годности')),
            ],
            options={
                'verbose_name': 'блюда',
                'verbose_name_plural': 'Блюда',
                'db_table': 'products',
                'ordering': ['id'],
            },
        ),
    ]
