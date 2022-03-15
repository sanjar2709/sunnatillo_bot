import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from django.shortcuts import render
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from .models import SendData, SendDataButtons, Users, Questions, QuestionValues, Answers, DocsPage, DocsKeys
# -----------------------------sends function
def go_message(context,user_id, message, reply_murkup):
    context.bot.send_message(chat_id=user_id, text=message,reply_markup=reply_murkup, parse_mode='HTML',
                             disable_web_page_preview=True)

def send_photo(context, user_id, photo, caption=None, reply_mukup=None):
    try:
        context.bot.send_photo(chat_id=user_id, photo=photo, caption=caption, reply_markup=reply_mukup, parse_mode='HTML' )
    except Exception as e:
        print("error send_photo", e)

def send_video(context, user_id, message, video, buttons):
    context.bot.send_video(chat_id=user_id, video=video, caption=message, supports_streaming=True, reply_markup=buttons)

def delete_message_user(context,user_id, message_id):
    context.bot.delete_message(chat_id=user_id, message_id=message_id)

def start(update, context):
    user_data = update.message.from_user
    try:
        user = Users.objects.get(tg_id=user_data.id)
    except:
        user = user_save_data(user_data)

    buttons = ReplyKeyboardMarkup([['🏢 Savol javob', '🏢 Biz haqimizda']], one_time_keyboard=True, resize_keyboard=True)

    text = f"""Assalomu aleykum <b>{user_data.first_name}</b>"""
    go_message(context, user_data.id, text, buttons)
    send_commands(user_id=user_data.id, status=1, context=context)



def text_function(update, context):
    context_data = context.user_data.get('dataa', [])

    user_status = context.user_data.get('user_status', 1)
    message_id = update.message.message_id
    user = update.message.from_user
    state = context.user_data.get('state', 0)
    text = update.message.text

    if text == '🏢 Biz haqimizda':
        send_commands(user_id=user.id, context=context, status=2)
    elif text == '🏢 Savol javob':
        context.user_data['state'] = 100
        questions = Questions.objects.filter(is_active=True)
        data = []
        for ques in questions:
            data.append(ques)
        if data:
            question = data[0]
            del data[0]
            context.user_data['questions'] = data
            context.user_data['question_id'] = question.id
            send_question(question=question, context=context, user_id=user.id, message_id=message_id)
        else:
            go_message(context=context, user_id=user.id, message='Hozircha savollar yoq ❌', reply_murkup=None)
    elif state == 100:
        questions = context.user_data['questions']
        question_id = context.user_data['question_id']

        context_data.append({ "user_id":user.id, "question_id":question_id, "text":text})
        context.user_data['dataa'] = context_data

        if user_status == 1:
            userr = Users.objects.get(tg_id=user.id)
            userr.user_status = 2
            userr.save()
            context.user_data['user_status'] = 2

        if questions:
            question = questions[0]
            del questions[0]
            context.user_data['questions'] = questions
            context.user_data['question_id'] = question.id
            send_question(question=question, context=context,user_id=user.id, message_id=message_id)
        else:
            context.user_data['state'] = 0
            send_commands(user_id=user.id, status=3, context=context)
            answer_save(context=context, user_id=user.id)
    else:
        send_commands(user_id=user.id, status=1, context=context)

def calback_function(update, context):
    context_data = context.user_data.get('dataa', [])
    user_status = context.user_data.get('user_status', 1)

    message_id = update.callback_query.message.message_id
    state = context.user_data.get('state',0)
    user = update.callback_query.from_user
    data_sp = update.callback_query.data.split('_')

    if state == 100 and data_sp[0] == 'question':
        questions = context.user_data['questions']
        question_id = context.user_data['question_id']

        context_data.append({"user_id":user.id, "question_id":question_id, "value":int(data_sp[1])})
        context.user_data['dataa'] = context_data
        if user_status == 1:
            userr = Users.objects.get(tg_id=user.id)
            userr.user_status = 2
            userr.save()
            context.user_data['user_status'] = 2

        if questions:
            question = questions[0]
            del questions[0]
            context.user_data['questions'] = questions
            context.user_data['question_id'] = question.id
            send_question(question=question, context=context, user_id=user.id, message_id=message_id, state=state)
        else:
            delete_message_user(context, user.id, message_id)
            context.user_data['state'] = 0
            send_commands(user_id=user.id, status=3, context=context)
            answer_save(context=context, user_id=user.id)
    else:
        send_commands(user_id=user.id, status=1, context=context)


