# Generated by Django 3.1.4 on 2020-12-21 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0003_auto_20201220_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dish',
            old_name='owner_id',
            new_name='user_id',
        ),
    ]
