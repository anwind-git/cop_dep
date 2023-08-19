from django.db import models
from organizations.models import RestaurantAddresses


class Employees(models.Model):
    GENDER_CHOICES = (
        (0, '---------'),
        (1, 'Мужчина'),
        (2, 'Женщина')
    )

    restaurant = models.ManyToManyField(RestaurantAddresses, verbose_name='Место работы')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    middle_name = models.CharField(max_length=50, verbose_name='Отчество')
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0, verbose_name='Пол')
    INN = models.PositiveBigIntegerField(null=True, unique=True, verbose_name='ИНН')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    phone = models.CharField(max_length=20, unique=True, verbose_name='Телефон')
    name_telegram = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name='Ник telegram')
    job = models.ManyToManyField('Professions', verbose_name='Должность')
    status1 = models.BooleanField(default=False, verbose_name='Принят на работу')
    job_date = models.DateField(null=True, blank=True, verbose_name='Принят на работу, дата')
    status2 = models.BooleanField(default=False, editable=False, verbose_name='На доставке')
    form_of_payment = models.ForeignKey('FormPayment', on_delete=models.PROTECT, verbose_name='Форма оплаты')
    salary = models.IntegerField(verbose_name='Оклад/Оплата')
    about_me = models.TextField(verbose_name='О сотруднике')

    class Meta:
        db_table = 'employees'
        verbose_name = 'сотрудника'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.last_name


class Professions(models.Model):
    profession = models.CharField(max_length=100, db_index=True, blank=False, verbose_name='Должность')

    class Meta:
        db_table = 'professions'
        verbose_name = 'должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.profession


class FormPayment(models.Model):
    form_payment = models.CharField(max_length=50, db_index=True, blank=False, verbose_name='Форма оплаты')

    class Meta:
        db_table = 'form_payment'
        verbose_name = 'форму оплаты'
        verbose_name_plural = 'Форма оплаты'

    def __str__(self):
        return self.form_payment
