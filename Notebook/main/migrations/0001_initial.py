# Generated by Django 4.0.3 on 2022-03-08 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, verbose_name='Заметка')),
                ('data', models.PositiveSmallIntegerField(default='202238', verbose_name='Дата')),
                ('category', models.BooleanField(verbose_name='Заметка в календаре')),
            ],
            options={
                'verbose_name': 'Заметка',
                'verbose_name_plural': 'Заметки',
                'ordering': ('-data',),
            },
        ),
    ]
