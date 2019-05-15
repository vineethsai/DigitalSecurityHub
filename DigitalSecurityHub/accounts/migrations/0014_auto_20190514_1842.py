# Generated by Django 2.2 on 2019-05-15 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20190514_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='company',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='state',
            field=models.CharField(max_length=100),
        ),
    ]
