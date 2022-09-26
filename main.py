import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
import random
from config import TOKEN

# Подключаем токен бота
bot = telebot.TeleBot(TOKEN)

# Подключаем БД
conn = sqlite3.connect('db/database.db', check_same_thread=False)
cursor = conn.cursor()

img = r'pycasino.PNG'


# Определяем таблицу
def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, balance: int, bet: int, gamesplayed: int, gameswin: int, gameslose: int):
    cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username, balance, bet, gamesplayed, gameswin, gameslose) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (user_id, user_name, user_surname, username, balance, bet, gamesplayed, gameswin, gameslose))
    conn.commit()


@bot.message_handler(commands=['start'])
def start_message(message):

    # Делаем записи в БД
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    default_balance = 1000
    default_bet = 0
    games_num = 0
    win_num = 0
    lose_num = 0

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Кнопки
    btn1 = types.KeyboardButton("👤 Аккаунт")
    btn2 = types.KeyboardButton("🎲 Рулетка")
    btn3 = types.KeyboardButton("⚙ Разработчик")

    markup.add(btn1, btn2, btn3)

    # Проверяем наличие пользователя в БД
    user = cursor.execute('SELECT * FROM users WHERE user_id=?', (us_id,))

    # Если пользователя нет:
    if user.fetchone() is None:
        db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username,
                     balance=default_balance, bet=default_bet, gamesplayed=games_num, gameswin=win_num, gameslose=lose_num)
        bot.send_photo(message.chat.id, photo=open(img, 'rb'), caption=f"🤚🏻 Привет, <b>{message.from_user.first_name}</b>!\n"
                                          f"Добро пожаловать на <b>pyCasino</b>. \n\n"
                                          f"🎲 Здесь ты можешь поиграть в классическую рулетку и "
                                          f"приумножить свой капитал, выиграв <b>настоящие</b> деньги! \n\n"
                                          f"🎁 Для <b>новых</b> пользователей "
                                          f"у нас есть подарок - <b>1000</b> стартовых игровых монет. Удачной игры :) \n\n"
                                          f"📍 Твой уникальный id: <code>{us_id}</code> \n"
                                          f"💰 Твой баланс: <code>{default_balance}</code> монет \n", parse_mode="HTML",
                                          reply_markup=markup)

    # Если пользователь есть:
    else:
        us_balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (us_id,)).fetchone()[0]
        bot.send_photo(message.chat.id, photo=open(img, 'rb'), caption=f"Добро пожаловать, <b>{message.from_user.first_name} 🤚🏻</b>\n\n"
                                          f"Рады снова видеть тебя на <b>pyCasino</b>.\n"
                                          f"Мы сохранили твой баланс, \nможешь приступить к игре!\n\n"
                                          f"📍 Твой уникальный id: <code>{us_id}</code> \n"
                                          f"💰 Твой баланс: <code>{us_balance}</code> монет \n", parse_mode="HTML",
                                          reply_markup=markup)


@bot.message_handler(content_types=['text'])
def menu(message):

    user_id = message.from_user.id
    us_id = cursor.execute('SELECT user_id FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    us_balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    games_num = cursor.execute('SELECT gamesplayed FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    games_win = cursor.execute('SELECT gameswin FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    games_lose = cursor.execute('SELECT gameslose FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

    if(message.text == "👤 Аккаунт"):

        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text="💸 Вывод", callback_data="withdrawal")
        button2 = InlineKeyboardButton(text="💳 Пополнить", callback_data="addfunds")
        markup.add(button1, button2)

        bot.send_photo(message.chat.id, photo=open(img, 'rb'), caption=f"👤 <b>Аккаунт</b> - {message.from_user.first_name}\n\n"
                                          f"📍 Твой уникальный id: <code>{us_id}</code> \n"
                                          f"💰 Твой баланс: <code>{us_balance}</code> монет \n\n"
                                          f"📊 <b>Статистика</b>\n\n"
                                          f"🎲 Всего игр: {games_num}\n"
                                          f"🏆 Побед: {games_win}\n"
                                          f"☠ Поражений: {games_lose}", parse_mode="HTML",
                                          reply_markup=markup)

    elif(message.text == "⚙ Разработчик"):

        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text="GitHub", url="https://github.com/quake808")
        button2 = InlineKeyboardButton(text="LinkedIn", url="https://bit.ly/3dsSHRj")
        markup.add(button1, button2)

        bot.send_message(message.chat.id, text="⚙ <b>Разработчик</b> \n\n"
                                               "Привет, по кнопкам ниже можешь найти\n"
                                               "мои другие проекты на Python!", parse_mode="HTML", reply_markup=markup)

    elif(message.text == "🎲 Рулетка"):
        default_bet = 0
        cursor.execute(f'UPDATE users SET bet = "{default_bet}" WHERE user_id = "{user_id}"')
        conn.commit()
        msg = bot.send_message(message.chat.id, text=f"🎲 <b>Рулетка</b> \n\n"
                                               f"Введите сумму ставки.\n"
                                               f"Доступно для игры: <code>{us_balance}</code> монет", parse_mode="HTML")
        bot.register_next_step_handler(msg, userbet)


