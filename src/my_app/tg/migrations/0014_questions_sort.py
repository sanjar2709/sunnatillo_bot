# Generated by Django 4.0.2 on 2022-04-10 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg', '0013_alter_users_tg_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='sort',
            field=models.IntegerField(blank=True, default=0, help_text="Bu savol nechanchi o'rinda chiqishini belgilaydi", null=True),
        ),
    ]
