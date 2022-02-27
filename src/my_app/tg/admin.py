from django.contrib import admin
from .models import SendData, SendDataButtons, Users, Questions, QuestionValues, Answers

class AnswerAdmin(admin.StackedInline):
    model = Answers
    extra = 1

class SendDataButtonsAdmin(admin.StackedInline):
    model = SendDataButtons
    extra = 1

class SendDataAdmin(admin.ModelAdmin):
    inlines = [SendDataButtonsAdmin]

class UsersAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]
    list_display = ('tg_id', 'tg_firstname', 'user_status')

class QuestionValuesAdmin(admin.StackedInline):
    model = QuestionValues
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionValuesAdmin]


admin.site.register(SendData, SendDataAdmin)
admin.site.register(Questions, QuestionAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(Answers)
