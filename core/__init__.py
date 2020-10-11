# -*- coding: utf-8 -*-
import telebot
import telepot
import config
import func
from loguru import logger

bot = telebot.TeleBot(config.TOKEN)
logger.add(".logger.log", format="{time} {level} {message}", rotation="50 MB")


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Шалом, я предназначен для того, чтобы смотреть кто сколько пива должен\n' +
        'Если есть вопросы, то напишите /help.'
    )


# for stupid
@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'message to developer', url='t.me/ristleell'
        )
    )
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'GitHub', url='https://github.com/ristle/BeerBot.git'
        )
    )
    bot.send_message(
        message.chat.id,
        '1) Для того, чтобы начать напишите: /main ' +
        'и нажмите на желаемое действие\n' +
        '2) Если вы выбрали "Добавить", то далее нажмите на нужного человека\n' +
        '3) Нажмите на количество пива\n' +
        '4) Для того, чтобы сразу добавить пиво на счет можете также написать /add\n' +
        '5) Можно добавить нового человека через /add (последняя кнопка\n' +
        '6) Для просмотра списка должников можно сразу написать /list\n' +
        '7) Ссылка на исходники : https://github.com/ristle/BeerBot.git',
        reply_markup=keyboard
    )


# /main function for lazy people
@bot.message_handler(commands=['main'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Список', callback_data='Список')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Добавить', callback_data='Добавить')
    )

    if config.LAST_REPLY_MESSAGE is not None:
        bot.delete_message(message.chat.id, config.LAST_REPLY_MESSAGE)

    send_message_ = 'Выберите'
    msg = bot.send_message(message.chat.id, send_message_, reply_markup=keyboard)

    config.LAST_REPLY_MESSAGE = msg.message_id


# needed for one line adding new beer
@bot.message_handler(commands=['add'])
def exchange_command(message):
    config.NAME = None
    if message.from_user.username not in config.trust_list:
        bot.send_message(message.chat.id, "У Вас нет прав на добавление")
        return
    func.send_inline_beer(bot, message)


# needed for sending list by typing one command
@bot.message_handler(commands=['list'])
def exchange_command(message):
    print(message.text)
    config.NAME = None
    func.send_list(bot, message)


# main function for handle all keyboard
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    beers = config.load_beer_list()

    if query.data == 'Список':
        config.NAME = None
        config.ADD_PERSON = False
        config.REMOVE_PERSON = False
        func.send_list(bot, query.message)
    elif query.data == 'Добавить':
        config.NAME = None
        config.REMOVE_PERSON = False
        if query.message.from_user.username not in config.trust_list:
            bot.send_message(query.message.chat.id, "У Вас нет прав на добавление")
            return
        func.send_inline_beer(bot, query.message)
    elif query.data in list(beers.keys()):
        config.NAME = query.data
        if config.REMOVE_PERSON:
            config.ADD_PERSON = False
            func.delete_person(bot, query.message)
        else:
            config.REMOVE_PERSON = False
            func.choose_number_of_beer(bot, query)
    elif query.data in [str(i) for i in config.numbers]:
        func.add_beer(bot, query)
    elif query.data == 'Other':
        if config.REMOVE_PERSON:
            config.ADD_PERSON = False
            func.delete_inline_person(bot, query.message)
        else:
            config.REMOVE_PERSON = False
            func.add_inline_person(bot, query.message)
        # bot.send_message(query.message.chat.id, "**Error**",  parse_mode='Markdown')


# needed for stopping useless bot while adding a new person
@bot.message_handler(commands=['stop'])
def exchange_command(message):
    config.ADD_PERSON = False
    config.REMOVE_PERSON = False

    logger.debug("{}", message.text)
    bot.send_message(message.chat.id, "Остановлено добавление бота")


@bot.message_handler(commands=['delete'])
def exchange_command(message):
    logger.debug("{}", message.text)

    if message.from_user.username not in config.trust_list:
        bot.send_message(message.chat.id, "У Вас нет прав на добавление")
        return

    config.REMOVE_PERSON = True
    config.NAME = None

    func.delete_inline_person(bot, message)


# add listener for simple telegram messages
# needed for adding person
def listener(messages):
    logger.debug("{}", messages)
    for m in messages:
        if config.LAST_REPLY_MESSAGE:
            if config.ADD_PERSON:
                config.ADD_PERSON = False
                func.add_person(bot, m)
            elif config.REMOVE_PERSON:
                config.REMOVE_PERSON = False
                func.delete_person(bot, m)


bot.set_update_listener(listener)
bot.polling(none_stop=True)
