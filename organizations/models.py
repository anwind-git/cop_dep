from django.urls import reverse

from django.db import models


class Organizations(models.Model):
    REG_FORM = (
        ('IP', 'ИП'),
        ('OOO', 'ООО'),
    )

    registration_form = models.CharField(max_length=3, choices=REG_FORM, default='IP', verbose_name='Форма регистрации')
    restaurant = models.ManyToManyField('RestaurantAddresses', blank=False, verbose_name='Адреса ресторанов')
    name_restaurant = models.CharField(max_length=50, blank=True, verbose_name='Название ресторана')
    last_name = models.CharField(max_length=50, blank=False, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, blank=False, verbose_name='Имя')
    middle_name = models.CharField(max_length=50, blank=False, verbose_name='Отчество')
    INN = models.PositiveBigIntegerField(blank=False, verbose_name='ИНН')
    OGRN = models.PositiveBigIntegerField(blank=False, verbose_name='ОГРН')
    phone1 = models.CharField(max_length=20, blank=False, verbose_name='Телефон')
    phone2 = models.CharField(max_length=20, blank=True, verbose_name='Телефон')

    class Meta:
        db_table = 'organizations'
        verbose_name = 'организацию'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name_restaurant


class RestaurantAddresses(models.Model):
    restaurant_addresse = models.CharField(max_length=250, db_index=True, blank=False, verbose_name='Адрес ресторана')

    class Meta:
        db_table = 'restaurant_addresses'
        verbose_name = 'адрес'
        verbose_name_plural = 'Адреса ресторанов'

    def __str__(self):
        return self.restaurant_addresse


class Cities(models.Model):
    city = models.CharField(max_length=100, verbose_name='Город')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        db_table = 'cities'
        verbose_name = 'Город'
        verbose_name_plural = 'Города обслуживания'

    def __str__(self):
        return self.city
