# Generated by Django 4.0.2 on 2022-03-08 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg', '0010_alter_questions_colum'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocsKeys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keys', models.JSONField(default={}, help_text='Bu googda yani accaunt ochilganda beriladigan keyslar')),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Docs Keys',
            },
        ),
    ]
