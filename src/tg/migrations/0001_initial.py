# Generated by Django 4.0.2 on 2022-02-27 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SendData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text="Bu botga chiqmaydi shunchaki o'zingiz uchun", max_length=200)),
                ('text', models.TextField(blank=True, null=True)),
                ('post_file', models.FileField(blank=True, null=True, upload_to='files')),
                ('media_type', models.SmallIntegerField(choices=[(1, 'Text'), (2, 'Photo'), (3, 'Video')], default=1)),
                ('message_place', models.SmallIntegerField(choices=[(1, 'Start Komandasida'), (2, 'Biz haqimizda'), (3, 'Test yakunlanganda')], default=1)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Kommandalardan keyin chiqadigan malumotlar',
            },
        ),
        migrations.CreateModel(
            name='SendDataButtons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(help_text='Button texti', max_length=50)),
                ('link', models.CharField(help_text='Button boradigan kanal yokim accaunt silkasi', max_length=100)),
                ('send_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tg.senddata')),
            ],
        ),
    ]