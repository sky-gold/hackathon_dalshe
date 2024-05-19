import telebot
from telebot import types
from telebot.custom_filters import SimpleCustomFilter
from consts import SPECIALISTS
import os

from database import add_user, add_question, answer_question, is_admin, get_all_questions, get_question
from faq import get_most_similar_faq

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


class MyIsAdmin(SimpleCustomFilter):
    key = 'is_admin'
    @staticmethod
    def check(message):
        add_user(message.from_user.id, message.from_user.username,
                 message.from_user.first_name + " " + message.from_user.last_name)
        return is_admin(message.from_user.id)


bot.add_custom_filter(MyIsAdmin())


def make_keyboard(arr: list[tuple[str, str]] | None = None):
    keyboard = types.InlineKeyboardMarkup()
    if arr is None:
        return keyboard
    for button in arr:
        keyboard.add(types.InlineKeyboardButton(text=button[0], callback_data=button[1]))
    return keyboard


def ask_question(specialist):
    def second_step(message):
        question_num = str(add_question(specialist, message.from_user.id, message.text))
        faq1, faq2 = get_most_similar_faq(message.text)
        keyboard = make_keyboard(
            [("Да", f"find_ans{question_num}"), ("Нет", "ans_not_find")])
        bot.send_message(message.chat.id, f"Часто задаваемые вопросы, похожие на ваш, есть ли среди них ответ на"
                                          f"него?\n"
                                          f"{faq1[0]} -> {faq1[1]}\n"
                                          f"{faq2[0]} -> {faq2[1]}", reply_markup=keyboard)
    return second_step


@bot.message_handler(is_admin=False, commands=['start'])
def start_command_handler(message):
    add_user(message.from_user.id, message.from_user.username,
             message.from_user.first_name + " " + message.from_user.last_name)
    keyboard = make_keyboard([("Хочу больше узнать о раке груди", "More about breast cancer"),
                              ("Получить помощь фонда", "Get help from the foundation"),
                              ("Связаться с нами", "Contact us"),
                              ("Психологическая помощь", "Psychological help"),
                              ("Хочу помочь фонду", "Desire to help the foundation"),
                              ("Отзывы", "Reviews"),
                              ("Истории пациентов", "Patient stories"),
                              ("О фонде", "About us")])
    bot.send_message(message.chat.id, "Добро пожаловать, что бы вы хотели?", reply_markup=keyboard)


