# Generated by Django 3.1.1 on 2020-09-14 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_post_main_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at'], 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AlterModelOptions(
            name='postimage',
            options={'verbose_name': 'Картинка к посту', 'verbose_name_plural': 'Картинки к постам'},
        ),
    ]
