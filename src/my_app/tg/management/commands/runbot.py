from django.core.management.base import BaseCommand, CommandError
from telegram.ext import (messagequeue as mq, Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler)
from telegram.utils.request import Request
from ...mqbot import MQBot
from django.conf import settings

from ...views import start, text_function, calback_function

class Command(BaseCommand):
    help = 'Companiya bot'
    def handle(self, *args, **options):
        q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
        request = Request(con_pool_size=36)

        bot = MQBot(settings.TOKEN_KEY, request=request, mqueue=q)
        updater = Updater(bot=bot, use_context=True, workers=32)

        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text,text_function))
        dispatcher.add_handler(CallbackQueryHandler(calback_function))

        updater.start_polling()
        updater.idle()