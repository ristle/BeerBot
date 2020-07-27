# -*- coding: utf-8 -*-
import telebot
import telepot
import config
import func

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['beer_s'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Шалом, я предназначен для того, чтобы смотреть кто сколько пива должен\n' +
        'Если есть вопросы, то напишите /help.'
    )


# for stupid
@bot.message_handler(commands=['beer_h'])
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
        '1) Для того, чтобы начать напишите: /beer_m ' +
        'и нажмите на желаемое действие\n' +
        '2) Если вы выбрали "Добавить", то далее нажмите на нужного человека\n' +
        '3) Нажмите на количество пива\n' +
        '4) Для того, чтобы сразу добавить пиво на счет можете также написать /beer_a\n' +
        '5) Можно добавить нового человека через /beer_a (последняя кнопка\n' +
        '6) Для просмотра списка должников можно сразу написать /beer_l\n' +
        '7) Ссылка на исходники : https://github.com/ristle/BeerBot.git',
        reply_markup=keyboard
    )


# /main function for lazy people
@bot.message_handler(commands=['beer_m'])
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
@bot.message_handler(commands=['beer_a'])
def exchange_command(message):
    config.NAME = None
    if message.from_user.username not in config.trust_list:
        bot.send_message(message.chat.id, "У Вас нет прав на добавление")
        return
    func.send_inline_beer(bot, message)


# needed for sending list by typing one command
@bot.message_handler(commands=['beer_l'])
def exchange_command(message):
    config.NAME = None
    func.send_list(bot, message)


# main function for handle all keyboard
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    beers = config.load_beer_list()

    if query.data == 'Список':
        config.NAME = None
        func.send_list(bot, query.message)
    elif query.data == 'Добавить':
        config.NAME = None
        if query.message.from_user.username not in config.trust_list:
            bot.send_message(query.message.chat.id, "У Вас нет прав на добавление")
            return
        func.send_inline_beer(bot, query.message)
    elif query.data in list(beers.keys()):
        config.NAME = query.data
        func.choose_number_of_beer(bot, query)
    elif query.data in [str(i) for i in config.numbers]:
        func.add_beer(bot, query)
    elif query.data == 'Other':
        config.ADD_PERSON = True
        func.add_inline_person(bot, query.message)


# add listener for simple telegram messages
# needed for adding person
def listener(messages):
    for m in messages:
        if config.LAST_REPLY_MESSAGE:
            config.ADD_PERSON = False
            func.add_person(bot, m)


bot.set_update_listener(listener)
bot.polling(none_stop=True)
