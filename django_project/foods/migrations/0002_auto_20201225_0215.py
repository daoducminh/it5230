# Generated by Django 3.1.4 on 2020-12-25 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='favorites',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='show_diet',
        ),
        migrations.RemoveField(
            model_name='user',
            name='show_email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='show_gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='show_height',
        ),
        migrations.RemoveField(
            model_name='user',
            name='show_phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='show_weight',
        ),
    ]