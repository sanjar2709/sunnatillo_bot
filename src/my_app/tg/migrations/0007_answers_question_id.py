# Generated by Django 4.0.2 on 2022-02-27 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg', '0006_alter_answers_answer_alter_answers_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='question_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
