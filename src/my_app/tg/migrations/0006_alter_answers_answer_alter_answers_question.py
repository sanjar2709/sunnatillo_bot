# Generated by Django 4.0.2 on 2022-02-27 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg', '0005_answers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='answer',
            field=models.CharField(help_text='Olingan javob', max_length=200),
        ),
        migrations.AlterField(
            model_name='answers',
            name='question',
            field=models.CharField(help_text='Berilgan savol', max_length=200),
        ),
    ]