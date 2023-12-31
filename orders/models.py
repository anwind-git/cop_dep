from django.db import models
from shop.models import Products
from organizations.models import Cities


class Orders(models.Model):
    identifier = models.CharField(max_length=50, verbose_name='Идентификатор')
    city = models.ForeignKey(Cities, on_delete=models.PROTECT, verbose_name='Город')
    phone = models.CharField(max_length=250, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Адрес электронной почты')
    address = models.CharField(max_length=250, verbose_name='Адрес доставки')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Время оплаты')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    work = models.BooleanField(default=False, verbose_name='В работе')
    delivered = models.BooleanField(default=False, verbose_name='Доставлен')

    class Meta:
        ordering = ('-created',)
        db_table = 'orders'
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey('Orders', on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='order_items',
                                verbose_name='Наименование заказа')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кол-во')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'товар'
        verbose_name_plural = 'покупки'

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


class ShippingAddresses(models.Model):
    addresse = models.CharField(max_length=250, verbose_name='Адрес')

    class Meta:
        db_table = 'shipping_addresses'
        verbose_name = 'адрес доставки'
        verbose_name_plural = 'Подсказки, адреса доставки'

    def __str__(self):
        return self.addresse



