# Generated by Django 2.2.17 on 2020-12-28 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20201225_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerinvoice',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_invoice', to='customer.Customer', verbose_name='客户名称'),
        ),
        migrations.AlterField(
            model_name='customershop',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_shop', to='customer.Customer', verbose_name='客户名称'),
        ),
    ]
