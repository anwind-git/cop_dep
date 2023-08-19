# Generated by Django 4.2.1 on 2023-06-11 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
        ('orders', '0003_alter_orders_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organizations.cities', verbose_name='Город'),
        ),
    ]