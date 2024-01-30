import telebot
import random
from telebot import types

bot = telebot.TeleBot("6788020972:AAEbB-1vnxI0un95xQjLUvyQeGFg6FLYbKU")
room = {}
key_base = "qwertyuiopasdfghjklzxcvbnm1234567890"
f = open("data.txt")
data = {}
def load():
    global data
    global f
    data = {}
    for i in f:
        a,b,c = i.split()
        data[int(a)] = [int(b), int(c)]
load()
def save():
    global data
    global f
    print(data)
    f.close()
    f = open("data.txt", "w")
    s = ""
    for i in data:
        s += str(i) + " " + str(data[i][0]) + " " + str(data[i][1]) + "\n"
    f.write(s)
    f.close()
    f = open("data.txt")
def get_ph(x):
    return open("c" + str(x) + ".png", "rb")


def won(a, b, c):
    if sum(a) == 21 and sum(b) == 21:
        return 3
    if c == 0:
        if sum(a) == 22 and sum(b) == 22:
            return 3
        if sum(a) == 22:
            return 1
        if sum(b) == 22:
            return 2
        if sum(a) == 21:
            return 1
        if sum(b) == 21:
            return 2
        return 0
    if c == 2:
        if sum(a) == sum(b):
            return 3
        if sum(a) > sum(b):
            return 1
        if sum(b) > sum(a):
            return 2
    if c == 1:
        if sum(a) == 21:
            return 1
        if sum(b) == 21:
            return 2
        if sum(a) > 21:
            return 2
        if sum(b) > 21:
            return 1
        return 0


def name_card(nom):
    return str(nom)


def str_hand(arr):
    s = ""
    for i in arr:
        s += name_card(i) + " "
    return s
def add_stat(pl1, pl2, a1, a2):
    global data
    global f
    data[pl1][0] += a1
    data[pl1][1] += 1 - a1
    data[pl2][0] += a2
    data[pl2][1] += 1 - a2
    save()

def get_rd(ln):
    global key_base
    new_key = ""
    for i in range(ln):
        new_key += key_base[random.randint(0, len(key_base) - 1)]
    return new_key


