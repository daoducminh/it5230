# Generated by Django 3.1.4 on 2020-12-21 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0004_auto_20201221_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='score',
            field=models.IntegerField(),
        ),
    ]
