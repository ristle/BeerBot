# -*- coding: utf-8 -*-
import config
import telebot
import telepot
from loguru import logger


@logger.catch()
def inline_keyboard(bot, message, debug):
    keyboard = telebot.types.InlineKeyboardMarkup()

    beers = config.load_beer_list()
    logger.info("Got command from {}", message.from_user.username)
    logger.info(debug)

    if message.from_user.username not in config.trust_list:
        bot.send_message(message.chat.id, "У Вас нет прав на добавление", parse_mode='Markdown')
        return

    config.ADD_PERSON = True

    for NAME, iter in beers.items():
        keyboard.row(
            telebot.types.InlineKeyboardButton(NAME, callback_data=NAME)
        )
    return bot, keyboard


@logger.catch
def post_keyboard_action(bot, message, keyboard):
    bot.send_chat_action(message.chat.id, 'typing')
    if config.LAST_REPLY_MESSAGE is not None:
        bot.delete_message(message.chat.id, config.LAST_REPLY_MESSAGE)
        config.LAST_REPLY_MESSAGE = None

    send_message_ = 'Выберите '
    msg = bot.send_message(message.chat.id, send_message_, reply_markup=keyboard, parse_mode='Markdown')
    config.LAST_REPLY_MESSAGE = msg.message_id


@logger.catch()
def send_list(bot, message):
    text = str()

    logger.info("Got command from {}", message.from_user.username)
    logger.info("Starting sendin list")
    bot.send_chat_action(message.chat.id, 'typing')

    if config.LAST_REPLY_MESSAGE is not None:
        bot.delete_message(message.chat.id, config.LAST_REPLY_MESSAGE)
        config.LAST_REPLY_MESSAGE = None

    beers = config.load_beer_list()
    for name_, iter in beers.items():
        NAME = "*" + name_
        if iter and iter < 10:
            if name_ in config.girls:
                text += NAME + "* должна уже _" + str(iter) + "_. Бе)\n"
            else:
                text += NAME + "* должен уже _" + str(iter) + "_\n"
        elif iter >= 10:
            if name_ in config.girls:
                text += NAME + "* обнаглела и должна _" + str(iter) + '_. Фи\n'
            else:
                text += NAME + "* мало косячик, хотя должен уже _" + str(iter) + "_. Стоит призадуматься) \n"
        else:
            if name_ in config.girls:
                text += NAME + "* паинька и не должна ничего\n"
            else:
                text += NAME + "* паинька и не должен ничего\n"
    bot.send_message(message.chat.id, text, parse_mode='Markdown')
    config.LAST_REPLY_MESSAGE = None


@logger.catch()
def send_inline_beer(bot, message):
    bot, keyboard = inline_keyboard(bot, message, "Starting adding a new person")
    keyboard.row(
        telebot.types.InlineKeyboardButton('Добавить Человека', callback_data='Other')
    )
    post_keyboard_action(bot, message, keyboard)


@logger.catch()
def delete_inline_person(bot, message):
    bot, keyboard = inline_keyboard(bot, message, " Staring inline keyboard deleting the person")
    post_keyboard_action(bot, message, keyboard)


@logger.catch()
def choose_number_of_beer(bot, query):
    keyboard = telebot.types.InlineKeyboardMarkup()

    if query.from_user.username not in config.trust_list:
        bot.send_message(query.message.chat.id, "У Вас нет прав на добавление", parse_mode='Markdown')
        return

    for item in config.numbers:
        keyboard.row(
            telebot.types.InlineKeyboardButton(str(item), callback_data=item)
        )
    if config.NAME is None:
        bot.send_message(query.message.chat.id, "Ошибка! Человек который накосячил не выбран!", parse_mode='Markdown')
        return

    if config.LAST_REPLY_MESSAGE is not None:
        bot.delete_message(query.message.chat.id, config.LAST_REPLY_MESSAGE)
        config.LAST_REPLY_MESSAGE = None

    bot.send_chat_action(query.message.chat.id, 'typing')
    send_message_ = 'Выберите количество пиво для ' + config.NAME
    msg = bot.send_message(query.message.chat.id, send_message_, reply_markup=keyboard, parse_mode='Markdown')
    config.LAST_REPLY_MESSAGE = msg.message_id


@logger.catch()
def add_beer(bot, query):
    beers = config.load_beer_list()
    if config.NAME is None:
        bot.send_message(query.message.chat.id, "Ошибка! Человек который накосячил не выбран!", parse_mode='Markdown')
        return

    if query.from_user.username not in config.trust_list:
        logger.error("This person trying to access {}", query.from_user.username)
        bot.send_message(query.message.chat.id, "У Вас нет прав на добавление", parse_mode='Markdown')
        return

    beers[config.NAME] += int(query.data)

    if beers[config.NAME] < 0:
        beers[config.NAME] = 0
        bot.send_message(query.message.chat.id, 'Не пытайтесь понизить пиво меньше 0!', parse_mode='Markdown')

    config.save_beer_list(beers)

    if config.LAST_REPLY_MESSAGE is not None:
        bot.delete_message(query.message.chat.id, config.LAST_REPLY_MESSAGE)
        config.LAST_REPLY_MESSAGE = None

    send_message_ = 'Теперь у *' + config.NAME + '* должен __' + str(beers[config.NAME]) + \
                    '__ бутылок пива'
    bot.send_chat_action(query.message.chat.id, 'typing')
    bot.send_message(query.message.chat.id, send_message_, parse_mode='Markdown')
    config.LAST_REPLY_MESSAGE = None


@logger.catch
def add_inline_person(bot, message):
    logger.info("Starting adding")
    if config.LAST_REPLY_MESSAGE is not None:
        bot.delete_message(message.chat.id, config.LAST_REPLY_MESSAGE)
        config.LAST_REPLY_MESSAGE = None

    send_message_ = 'Напишите имя человека '
    msg = bot.send_message(message.chat.id, send_message_, parse_mode='Markdown')
    config.LAST_REPLY_MESSAGE = msg.message_id


@logger.catch()
def add_person(bot, query):
    beers = config.load_beer_list()
    beers[query.text] = 0

    config.save_beer_list(beers)

    logger.info("Added {}", query.text)
    bot.send_chat_action(query.chat.id, 'typing')
    send_message_ = 'Человек {0} *добавлен*. У него пока _0_ пива на счету, если хотите это исправить, то введите ' \
                    'комманду /add '.format(query.text)
    bot.send_message(query.chat.id, send_message_, parse_mode='Markdown')


@logger.catch()
def delete_person(bot, query):
    if config.LAST_REPLY_MESSAGE:
        try:
            bot.delete_message(query.chat.id, config.LAST_REPLY_MESSAGE)
            config.LAST_REPLY_MESSAGE = None
        except Exception as ex:
            logger.error(ex)
    if not config.NAME:
        logger.error("No name was provided")
        # Ошибка работы бота - он не выходит отсюда и не понимает, что пора остановится
        # bot.send_message(query.chat.id, "No *name* was provided! ", parse_mode='Markdown')
        return

    beers = config.load_beer_list()
    del beers[config.NAME]
    config.save_beer_list(beers)

    logger.info("Added {}", query.text)
    bot.send_chat_action(query.chat.id, 'typing')
    send_message_ = 'Человек _{0}_ *удален* '.format(config.NAME)
    bot.send_message(query.chat.id, send_message_, parse_mode='Markdown')

    config.NAME = None