@bot.callback_query_handler(is_admin=False, func=lambda call: True)
def callback_query(call):
    if call.data == "Start":
        keyboard = make_keyboard([("Хочу больше узнать о раке груди", "More about breast cancer"),
                                  ("Получить помощь фонда", "Get help from the foundation"),
                                  ("Связаться с нами", "Contact us"),
                                  ("Психологическая помощь", "Psychological help"),
                                  ("Хочу помочь фонду", "Desire to help the foundation"),
                                  ("Отзывы", "Reviews"),
                                  ("Истории пациентов", "Patient stories"),
                                  ("О фонде", "About us")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Добро пожаловать, что бы вы хотели?",
                              reply_markup=keyboard)
    elif call.data == "About us":
        keyboard = make_keyboard([("Назад", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   text="С апреля 2011 года Благотворительный фонд \"ДАЛЬШЕ\" делает все возможное,"
                                        "чтобы российские женщины имели доступ к качественной ранней диагностике рака"
                                        "груди, а те, кто столкнулся с заболеванием - своевременно получили лечение и"
                                        "как можно быстрее возвращались к полноценной жизни."
                                        "\n\n"
                                        "С 2014 года фонд представляет Россию в Европейской коалиции по борьбе с раком"
                                        "молочной железы Europa Donna (крупнейшая европейская общественная организация,"
                                        "лоббирующая интересы пациентов с диагнозом рак груди)"
                                        "\n"
                                        "[О нас](https://dalshefond.ru/#about)", reply_markup=keyboard, parse_mode="Markdown")
    elif call.data == "Patient stories":
        keyboard = make_keyboard([("Назад", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Тут вы можете почитать истории пациентов:  [Истории](https://vmesteplus.ru/first-hand/stories/)",
                              reply_markup=keyboard, parse_mode="Markdown")
    elif call.data == "Reviews":
        keyboard = make_keyboard([("Назад", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Тут вы можете посмотреть отзывы пациентов о фонде:  [Отзывы](https://vmesteplus.ru/first-hand/reviews/)",
                              reply_markup=keyboard, parse_mode="Markdown")
    elif call.data == "Desire to help the foundation":
        keyboard = make_keyboard([("Назад", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Тут вы можете помочь нашему фонду:  [Пожертвовать](https://dalshefond.ru/donate/)",
                              reply_markup=keyboard, parse_mode="Markdown")
    elif call.data == "Psychological help":
        keyboard = make_keyboard([("Назад", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="О психологической помощи: "
                                   "[О помощи](https://vmesteplus.ru/support/how/psychological-support/)"
                                   "\n"
                                   "Расписание мероприятий: [Расписание](https://vmesteplus.ru/events/)",
                              reply_markup=keyboard, parse_mode="Markdown")
    elif call.data == "More about breast cancer":
        keyboard = make_keyboard([("Как сохранить здоровье груди", "Keep the breasts healthy"),
                                  ("Как узнать свой риск", "Recognizing your risk"),
                                  ("Как лечится рак груди", "How breast cancer is treated"),
                                  ("Навигатор для пациента", "Patient navigator"),
                                  ("Получить фонд помощи", "Get help from the foundation"),
                                  ("Назад", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Что вы хотите узнать?", reply_markup=keyboard)
    elif call.data == "Keep the breasts healthy":
        keyboard = make_keyboard([("Назад", "More about breast cancer"), ("Вернуться в начало", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Тут вы можете получить пособие по профилактике [Пособие](https://dalshefond.ru/prevention-manual/)",
                              reply_markup=keyboard)
    elif call.data == "Recognizing your risk":
        keyboard = make_keyboard([("Назад", "More about breast cancer"), ("Вернуться в начало", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="В этом калькуляторе вы можете узнать свой риск: "
                                   "[Калькулятор риска](https://www.dalshefond.ru/check/)",
                              reply_markup=keyboard, parse_mode="Markdown")
    elif call.data == "Patient navigator":
        keyboard = make_keyboard([("Назад", "More about breast cancer"), ("Вернуться в начало", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Тут вы можете узнать, как лечиться по ОМС: "
                                   "[Путеводитель](https://vmesteplus.ru/first-hand/articles/rak-grudi-putevoditel/)",
                              reply_markup=keyboard, parse_mode="Markdown")
    elif call.data == "How breast cancer is treated":
        keyboard = make_keyboard([("Назад", "More about breast cancer")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Есть онлайн курс, где можно узнать как лечится рак груди: "
                                   "[Курс](https://vmesteplus.ru/distance-programs/oncologist-course/)",
                              reply_markup=keyboard, parse_mode="Markdown")
    elif call.data == "Get help from the foundation":
        keyboard = make_keyboard([("Пособие пациента", "Patient manual"),
                                  ("Индивидуальную помощь", "Individual assistance"),
                                  ("Бесплатное такси к месту лечения", "Targeted assistance"),
                                  ("Назад", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Какую помощь вы хотите получить?", reply_markup=keyboard)
    elif call.data == "Patient manual":
        with open("patient_manual.pdf", "rb") as file:
            bot.send_document(call.message.chat.id, file)
        keyboard = make_keyboard([("Назад", "Get help from the foundation"), ("Вернуться в начало", "Start")])
        bot.send_message(chat_id=call.message.chat.id, text="Это пособие содержит информацию для пациентов",
                         reply_markup=keyboard)
    elif call.data == "Individual assistance":
        keyboard = make_keyboard([("Назад", "Get help from the foundation"), ("Вернуться в начало", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Тут вы можете получить индивидуальную помощь: "
                                   "[Индивидуальная помощь](https://vmesteplus.ru/personal/personalized-help/)",
                              reply_markup=keyboard, parse_mode="Markdown")
    elif call.data == "Targeted assistance":
        keyboard = make_keyboard([("Назад", "Get help from the foundation"), ("Вернуться в начало", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Тут вы можете узнать про бесплатное такси до места лечения: "
                                   "[Адресная помощь](https://vmesteplus.ru/support/how/targeted-assistance/)",
                              reply_markup=keyboard, parse_mode="Markdown")
    elif call.data == "Contact us":
        keyboard = make_keyboard([("По телефону или почте", "Phone and email"), ("Задать вопрос", "Ask a question"),
                                  ("Назад", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Как вы хотите связаться с нами?",
                              reply_markup=keyboard)
    elif call.data == "Phone and email":
        keyboard = make_keyboard([("Назад", "Contact us"), ("Вернуться в начало", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Рабочее время: пн-пт с 11:00 до 20:00\n"
                                   "почта: info@dalshefond.ru\n"
                                   "телефон: 8-800-707-44-03",
                              reply_markup=keyboard)
    elif call.data == "Ask a question":
        specs = []
        for specialist in SPECIALISTS:
            specs.append((specialist, specialist))
        specs.append(("Назад", "Contact us"))
        specs.append(("Вернуться в начало", "Start"))
        keyboard = make_keyboard(specs)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Какому специалисту вы хотите задать вопрос?",
                              reply_markup=keyboard)
    elif call.data in SPECIALISTS:
        keyboard = make_keyboard([("Назад", "Ask a question"), ("Вернуться в начало", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Напишите свой вопрос для специалиста или вернитесь назад или в начало",
                              reply_markup=keyboard)
        bot.register_next_step_handler(call.message, ask_question(call.data))
    elif call.data.startswith("find_ans"):
        question_num = int(call.data.removeprefix("find_ans"))
        answer_question(question_num, "FAQ")
        keyboard = make_keyboard([("Хочу больше узнать о раке груди", "More about breast cancer"),
                                  ("Получить помощь фонда", "Get help from the foundation"),
                                  ("Связаться с нами", "Contact us"),
                                  ("Психологическая помощь", "Psychological help"),
                                  ("Хочу помочь фонду", "Desire to help the foundation"),
                                  ("Отзывы", "Reviews"),
                                  ("Истории пациентов", "Patient stories"),
                                  ("О фонде", "About us")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Мы рады, что смогли помочь", reply_markup=keyboard)
    elif call.data == "ans_not_find":
        keyboard = make_keyboard([("Хочу больше узнать о раке груди", "More about breast cancer"),
                                  ("Получить помощь фонда", "Get help from the foundation"),
                                  ("Связаться с нами", "Contact us"),
                                  ("Психологическая помощь", "Psychological help"),
                                  ("Хочу помочь фонду", "Desire to help the foundation"),
                                  ("Отзывы", "Reviews"),
                                  ("Истории пациентов", "Patient stories"),
                                  ("О фонде", "About us")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Ваш вопрос был передан специалисту", reply_markup=keyboard)
    else:
        keyboard = make_keyboard([("Хочу больше узнать о раке груди", "More about breast cancer"),
                                  ("Получить помощь фонда", "Get help from the foundation"),
                                  ("Связаться с нами", "Contact us"),
                                  ("Психологическая помощь", "Psychological help"),
                                  ("Хочу помочь фонду", "Desire to help the foundation"),
                                  ("Отзывы", "Reviews"),
                                  ("Истории пациентов", "Patient stories"),
                                  ("О фонде", "About us")])
        bot.send_message(call.message.chat.id, "Извините, но эта команда мне не известна :(", reply_markup=keyboard)


def waiting_question_text_from_admin(question_id):
    def second_step(message):
        question = get_question(question_id)
        try:
            bot.send_message(chat_id=question["user_id"], text=f"На ваш вопрос:\n{question['question_text']}\n"
                                                               f"Для специалиста:\n{question['specialist_type']}\n"
                                                               f"Пришёл ответ:\n{message.text}")
            answer_question(question["id"], message.text)
            keyboard = make_keyboard([("Получить все незакрытые вопросы", "Get all questions"),
                                      ("Ответить на вопрос", "Answer for question")])
            bot.send_message(chat_id=message.chat.id, text="Ответ отправлен пользователю", reply_markup=keyboard)
        except Exception as e:
            keyboard = make_keyboard([("Получить все незакрытые вопросы", "Get all questions"),
                                      ("Ответить на вопрос", "Answer for question")])
            bot.send_message(chat_id=message.chat.id, text="Ошибка во время отправки сообщения, попробуйте позже",
                             reply_markup=keyboard)

    return second_step


def waiting_question_id_from_admin(message):
    question = get_question(int(message.text.strip()))
    if not question:
        keyboard = make_keyboard([("Получить все незакрытые вопросы", "Get all questions"),
                                  ("Ответить на вопрос", "Answer for question")])
        bot.send_message(chat_id=message.chat.id, text="Вопроса с таким id не существует", reply_markup=keyboard)
        return
    if question["status"] == "DONE":
        keyboard = make_keyboard([("Получить все незакрытые вопросы", "Get all questions"),
                                  ("Ответить на вопрос", "Answer for question")])
        bot.send_message(chat_id=message.chat.id, text="На этот вопрос уже ответили", reply_markup=keyboard)
        return
    bot.send_message(chat_id=message.chat.id, text="Введите ответ на этот вопрос")
    bot.register_next_step_handler(message=message,
                                   callback=waiting_question_text_from_admin(int(message.text.strip())))

@bot.message_handler(is_admin=True, commands=['start'])
def start_command_handler(message):
    add_user(message.from_user.id, message.from_user.username,
             message.from_user.first_name + " " + message.from_user.last_name)
    keyboard = make_keyboard([("Получить все незакрытые вопросы", "Get all questions"),
                              ("Ответить на вопрос", "Answer for question")])
    bot.send_message(message.chat.id, "Добро пожаловать в администраторскую", reply_markup=keyboard)


@bot.callback_query_handler(is_admin=True, func=lambda call: True)
def callback_query(call):
    if call.data == "Start":
        keyboard = make_keyboard([("Получить все незакрытые вопросы", "Get all questions"),
                                  ("Ответить на вопрос", "Answer for question")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Добро пожаловать в администраторскую",
                              reply_markup=keyboard)
    elif call.data == "Get all questions":
        id_list = get_all_questions()
        keyboard = make_keyboard([("Получить все незакрытые вопросы", "Get all questions"),
                                  ("Ответить на вопрос", "Answer for question")])
        if not id_list:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Вопросов пока что нет",
                                  reply_markup=keyboard)
        else:
            live_message_fl = False
            for question_id in id_list:
                question = get_question(question_id)
                if not question:
                    continue
                if question["status"] == "DONE":
                    continue
                live_message_fl = True
                bot.send_message(chat_id=call.message.chat.id, text=f"Вопрос с id: {question['id']} "
                                                                    f"для специалиста: {question['specialist_type']}: "
                                                                    f"{question['question_text']}")
            if live_message_fl:
                bot.send_message(chat_id=call.message.chat.id, text="Что будем делать дальше?", reply_markup=keyboard)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Вопросов пока что нет",
                                      reply_markup=keyboard)

    elif call.data == "Answer for question":
        keyboard = make_keyboard([("В начало", "Start")])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Введите id вопроса или вернитесь в начало", reply_markup=keyboard)
        bot.register_next_step_handler(call.message, waiting_question_id_from_admin)
    else:
        keyboard = make_keyboard([("Получить все незакрытые вопросы", "Get all questions"),
                                  ("Ответить на вопрос", "Answer for question")])
        bot.send_message(call.message.chat.id, "Неизвестная команда :(", reply_markup=keyboard)




bot.polling(none_stop=True)
