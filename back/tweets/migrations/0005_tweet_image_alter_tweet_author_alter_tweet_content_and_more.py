# Generated by Django 5.1.2 on 2024-10-23 13:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_alter_tweet_updated_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='tweet_images/', verbose_name='Tweet Image'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tweets', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='content',
            field=models.TextField(verbose_name='Tweet Content'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation Date'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='updated_at',
            field=models.DateTimeField(null=True, verbose_name='Update Date'),
        ),
    ]