import logging
import actions
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackQueryHandler, MessageHandler, Filters


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                  level=logging.INFO)


with open('key.config', 'r', encoding='utf-8') as myfile:
    key = myfile.read().replace('\n', '')

def error_callback(bot, update, error):
    print(error)

updater = Updater(key)
updater.dispatcher.add_error_handler(error_callback)
updater.dispatcher.add_handler(CallbackQueryHandler(actions.click))
updater.dispatcher.add_handler(CommandHandler('start', actions.menu))
updater.dispatcher.add_handler(CommandHandler('getsettings', actions.editFile))
updater.dispatcher.add_handler(MessageHandler(Filters.document, actions.replaceSettings))
updater.dispatcher.add_handler(InlineQueryHandler(actions.inlineGame))
updater.start_polling()
updater.idle()
