from django.contrib import admin
from .models import SendData, SendDataButtons, Users, Questions, QuestionValues, Answers, DocsPage, DocsKeys,CustomUser

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class SendDataButtonsAdmin(admin.StackedInline):
    model = SendDataButtons
    extra = 1

class SendDataAdmin(admin.ModelAdmin):
    inlines = [SendDataButtonsAdmin]

class UsersAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'tg_firstname', 'user_status')

class KeysAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active')

class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'page' ,'is_active')

class QuestionValuesAdmin(admin.StackedInline):
    model = QuestionValues
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionValuesAdmin]


admin.site.register(SendData, SendDataAdmin)
admin.site.register(Questions, QuestionAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(DocsPage,PageAdmin)
admin.site.register(DocsKeys,KeysAdmin)

admin.site.unregister(User)
admin.site.register(CustomUser, UserAdmin)
