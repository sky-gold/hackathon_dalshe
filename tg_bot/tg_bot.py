import telebot
from telebot import types
import os


BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


def MakeKeyboard(arr: list[tuple[str, str]] | None = None):
    keyboard = types.InlineKeyboardMarkup()
    if arr is None:
        return keyboard
    # buttons = list()
    for button in arr:
        # buttons.append(types.InlineKeyboardButton(text=button[0], callback_data=button[1]))
        keyboard.add(types.InlineKeyboardButton(text=button[0], callback_data=button[1]))
    # keyboard.row(*buttons)
    return keyboard


def AskForExpert(expert):
    def second_step(message):
        keyboard = MakeKeyboard(
            [("Частые вопросы", "FAQ"), ("О нас", "About us"), ("Связаться с фондом", "Con with fond")])
        bot.send_message(message.chat.id, f"Ваш вопрос для {expert} был записан, ожидайте ответа", reply_markup=keyboard)
        # ADD QUESTION TO DB
    return second_step


@bot.message_handler(commands=['start'])
def start_command_handler(message):
    keyboard = MakeKeyboard([("Частые вопросы", "FAQ"), ("О нас", "About us"), ("Связаться с фондом", "Con with fond")])
    bot.send_message(message.chat.id, "Place holder", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "Start":
        keyboard = MakeKeyboard(
            [("Частые вопросы", "FAQ"), ("О нас", "About us"), ("Связаться с фондом", "Con with fond")])
        bot.(chat_id=call.message.chat.id, message_id=call.message.id,
                              text="Place holder", reply_markup=keyboard)
    elif call.data == "FAQ":
        bot.send_message(call.message.chat.id, "Тут будет FAQ")
    elif call.data == "About us":
        bot.send_message(call.message.chat.id, "Что-то про нас")
    elif call.data == "Con with fond":
        keyboard = MakeKeyboard([("Связаться по номеру телефона или почте", "Con using email or phone"),
                                 ("Задать вопрос", "Ask a specialist a question"),
                                 ("Связаться со специалистом", "Con with expert"),
                                 ("Назад", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text="Как хотите связаться?", reply_markup=keyboard)
    elif call.data == "Con using email or phone":
        keyboard = MakeKeyboard(
            [("Частые вопросы", "FAQ"), ("О нас", "About us"), ("Связаться с фондом", "Con with fond")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text="Рабочее время в будни с 10:00 до 21:00\nпочта: info@dalshefond.ru\nтелефон: 8-800-707-44-03", reply_markup=keyboard)
    elif call.data == "Ask a specialist a question":
        # spec = GetSpec()
        keyboard = MakeKeyboard(
            [("Лимфолог", "Expert_ask: lymphologist"), ("Онколог", "Expert_ask: oncologist"), ("В стартовое меню", "Con with fond")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text="Какому специалисту вы хотите задать вопрос?", reply_markup=keyboard)
    elif call.data.startswith("Expert_ask: "):
        # spec = GetSpec()
        expert = call.data.removeprefix("Expert_ask: ")
        keyboard = MakeKeyboard([("Назад", "Ask a specialist a question")])
        if expert == "oncologist":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text="Напишите свой вопрос специалисту: ", reply_markup=keyboard)
            bot.register_next_step_handler(call.message, AskForExpert(expert))
        elif expert == "lymphologist":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text="Напишите свой вопрос специалисту: ", reply_markup=keyboard)
            bot.register_next_step_handler(call.message, AskForExpert(expert))
        else:
            keyboard = MakeKeyboard(
                [("Частые вопросы", "FAQ"), ("О нас", "About us"), ("Связаться с фондом", "Con with fond")])
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text="Place holder", reply_markup=keyboard)
    else:
        bot.send_message(call.message.chat.id, "Я такого не умею")


bot.polling(none_stop=True)
