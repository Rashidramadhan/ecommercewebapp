# Generated by Django 3.0 on 2019-12-09 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20191208_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverydetailsmodel',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='deliverydetailsmodel',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]