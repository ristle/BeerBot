import config
import telebot
import telepot


def send_list(bot, message):
    text = str()

    bot.send_chat_action(message.chat.id, 'typing')

    if config.LAST_REPLY_MESSAGE is not None:
        bot.delete_message(message.chat.id, config.LAST_REPLY_MESSAGE)

    beers = config.load_beer_list()
    for NAME, iter in beers.items():
        if iter and iter < 10:
            if NAME in config.girls:
                text += NAME + " должна уже " + str(iter) + ". Фииииии\n\n"
            else:
                text += NAME + " должен уже " + str(iter) + "\n\n"
        elif iter > 10:
            if NAME in config.girls:
                text += NAME + " обнаглела и должна " + str(iter) + '. Фиииии\n\n'
            else:
                text += NAME + " мало косячик, хотя должен уже " + str(iter) + ". Стоит призадуматься) \n\n"
        else:
            text += NAME + " паинька и не должен ничего\n\n"
    bot.send_message(message.chat.id, text)
    config.LAST_REPLY_MESSAGE = None


def send_inline_beer(bot, message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    beers = config.load_beer_list()

    for NAME, iter in beers.items():
        keyboard.row(
            telebot.types.InlineKeyboardButton(NAME, callback_data=NAME)
        )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Добавить Человека', callback_data='Other')
    )

    bot.send_chat_action(message.chat.id, 'typing')
    if config.LAST_REPLY_MESSAGE is not None:
        bot.delete_message(message.chat.id, config.LAST_REPLY_MESSAGE)

    send_message_ = 'Выберите'
    msg = bot.send_message(message.chat.id, send_message_, reply_markup=keyboard)
    config.LAST_REPLY_MESSAGE = msg.message_id


def choose_number_of_beer(bot, query):
    keyboard = telebot.types.InlineKeyboardMarkup()
    if query.message.from_user.username not in config.trust_list:
        bot.send_message(query.message.chat.id, "У Вас нет прав на добавление")
        return

    for item in config.numbers:
        keyboard.row(
            telebot.types.InlineKeyboardButton(str(item), callback_data=item)
        )
    if config.NAME is None:
        bot.send_message(query.message.chat.id, "Ошибка! Человек который накосячил не выбран!")
        return

    if config.LAST_REPLY_MESSAGE is not None:
        bot.delete_message(query.message.chat.id, config.LAST_REPLY_MESSAGE)

    bot.send_chat_action(query.message.chat.id, 'typing')
    send_message_ = 'Выберите количество пиво для ' + config.NAME
    msg = bot.send_message(query.message.chat.id, send_message_, reply_markup=keyboard)
    config.LAST_REPLY_MESSAGE = msg.message_id


def add_beer(bot, query):
    beers = config.load_beer_list()
    if config.NAME is None:
        bot.send_message(query.message.chat.id, "Ошибка! Человек который накосячил не выбран!")
        return

    if query.message.from_user.username not in config.trust_list:
        bot.send_message(query.message.chat.id, "У Вас нет прав на добавление")
        return

    beers[config.NAME] += int(query.data)

    if beers[config.NAME] < 0:
        beers[config.NAME] = 0
        bot.send_message(query.message.chat.id, 'Не пытайтесь понизить пиво меньше 0!')

    config.save_beer_list(beers)

    if config.LAST_REPLY_MESSAGE is not None:
        bot.delete_message(query.message.chat.id, config.LAST_REPLY_MESSAGE)

    send_message_ = 'Теперь у ' + config.NAME + ' должен ' + str(beers[config.NAME]) + \
                    ' бутылок пива'
    bot.send_chat_action(query.message.chat.id, 'typing')
    bot.send_message(query.message.chat.id, send_message_)
    config.LAST_REPLY_MESSAGE = None


def add_inline_person(bot, message):
    if config.LAST_REPLY_MESSAGE is not None:
        bot.delete_message(message.chat.id, config.LAST_REPLY_MESSAGE)

    send_message_ = 'Напишите имя человека'
    msg = bot.send_message(message.chat.id, send_message_)
    config.LAST_REPLY_MESSAGE = msg.message_id


def add_person(bot, query):
    beers = config.load_beer_list()
    beers[query.text] = 0
    try:
        del beers['/main']
    except:
        pass
    config.save_beer_list(beers)

    bot.send_chat_action(query.message.chat.id, 'typing')
    send_message_ = 'Человек добавлен. У него пока 0 пива на счету, если хотите это исправить, то введите комманду /add'
    bot.send_message(query.chat.id, send_message_)