def userbet(message):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Назад", callback_data="change_bet")
    markup.add(button)

    try:
        default_bet = 0
        user_id = message.from_user.id
        us_balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        us_bet = message.text

        if int(us_bet) <= int(us_balance) and int(us_bet) > 0:
            cursor.execute(f'UPDATE users SET bet = "{us_bet}" WHERE user_id = "{user_id}"')
            conn.commit()
            upd_balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

            msg = bot.send_message(message.chat.id, f'📢 <b>Внимание</b>\n\n'
                                              f'Сумма ставки: <code>{us_bet}</code> монет. \n\n'
                                              f'Если вы подтверждаете ставку,\n'
                                              f'напишите "<b>Подтверждаю</b>".'
                                              , parse_mode='html')
            bot.register_next_step_handler(msg, playcasino)

        else:
            bot.send_message(message.chat.id, '🚫 <b>Ошибка</b>\n\n'
                                              'Сумма ставки не должна превышать ваш баланс, а так же\n'
                                              'быть меньше или равной нулю!\n'
                                              'Попробуйте снова. '
                                              , parse_mode='html', reply_markup=markup)
            cursor.execute(f'UPDATE users SET bet = "{default_bet}" WHERE user_id = "{user_id}"')
            conn.commit()

    except Exception as e:
        default_bet = 0
        user_id = message.from_user.id
        bot.send_message(message.chat.id, '🚫 <b>Ошибка</b>\n\n'
                                          'Ставка должна быть числом!\n'
                                          'Попробуйте снова. '
                                          , parse_mode='html', reply_markup=markup)
        cursor.execute(f'UPDATE users SET bet = "{default_bet}" WHERE user_id = "{user_id}"')
        conn.commit()


