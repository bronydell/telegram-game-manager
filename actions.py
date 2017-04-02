import json
import base64
from uuid import uuid4
from telegram import InlineQueryResultGame, InlineKeyboardButton, \
    InlineKeyboardMarkup
from shutil import move
import telegram


def getBotSettings():
    with open('bot.json', encoding='UTF-8') as data_file:
        data = json.load(data_file)
    return data


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


def replaceSettings(bot, update, filename='bot'):
    settings = getBotSettings()
    if update.message.document:
        move(filename + '.json', filename + '_old' + '.json')
        file_id = update.message.document.file_id
        bot.getFile(file_id).download(filename + '.json')
        with open(filename + '.json', 'r') as content_file:
            if not is_json(content_file.read()):
                move(filename + '_old' + '.json', filename + '.json')
                bot.sendMessage(update.message.chat_id, text=settings['message']['json_bot_not_valid'])
            else:
                bot.sendMessage(update.message.chat_id, text=settings['message']['json_bot_valid'])


def menu(bot, update, id=-1):
    settings = getBotSettings()
    uid = update.message.from_user.id
    if not id == -1:
        uid = id
    bot.sendMessage(uid, text=settings['message']['Play with friends!'])


def isAdmin(id):
    return id in getBotSettings()['admins']


def inlineGame(bot, update):
    games = getBotSettings()['games']
    query = update.inline_query.query
    inline_games = list()
    for game in games:
        if game['name'].startswith(query):
            inline_games.append(
                InlineQueryResultGame(type='game', id=str(uuid4()),
                                      game_short_name=game['game_short_name']))
    update.inline_query.answer(inline_games)


def editFile(bot, update):
    settings = getBotSettings()
    if isAdmin(update.message.from_user.id):
        uid = update.message.from_user.id
        bot.sendDocument(update.message.chat_id, document=open('bot.json', 'rb'))
    else:
        bot.sendMessage(update.message.chat_id, text=settings['messages']['not_admin'])


def click(bot, update):
    uid = update.callback_query.from_user.id
    games = getBotSettings()['games']
    for game in games:
        if game['game_short_name'] == update.callback_query.game_short_name:
            parametrs = {'u': update.callback_query.from_user.id, 'i': update.callback_query.inline_message_id}
            bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                                    url=game['url'] + '/#player_info={}'.format(
                                        base64.b64encode(json.dumps(parametrs).encode('utf-8')).decode("utf-8")))
