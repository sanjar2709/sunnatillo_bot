# Generated by Django 4.0.2 on 2022-03-07 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg', '0009_alter_questionvalues_options_questions_colum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='colum',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
