# Generated by Django 5.1.2 on 2024-10-22 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_customuser_followers_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='followers_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Seguidores'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='following_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Seguindo'),
        ),
    ]
