import telebot
from telebot import types
import os


BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


def MakeKeyboard(arr: list[tuple[str, str]] | None = None):
    keyboard = types.InlineKeyboardMarkup()
    if arr is None:
        return keyboard
    buttons = list()
    for button in arr:
        buttons.append(types.InlineKeyboardButton(text=button[0], callback_data=button[1]))
    keyboard.row(*buttons)
    return keyboard


@bot.message_handler(commands=['start'])
def start_command_handler(message):
    start_keyboard = MakeKeyboard([("Частые вопросы", "FAQ"), ("О нас", "About us"), ("Связаться со специалистом", "Con with expert")])
    bot.send_message(message.chat.id, "Hi", reply_markup=start_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "FAQ":
        bot.send_message(call.message.chat.id, "Тут будет FAQ")
    elif call.data == "About us":
        bot.send_message(call.message.chat.id, "Что-то про нас")
    elif call.data == "Con with expert":
        bot.send_message(call.message.chat.id, "Связь")
    else:
        bot.send_message(call.message.chat.id, "Я такого не умею")


bot.polling(none_stop=True)