def playcasino(message):
    user_id = message.from_user.id
    userbet = cursor.execute('SELECT bet FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

    confirmation = message.text

    if str(confirmation) == "Подтверждаю":
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text="⚫ Черный", callback_data="black")
        button2 = InlineKeyboardButton(text="🔴 Красный", callback_data="red")
        button3 = InlineKeyboardButton(text="🟢 Зеленый", callback_data="green")
        button4 = InlineKeyboardButton(text="Изменить ставку", callback_data="change_bet")
        markup.add(button1, button2, button3, button4)

        upd_balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        bot.send_message(message.chat.id, f'🎲 <b>Выберите цвет</b>\n\n'
                                          f'Баланс: <code>{upd_balance}</code> монет.\n'
                                          f'Сумма ставки: <code>{userbet}</code> монет. '
                                          , parse_mode='html', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, '🚫 <b>Ставка отклонена</b>!', parse_mode='html')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    colors = ["black", "red", "black", "red", "black", "red", "green"]

    userbet = cursor.execute('SELECT bet FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

    randomcolor = str(random.choice(colors))
    print(f"random: {randomcolor}")

    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="⚫ Черный", callback_data="black")
    button2 = InlineKeyboardButton(text="🔴 Красный", callback_data="red")
    button3 = InlineKeyboardButton(text="🟢 Зеленый", callback_data="green")
    button4 = InlineKeyboardButton(text="Изменить ставку", callback_data="change_bet")
    markup.add(button1, button2, button3, button4)

    if call.data == "black" and call.data == randomcolor:
        print(f"user bet:{call.data}")
        bot.answer_callback_query(call.id, "Победа!")

        cursor.execute(f'UPDATE users SET balance = (balance + bet * 2) WHERE user_id = "{user_id}"')
        conn.commit()
        cursor.execute(f'UPDATE users SET gamesplayed = (gamesplayed + 1) WHERE user_id = "{user_id}"')
        conn.commit()
        cursor.execute(f'UPDATE users SET gameswin = (gameswin + 1) WHERE user_id = "{user_id}"')
        conn.commit()

        upd_balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        bot.send_message(call.message.chat.id, f'🎲 <b>Победа!</b>\n\n'
                                          f'Баланс: <code>{upd_balance}</code> монет.\n'
                                          f'Сумма ставки: <code>{userbet}</code> монет.\n\n'
                                          f'Играем дальше? Выбери цвет.'
                                          , parse_mode='html', reply_markup=markup)
    elif call.data == "red" and call.data == randomcolor:
        print(f"user bet:{call.data}")
        bot.answer_callback_query(call.id, "Победа!")

        cursor.execute(f'UPDATE users SET balance = (balance + bet * 2) WHERE user_id = "{user_id}"')
        conn.commit()
        cursor.execute(f'UPDATE users SET gamesplayed = (gamesplayed + 1) WHERE user_id = "{user_id}"')
        conn.commit()
        cursor.execute(f'UPDATE users SET gameswin = (gameswin + 1) WHERE user_id = "{user_id}"')
        conn.commit()

        upd_balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        bot.send_message(call.message.chat.id, f'🎲 <b>Победа!</b>\n\n'
                                          f'Баланс: <code>{upd_balance}</code> монет.\n'
                                          f'Сумма ставки: <code>{userbet}</code> монет.\n\n'
                                          f'Играем дальше? Выбери цвет.'
                                          , parse_mode='html', reply_markup=markup)
    elif call.data == "green" and call.data == randomcolor:
        print(f"user bet:{call.data}")
        bot.answer_callback_query(call.id, "Победа!")

        cursor.execute(f'UPDATE users SET balance = (balance + bet * 3) WHERE user_id = "{user_id}"')
        conn.commit()
        cursor.execute(f'UPDATE users SET gamesplayed = (gamesplayed + 1) WHERE user_id = "{user_id}"')
        conn.commit()
        cursor.execute(f'UPDATE users SET gameswin = (gameswin + 1) WHERE user_id = "{user_id}"')
        conn.commit()

        upd_balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        bot.send_message(call.message.chat.id, f'🎲 <b>Победа!</b>\n\n'
                                          f'Баланс: <code>{upd_balance}</code> монет.\n'
                                          f'Сумма ставки: <code>{userbet}</code> монет.\n\n'
                                          f'Играем дальше? Выбери цвет.'
                                          , parse_mode='html', reply_markup=markup)
    elif call.data == "change_bet":
        default_bet = 0
        cursor.execute(f'UPDATE users SET bet = "{default_bet}" WHERE user_id = "{user_id}"')
        conn.commit()
        upd_balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        msg2 = bot.send_message(call.message.chat.id, text=f"🎲 <b>Рулетка</b> \n\n"
                                                     f"Введите сумму ставки.\n"
                                                     f"Доступно для игры: <code>{upd_balance}</code> монет",
                                                     parse_mode="HTML")
        bot.register_next_step_handler(msg2, userbetchange)

    elif call.data == "withdrawal":
        bot.send_message(call.message.chat.id, text=f"В разработке...", parse_mode="HTML")

    elif call.data == "addfunds":
        bot.send_message(call.message.chat.id, text=f"В разработке...", parse_mode="HTML")

    else:
        print(f"user bet:{call.data}")
        bot.answer_callback_query(call.id, "Вы проиграли :(")

        cursor.execute(f'UPDATE users SET balance = (balance - bet) WHERE user_id = "{user_id}"')
        conn.commit()
        cursor.execute(f'UPDATE users SET gamesplayed = (gamesplayed + 1) WHERE user_id = "{user_id}"')
        conn.commit()
        cursor.execute(f'UPDATE users SET gameslose = (gameslose + 1) WHERE user_id = "{user_id}"')
        conn.commit()

        upd_balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        bot.send_message(call.message.chat.id, f'🎲 <b>Проигрыш!</b>\n\n'
                                          f'Баланс: <code>{upd_balance}</code> монет.\n'
                                          f'Сумма ставки: <code>{userbet}</code> монет.\n\n'
                                          f'Играем дальше? Выбери цвет.'
                                          , parse_mode='html', reply_markup=markup)


def userbetchange(message):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Назад", callback_data="change_bet")
    markup.add(button)

    try:
        default_bet = 0
        user_id = message.from_user.id
        us_balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        us_bet = message.text

        if int(us_bet) <= int(us_balance) and int(us_bet) > 0:
            cursor.execute(f'UPDATE users SET bet = "{us_bet}" WHERE user_id = "{user_id}"')
            conn.commit()
            upd_balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]

            msg = bot.send_message(message.chat.id, f'📢 <b>Внимание</b>\n\n'
                                              f'Сумма ставки: <code>{us_bet}</code> монет. \n\n'
                                              f'Если вы подтверждаете ставку,\n'
                                              f'напишите "<b>Подтверждаю</b>".'
                                              , parse_mode='html')
            bot.register_next_step_handler(msg, playcasino)

        else:
            bot.send_message(message.chat.id, '🚫 <b>Ошибка</b>\n\n'
                                              'Сумма ставки не должна превышать ваш баланс, а так же\n'
                                              'быть меньше или равной нулю!\n'
                                              'Попробуйте снова. '
                                              , parse_mode='html', reply_markup=markup)
            cursor.execute(f'UPDATE users SET bet = "{default_bet}" WHERE user_id = "{user_id}"')
            conn.commit()

    except Exception as e:
        default_bet = 0
        user_id = message.from_user.id
        bot.send_message(message.chat.id, '🚫 <b>Ошибка</b>\n\n'
                                          'Ставка должна быть числом!\n'
                                          'Попробуйте снова. '
                                          , parse_mode='html', reply_markup=markup)
        cursor.execute(f'UPDATE users SET bet = "{default_bet}" WHERE user_id = "{user_id}"')
        conn.commit()

bot.infinity_polling()