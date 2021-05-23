# coding: utf-8
import random
import socket
import io
import time
import os
from threading import Thread
from datetime import datetime
import telebot

bot = telebot.TeleBot('1197138814:AAGpfw816K5gDdp2mYKOrOASMDCZuofsQCE')

dir = os.path.abspath(os.curdir)
fname = 'ball.txt'
with open(dir+'/config/'+fname,'r') as f:
    s = f.read()
foo = s.split('\n')
with open(dir+'/config/fact.txt','r') as f:
    s = f.read()
facts = s.split('\n')
with open(dir+'/config/quotes.txt','r') as f:
    s = f.read()
quotes = s.split('\n')
with open(dir+'/config/when.txt','r') as f:
    s = f.read()
when = s.split('\n')
with open(dir+'/config/because.txt','r') as f:
    s = f.read()
because = s.split('\n')
with open(dir+'/config/status.txt','r') as f:
    s = f.read()
status = s.split('\n')


# @bot.message_handler(commands=['start', 'help','писюн'])
# def send_welcome(message):
#     #if()
#     bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')

# @bot.message_handler(content_types=['text'])
# def send_welcome(message):
#     if message.text == '/reg':
#         bot.send_message(message.from_user.id, "Как тебя зовут?");
#         bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
#     else:
#         bot.send_message(message.from_user.id, 'Напиши /reg');
#     #if()
#     #bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')



# msgs = []
# def send_message(message):
#     print(str(datetime.now().strftime("%H:%M:%S")) +" \033[1;32;40m " + NICK + "\033[0;37;40m: " + message)
#     s.send(bytes("PRIVMSG #" + CHANNEL + " :" + message + "\r\n", "UTF-8"))
    
# class Sender(Thread):
#     def __init__(self, name):
#         """Инициализация потока"""
#         Thread.__init__(self)
#         self.name = name
#     def run(self):
#         """Запуск потока"""
#         while True:
#             if len(msgs) > 0:
#                 send_message(msgs[0])
#                 msgs.pop(0)
#                 time.sleep(1.5)

# s = socket.socket()
# s.connect((HOST, PORT))
# s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
# s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
# s.send(bytes("JOIN #" + CHANNEL+" \r\n", "UTF-8"))


# while True:
#     line = s.recv(1024).decode('utf-8')
#     if "End of /NAMES list" in line:
#         break
    
# thread = Sender("Potok")
# thread.start()
msgs = []

def messages(message,username):
    msgs.clear()
    print(str(datetime.now().strftime('%H:%M:%S'))+' \033[1;32;40m '+username + "\033[0;37;40m: " + message)       
    if message.startswith(u'!шар'):
        if 'когда' in message:
            msgs.append(random.choice(when))
        elif 'почему' in message:
            msgs.append(random.choice(because))
        else:
            msgs.append(random.choice(foo))
    if message.startswith('!факт'):
        msgs.append(random.choice(facts))
    if message.startswith('!статус'):
        msgs.append(random.choice(status))
    if message.startswith('!писюн'):
        msgs.append("Писюн "+ username+" длинной целых "+ str(random.randint(1,35))+" см! PogChamp")

    if ' + ' in message:
        r = message.split('+')
        msgs.append(r[0]+'любит'+r[1]+' на '+str(random.randint(0,100))+'%')
    if message.startswith('!random'):
        message = message[8:]
        r = message.split(' ')
        msgs.append(random.choice(r))
    if ' <> ' in message:
        r = message.split('<>')
        msgs.append(random.choice(r))
    if message.startswith('!love'):
        r = message[6:]
        msgs.append(username+' любит '+r+' на '+str(random.randint(0,100))+'%')
    if message.startswith('!цитата'):
        msgs.append(random.choice(quotes))
    if message.startswith('!фап '):
        msgs.append(message[5:] +' фапабельно на '+str(random.randint(0,100)) + '%')
    if message.startswith('!+ '):
        quotes.append(message[3:])
        with open(dir+'/config/quotes.txt','a+') as f:
            f.write(message[3:])


        msgs.append("Цитата добавлена")
    if message.startswith('!iq'):
        if 3 < len(message):
            msgs.append('IQ '+message[4:]+' = '+str(random.randint(0,200)))
        else:
            msgs.append('IQ '+username+' = '+str(random.randint(0,200)))
    print(msgs)
    if len(msgs) > 0:
        return msgs[0]
    else:
        return "  "

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # print(message)
    reply = messages(message.text.replace("/","!"),message.from_user.first_name)
    if reply != "  ":
        bot.reply_to(message, reply)

bot.polling(none_stop=True)