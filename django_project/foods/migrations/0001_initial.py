# Generated by Django 3.1.4 on 2021-01-03 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import foods.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish_name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('calories', models.IntegerField()),
                ('is_public', models.BooleanField()),
                ('image', models.ImageField(upload_to=foods.validators.dish_image_path)),
                ('ingredients', models.CharField(max_length=250)),
                ('score', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250)),
                ('mealtime', models.DateTimeField()),
                ('limit', models.IntegerField()),
                ('calories', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField()),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('gender', models.BooleanField()),
                ('diet_factor', models.FloatField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('comment', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.dish')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Menu_Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.dish')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.menu')),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='dishes',
            field=models.ManyToManyField(null=True, through='foods.Menu_Dish', to='foods.Dish'),
        ),
        migrations.AddField(
            model_name='menu',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(weight__gt=0), name='weight_gt_0'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(height__gt=100), name='height_gt_100'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(diet_factor__gt=0), name='diet_factor_gt_0'),
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.CheckConstraint(check=models.Q(score__gt=0), name='rating_score_gt_0'),
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.CheckConstraint(check=models.Q(score__lte=5), name='rating_score_lte_5'),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('user', 'dish')},
        ),
        migrations.AddConstraint(
            model_name='menu_dish',
            constraint=models.CheckConstraint(check=models.Q(count__gt=0), name='count_gt_0'),
        ),
        migrations.AddConstraint(
            model_name='dish',
            constraint=models.CheckConstraint(check=models.Q(calories__gt=0), name='calories_gt_0'),
        ),
        migrations.AddConstraint(
            model_name='dish',
            constraint=models.CheckConstraint(check=models.Q(score__gte=0), name='dish_score_gte_0'),
        ),
        migrations.AddConstraint(
            model_name='dish',
            constraint=models.CheckConstraint(check=models.Q(score__lte=5), name='dish_score_lte_5'),
        ),
    ]
