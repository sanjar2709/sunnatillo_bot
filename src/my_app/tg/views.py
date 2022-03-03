from django.shortcuts import render
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from .models import SendData, SendDataButtons, Users, Questions, QuestionValues, Answers
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
        user = user_save(user_data)

    buttons = [['🏢 Savol javob', '🏢 Biz haqimizda']]
    text = f"""Assalomu aleykum <b>{user.tg_firstname}</b>"""
    go_message(context, user.tg_id, text, None)
    send_commands(user_id=user.tg_id, status=1, context=context)



def text_function(update, context):
    user_status = context.user_data.get('user_status', 1)
    message_id = update.message.message_id
    user = update.message.from_user
    state = context.user_data.get('state', 0)
    text = update.message.text
    print("text", text)
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
            go_message(context=context, user_id=user.id, message='Hozircha savollar yoq ❌')
    elif state == 100:
        questions = context.user_data['questions']
        question_id = context.user_data['question_id']
        print("answer_save javoblarni saqlaydi text function")
        answer_save(user_id=user.id, question_id=question_id, text=text)
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

def calback_function(update, context):
    user_status = context.user_data.get('user_status', 1)
    message_id = update.callback_query.message.message_id
    state = context.user_data['state']
    user = update.callback_query.from_user
    data_sp = update.callback_query.data.split('_')
    print("data_sp", data_sp)
    if state == 100 and data_sp[0] == 'question':
        questions = context.user_data['questions']
        question_id = context.user_data['question_id']
        print("answer_save javoblarni saqlaydi query function")
        answer_save(user_id=user.id, question_id=question_id, value=int(data_sp[1]))
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
            send_commands(user_id=user.id, status=3, context=context, message_id=message_id, state=state)


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
        print("------pass-----")

def user_save(user_data):
    user = Users()
    user.tg_id = user_data.id
    try:
        user.phone_number = user_data.phone_number
    except:
        pass
    try:
        user.tg_firstname = user_data.first_name
    except:
        pass
    try:
        user.tg_lastname = user_data.lastname
    except:
        pass

    user.save()
    return user

def answer_save(user_id, question_id, text=None, value=None):
    user = Users.objects.get(tg_id=user_id)
    answer = Answers()
    if text:
        ques = Answers.objects.filter(question_id=question_id, user=user)
        if ques:
            ques.delete()
        question = Questions.objects.get(pk=question_id)
        answer.question = question.question
        answer.answer = text
        answer.question_id = question_id
    elif value:
        ques = Answers.objects.filter(question_id=question_id, user=user)
        if ques:
            ques.delete()
        question = Questions.objects.get(pk=question_id)
        question_value = QuestionValues.objects.get(pk=question_id)
        answer.question = question.question
        answer.answer = question_value.value
        answer.question_id=question_id
    answer.user = user

    answer.save()