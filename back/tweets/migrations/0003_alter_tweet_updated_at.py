# Generated by Django 5.1.2 on 2024-10-21 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Data de Atualização'),
        ),
    ]