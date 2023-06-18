import telebot
from telebot import types
import blackjack
from telebot.types import InputMediaPhoto
from PIL import Image
import io

balances = {}
hand_of_player = []
hand_of_player_show = []

hand_of_casino = []
hand_of_casino_show = []
bet = 0


markup_pred_game = types.ReplyKeyboardMarkup(resize_keyboard=True)
but1 = types.KeyboardButton("Посмотреть свой баланс")
but2 = types.KeyboardButton("Сделать ставку")
markup_pred_game.add(but1, but2)

markup_in_game = types.ReplyKeyboardMarkup(resize_keyboard=True)
but3 = types.KeyboardButton("Удвоить ставки")
but4 = types.KeyboardButton("Взять карту")
but5 = types.KeyboardButton("Достаточно")
markup_in_game.add(but3, but4, but5)

markup_bet = types.ReplyKeyboardMarkup(resize_keyboard=True)
but6 = types.KeyboardButton("50")
but7 = types.KeyboardButton("100")
but8 = types.KeyboardButton("150")
but9 = types.KeyboardButton("200")
markup_in_game.add(but6, but7, but8, but9)


def process_bet(message):
    try:
        # Получаем сумму ставки из сообщения пользователя
        global bet
        global markup_bet
        bet = int(message.text)
        # Например, передать ее функции `blackjack.make_bet()` для обработки
        blackjack.make_bet(check_balance(message.from_user.id), bet)
        if check_balance(message.from_user.id) < bet:
            bot.send_message(message.chat.id, "Недостаточно фишек!")
            t = int("gg")
        update_balance(message.from_user.id, -bet)
        # Отправляем сообщение с подтверждением ставки
        bot.send_message(message.chat.id, f"Вы сделали ставку: {bet}")
        bot.send_message(message.chat.id, "Игра началась")

        blackjack.take_cards(hand_of_player, hand_of_player_show, 2)
        blackjack.take_cards(hand_of_casino, hand_of_casino_show, 1)

        send_cards(hand_of_player_show, message, "Ваши карты:")

        if blackjack.game_sum(hand_of_player) == 21:
            blackjack.take_cards(hand_of_casino, hand_of_casino_show, 1)
            send_cards(hand_of_casino_show, message, "Карты диллера: ")
            win = blackjack.win_and_lose_start(hand_of_player, hand_of_casino, bet)
            if win:
                if win == 2.5:
                    update_balance(message.chat.id, win * bet)
                    bot.send_message(
                        message.chat.id,
                        f"Блэкджек! Поздравляю, вы выиграли {(win-1)*bet} фишек!",
                    )
                    blackjack.clean(
                        hand_of_player,
                        hand_of_player_show,
                        hand_of_casino,
                        hand_of_casino_show,
                    )
                    bot.send_message(
                        message.chat.id,
                        "Выберите действие: ",
                        reply_markup=markup_pred_game,
                    )
                else:
                    bot.send_message(message.chat.id, "При своих")
                    blackjack.clean(
                        hand_of_player,
                        hand_of_player_show,
                        hand_of_casino,
                        hand_of_casino_show,
                    )
                    bot.send_message(
                        message.chat.id,
                        "Выберите действие: ",
                        reply_markup=markup_pred_game,
                    )
        else:
            send_cards(hand_of_casino_show, message, "Карты диллера: ")
    except ValueError:
        bot.send_message(
            message.chat.id, "Некорректная сумма ставки. Попробуйте снова."
        )


def send_cards(hand, message, caption):
    media = []
    for i in hand:
        f = i[0] + i[1] + ".jpg"
        photo_path = "cards/" + f
        with open(photo_path, "rb") as photo_file:
            photo_data = photo_file.read()  # Сохраняем содержимое файла в переменную
        media.append(InputMediaPhoto(photo_data))
    bot.send_message(message.chat.id, caption)
    bot.send_media_group(message.chat.id, media)


def result_game(message, bet, choose):
    blackjack.make_casino_hand(hand_of_casino, hand_of_casino_show)
    send_cards(hand_of_casino_show, message, "Карты диллера: ")
    win = blackjack.win_and_lose(hand_of_player, hand_of_casino, choose)

    if win > 1:
        update_balance(message.chat.id, win * bet)
        bot.send_message(
            message.chat.id, f"Поздравляю, вы выиграли {(win-1)*bet} фишек!"
        )
        blackjack.clean(
            hand_of_player, hand_of_player_show, hand_of_casino, hand_of_casino_show
        )

    elif win == 1:
        bot.send_message(message.chat.id, "При своих")
        blackjack.clean(
            hand_of_player, hand_of_player_show, hand_of_casino, hand_of_casino_show
        )
    else:
        update_balance(message.chat.id, win * bet)
        bot.send_message(message.chat.id, f"Вы проиграли {abs((win-1)*bet)} фишек")
        blackjack.clean(
            hand_of_player, hand_of_player_show, hand_of_casino, hand_of_casino_show
        )


def check_balance(user_id):
    balance = balances.get(user_id, 1000)
    return balance


def update_balance(user_id, amount):
    if user_id in balances:
        balances[user_id] += amount
    else:
        balances[user_id] = 1000 + amount


token = "YOUR_TOKEN"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать игру")
    item2 = types.KeyboardButton("Правила игры")
    markup.add(item1, item2)
    bot.send_message(
        message.chat.id,
        "Привет! Здесь ты сможешь поиграть в блэкджек",
        reply_markup=markup,
    )


@bot.message_handler(content_types="text")
def message_reply(message):
    global bet
    global markup_pred_game
    if message.text == "Правила игры":
        bot.send_message(
            message.chat.id,
            "На этой странице вы можете ознакомиться с правилами: https://ru.wikipedia.org/wiki/%D0%91%D0%BB%D1%8D%D0%BA%D0%B4%D0%B6%D0%B5%D0%BA",
        )
    elif message.text == "Начать игру":
        bot.send_message(
            message.chat.id, "Выберите действие: ", reply_markup=markup_pred_game
        )
    elif message.text == "Посмотреть свой баланс":
        bot.send_message(
            message.chat.id,
            f"Ваш текущий баланс: {check_balance(message.from_user.id)}",
        )
    elif message.text == "Сделать ставку":
        global markup_in_game
        bot.send_message(
            message.chat.id,
            "Укажите сумму ставки:",
            reply_markup=markup_bet,
        )
        bot.register_next_step_handler(message, process_bet)
        bot.send_message(
            message.chat.id,
            "Выберите действие:",
            reply_markup=markup_in_game,
        )
    elif message.text == "Удвоить ставки":
        blackjack.take_cards(hand_of_player, hand_of_player_show, 1)
        send_cards(hand_of_player_show, message, "Ваши карты:")
        result_game(message, bet, 1)
        bot.send_message(
            message.chat.id, "Выберите действие: ", reply_markup=markup_pred_game
        )
    elif message.text == "Достаточно":
        result_game(message, bet, 3)
        bot.send_message(
            message.chat.id, "Выберите действие: ", reply_markup=markup_pred_game
        )
    elif message.text == "Взять карту":
        blackjack.take_cards(hand_of_player, hand_of_player_show, 1)
        send_cards(hand_of_player, message, "Ваши карты:")


bot.infinity_polling()
