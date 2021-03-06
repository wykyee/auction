# Generated by Django 3.1.1 on 2020-11-24 22:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auction', '0004_auto_20200914_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='post',
            name='initial_bet',
            field=models.PositiveIntegerField(verbose_name='Начальная ставка'),
        ),
        migrations.AlterField(
            model_name='post',
            name='main_image',
            field=models.ImageField(upload_to='auction/images', verbose_name='Отображаемая картинка'),
        ),
        migrations.AlterField(
            model_name='post',
            name='permanent_price',
            field=models.PositiveIntegerField(verbose_name='Цена выкупа'),
        ),
        migrations.AlterField(
            model_name='postimage',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_images', to='auction.post'),
        ),
    ]