def send_question(question, context, user_id, message_id, state=None):
    if question.question_type == 1:
        buttons = None
    elif question.question_type == 2:
        try:
            question_values = QuestionValues.objects.filter(question=question.id)
            buttons = [[InlineKeyboardButton(text=question_value.value, callback_data=f"question_{question_value.id}")] for question_value in question_values]
            buttons = InlineKeyboardMarkup(buttons)
        except:
            buttons = None
    else:
        pass
    if state:
        delete_message_user(context, user_id, message_id)
    go_message(context=context,user_id=user_id, message=question.question, reply_murkup=buttons)

def send_commands(user_id, status, context):
    try:
        sendData = SendData.objects.filter(message_place=status, is_active=True).first()
    except:
        sendData = []

    if sendData:
        try:
            sendDataButton = SendDataButtons.objects.filter(send_data=sendData.id)
        except:
            sendDataButton = []

        if sendDataButton:
            buttons = [[InlineKeyboardButton(text=button.text, url=button.link)] for button in sendDataButton]
        else:
            buttons = []
        if sendData.media_type == 1:
            go_message(context=context,user_id=user_id, message=sendData.text, reply_murkup=None) if not buttons else go_message(context=context,user_id=user_id, message=sendData.text, reply_murkup=InlineKeyboardMarkup(buttons))
        elif sendData.media_type == 2:
            send_photo(context=context, user_id=user_id, caption=sendData.text,photo=open(sendData.post_file.path, 'rb'), reply_mukup=None) if not buttons else send_photo(context=context, user_id=user_id, caption=sendData.text,photo=open(sendData.post_file.path, 'rb'), reply_mukup=InlineKeyboardMarkup(buttons))
        elif sendData.media_type == 3:
            send_video(context=context, user_id=user_id, message=sendData.text, video=open(sendData.post_file.path, 'rb'), buttons=None) if not buttons else send_video(context=context, user_id=user_id, message=sendData.text, video=open(sendData.post_file.path, 'rb'), buttons=InlineKeyboardMarkup(buttons))
    else:
        go_message(context=context,user_id=user_id,message="Bazaga malumot kiritish kerak", reply_murkup=None)

def user_save_data(user_data):
    user = Users()
    user.tg_id = user_data.id
    try:
        user.phone_number = user_data.phone_number
    except:
        user.phone_number = ''

    try:
        user.tg_username = user_data.username
    except:
        user.tg_username = ''

    try:
        user.tg_firstname = user_data.first_name
    except:
        user.tg_firstname = ''

    try:
        user.tg_lastname = user_data.lastname
    except:
        user.tg_lastname = ''

    user.save()
    return user

def answer_save(context, user_id):
    question_values = context.user_data.get('dataa', [])
    for quest in question_values:
        text = quest.get('text', None)
        value = quest.get('value', None)
        question_id = quest.get('question_id')
        user_id = quest.get("user_id")

        user = Users.objects.get(tg_id=user_id)
        question = Questions.objects.get(pk=question_id)

        if text:
            AnswerSaved(context=context,user_id=user_id, value=text, colum=question.colum)
        elif value:
            question_value = QuestionValues.objects.get(pk=value)
            AnswerSaved(context=context,user_id=user_id, value=question_value.value, colum=question.colum)

def AnswerSaved(context, user_id, value, colum):
    colum_answer = context.user_data.get('colum', None)

    page = DocsPage.objects.filter(is_active=True).first()
    keys = DocsKeys.objects.filter(is_active=True).first()

    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]
    creads = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
    client = gspread.authorize(creads)
    docsData = client.open("Answers").worksheet(page.page.capitalize())

    if not colum_answer:
        i = 1
        while docsData.cell(i,1).value != None:
            i = i + 1
        context.user_data['colum'] = i

        docsData.update_cell(i, 1, f"tg_id=>{user_id}")
        docsData.update_cell(i, colum, value)
    else:
        docsData.update_cell(colum_answer, colum, value)


