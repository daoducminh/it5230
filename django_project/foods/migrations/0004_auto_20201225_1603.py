# Generated by Django 3.1.4 on 2020-12-25 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0003_auto_20201225_1553'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'ordering': ['-timestamp']},
        ),
    ]