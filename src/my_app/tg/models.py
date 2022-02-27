from django.db import models
from . import MediaType, MessagePlase, UsersStatus, QuestionType

class Questions(models.Model):
    question = models.TextField(null=False,blank=False, help_text='Savol matni')
    question_type = models.SmallIntegerField(choices=QuestionType.CHOICES, default=QuestionType.text, help_text='Savol turi')
    is_active = models.BooleanField(default=False, null=False, blank=False, help_text="Buni belgilasayiz savol foydalanuvchiga boradi")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Savollar'

class QuestionValues(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    value = models.CharField(max_length=100, null=False, blank=False, help_text='Savol varianti')

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Savolning javoblari'


class Users(models.Model):
    tg_id = models.IntegerField(null=False, blank=False)
    tg_username = models.CharField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    tg_firstname = models.CharField(max_length=150, null=True, blank=True)
    tg_lastname = models.CharField(max_length=150, null=True, blank=True)
    user_status = models.SmallIntegerField(choices=UsersStatus.CHOICES, default=UsersStatus.simple_user)

    def __str__(self):
        return self.tg_firstname if self.tg_firstname else str(self.tg_id)

    class Meta:
        verbose_name = 'Foydalanuvchilar'

class SendData(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False,help_text="Bu botga chiqmaydi shunchaki o'zingiz uchun")
    text = models.TextField(null=True, blank=True)
    post_file = models.FileField(upload_to='files', blank=True, null=True)
    media_type = models.SmallIntegerField(choices=MediaType.CHOICES,default=MediaType.TEXT)
    message_place = models.SmallIntegerField(choices=MessagePlase.CHOICES, default=MessagePlase.start)
    is_active = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Kommandalardan keyin chiqadigan malumotlar'

class SendDataButtons(models.Model):
    send_data = models.ForeignKey(SendData, on_delete=models.CASCADE)
    text = models.CharField(max_length=50, null=False, blank=False, help_text='Button texti')
    link = models.CharField(max_length=100,blank=False, null=False, help_text='Button boradigan kanal yokim accaunt silkasi')

    def __str__(self):
        return self.text

class Answers(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    question_id = models.IntegerField(null=False, blank=False)
    question = models.CharField(max_length=200, null=False, blank=False, help_text='Berilgan savol')
    answer = models.CharField(max_length=200, null=False, blank=False, help_text='Olingan javob')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Foydalanuvchilar javoblari'
