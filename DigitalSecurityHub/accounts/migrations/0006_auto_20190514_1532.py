# Generated by Django 2.2 on 2019-05-14 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20190514_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(default='UDistrict', max_length=100),
        ),
    ]