def creat(rkey):
    global room
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Взять новую карту")
    btn2 = types.KeyboardButton("Пропустить")
    btn3 = types.KeyboardButton("Статистика")
    markup.add(btn1, btn2, btn3)
    bank = []
    for i in range(2, 12):
        if i != 5:
            for j in range(4):
                bank.append(i)
    for i in range(2):
        c = random.randint(0, len(bank) - 1)
        room[rkey][3].append(bank[c])
        bank.pop(c)
    for i in range(2):
        c = random.randint(0, len(bank) - 1)
        room[rkey][4].append(bank[c])
        bank.pop(c)
    room[rkey][2] = bank
    bot.send_message(room[rkey][0], text="Ваши карты: " + str_hand(room[rkey][3]), reply_markup=markup)
    bot.send_message(room[rkey][1], text="Ваши карты: " + str_hand(room[rkey][4]), reply_markup=markup)
    for i in room[rkey][3]:
        bot.send_photo(room[rkey][0], get_ph(i))
    for i in room[rkey][4]:
        bot.send_photo(room[rkey][1], get_ph(i))
    res = won(room[rkey][3], room[rkey][4], 0)
    if res == 1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Создать")
        btn2 = types.KeyboardButton("Присоединиться")
        btn3 = types.KeyboardButton("Статистика")
        markup.add(btn1, btn2, btn3)
        bot.send_message(room[rkey][0], text="Победа!!!", reply_markup=markup)
        bot.send_message(room[rkey][1], text="Поражение....", reply_markup=markup)
        add_stat(room[rkey][0], room[rkey][1], 1, 0)
        room.pop(rkey)
    if res == 2:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Создать")
        btn2 = types.KeyboardButton("Присоединиться")
        btn3 = types.KeyboardButton("Статистика")
        markup.add(btn1, btn2, btn3)
        bot.send_message(room[rkey][1], text="Победа!!!", reply_markup=markup)
        bot.send_message(room[rkey][0], text="Поражение....", reply_markup=markup)
        add_stat(room[rkey][1], room[rkey][0], 1, 0)
        room.pop(rkey)
    if res == 3:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Создать")
        btn2 = types.KeyboardButton("Присоединиться")
        btn3 = types.KeyboardButton("Статистика")
        markup.add(btn1, btn2, btn3)
        bot.send_message(room[rkey][1], text="Ничья", reply_markup=markup)
        bot.send_message(room[rkey][0], text="Ничья", reply_markup=markup)
        room.pop(rkey)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Создать")
    btn2 = types.KeyboardButton("Присоединиться")
    btn3 = types.KeyboardButton("Статистика")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Сыграй с другом в 42/2 очко", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.chat.id not in data:
        data[message.chat.id] = [0, 0]
        save()
    if (message.text == "Создать"):
        new_key = get_rd(7)
        room[new_key] = [message.chat.id, 0, [], [], [], False, False]
        bot.send_message(message.chat.id, text=new_key)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        print(room)
        return
    if (message.text == "Статистика"):
        bot.send_message(message.chat.id, text="Побед: " + str(data[message.chat.id][0]) + " Поражений: " + str(data[message.chat.id][1]))
        return
    if (message.text == "Присоединиться"):
        bot.send_message(message.chat.id, text="Введите ключ комнаты: ")
        print(room)
        return
    
    if (message.text == "Взять новую карту"):
        rkey = -1
        for i in room:
            if room[i][0] != message.chat.id and room[i][1] != message.chat.id:
                pass
            else:
                rkey = i
        if rkey == -1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Создать")
            btn2 = types.KeyboardButton("Присоединиться")
            btn3 = types.KeyboardButton("Статистика")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, text="Вы не в игре", reply_markup=markup)
        else:
            c = random.randint(0, len(room[rkey][2]) - 1)
            on = 0
            if room[rkey][1] == message.chat.id:
                on = 1
            if room[rkey][on + 5]:
                bot.send_message(message.chat.id, text="Вы пропускаете ход")
                return
            room[rkey][on + 3].append(room[rkey][2][c])
            bu = room[rkey][2][c]
            room[rkey][2].pop(c)
            res = won(room[rkey][3], room[rkey][4], 1)
            bot.send_message(message.chat.id, text="Ваши карты: " + str_hand(room[rkey][on + 3]))
            bot.send_photo(message.chat.id, get_ph(bu))

            if res == 1:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Создать")
                btn2 = types.KeyboardButton("Присоединиться")
                btn3 = types.KeyboardButton("Статистика")
                markup.add(btn1, btn2, btn3)
                bot.send_message(room[rkey][0], text="Победа!!!", reply_markup=markup)
                bot.send_message(room[rkey][1], text="Поражение....", reply_markup=markup)
                add_stat(room[rkey][0], room[rkey][1], 1, 0)
                room.pop(rkey)
            if res == 2:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Создать")
                btn2 = types.KeyboardButton("Присоединиться")
                btn3 = types.KeyboardButton("Статистика")
                markup.add(btn1, btn2, btn3)
                bot.send_message(room[rkey][1], text="Победа!!!", reply_markup=markup)
                bot.send_message(room[rkey][0], text="Поражение....", reply_markup=markup)
                add_stat(room[rkey][1], room[rkey][0], 1, 0)
                room.pop(rkey)
            if res == 3:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Создать")
                btn2 = types.KeyboardButton("Присоединиться")
                btn3 = types.KeyboardButton("Статистика")
                markup.add(btn1, btn2, btn3)
                bot.send_message(room[rkey][1], text="Ничья", reply_markup=markup)
                bot.send_message(room[rkey][0], text="Ничья", reply_markup=markup)
                room.pop(rkey)
                print(room)
        return
    if (message.text == "Пропустить"):
        rkey = -1
        for i in room:
            if room[i][0] != message.chat.id and room[i][1] != message.chat.id:
                pass
            else:
                rkey = i
        if rkey == -1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Создать")
            btn2 = types.KeyboardButton("Присоединиться")
            btn3 = types.KeyboardButton("Статистика")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, text="Вы не в игре", reply_markup=markup)
        else:

            on = 0
            if room[rkey][1] == message.chat.id:
                on = 1
            room[rkey][on + 5] = True
            if room[rkey][1 - on + 5] == False:
                return
            res = won(room[rkey][3], room[rkey][4], 2)
            if res == 1:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Создать")
                btn2 = types.KeyboardButton("Присоединиться")
                btn3 = types.KeyboardButton("Статистика")
                markup.add(btn1, btn2, btn3)
                bot.send_message(room[rkey][0], text="Победа!!!", reply_markup=markup)
                bot.send_message(room[rkey][1], text="Поражение....", reply_markup=markup)
                add_stat(room[rkey][0], room[rkey][1], 1, 0)
                room.pop(rkey)
            if res == 2:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Создать")
                btn2 = types.KeyboardButton("Присоединиться")
                btn3 = types.KeyboardButton("Статистика")
                markup.add(btn1, btn2, btn3)
                bot.send_message(room[rkey][1], text="Победа!!!", reply_markup=markup)
                bot.send_message(room[rkey][0], text="Поражение....", reply_markup=markup)
                add_stat(room[rkey][1], room[rkey][0], 1, 0)
                room.pop(rkey)
            if res == 3:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Создать")
                btn2 = types.KeyboardButton("Присоединиться")
                btn3 = types.KeyboardButton("Статистика")
                markup.add(btn1, btn2, btn3)
                bot.send_message(room[rkey][1], text="Ничья", reply_markup=markup)
                bot.send_message(room[rkey][0], text="Ничья", reply_markup=markup)
                room.pop(rkey)
            print(room)
        return
    if (message.text not in room):
        bot.send_message(message.chat.id, text="Такой команды нет, используйте допустимые команды, либо перепроверьете номер ключа")
    else:
        if room[message.text][1] == 0:
            room[message.text][1] = message.chat.id
            creat(message.text)
        else:
            bot.send_message(message.chat.id, text="Комната занята")
    print(room)


bot.polling(none_stop=True)
