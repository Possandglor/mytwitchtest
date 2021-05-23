# coding: utf-8
import random
import socket
import io
import time
import os
import Ui_Form1
from threading import Thread
from datetime import datetime
dir = os.path.abspath(os.curdir)
fname = 'ball.txt'
with open(dir+'/config/'+fname,'r',encoding='utf-8') as f:
    s = f.read()
foo = s.split('\n')
with open(dir+'/config/fact.txt','r',encoding='utf-8') as f:
    s = f.read()
facts = s.split('\n')
with open(dir+'/config/quotes.txt','r',encoding='utf-8') as f:
    s = f.read()
quotes = s.split('\n')
with open(dir+'/config/when.txt','r',encoding='utf-8') as f:
    s = f.read()
when = s.split('\n')
with open(dir+'/config/because.txt','r',encoding='utf-8') as f:
    s = f.read()
because = s.split('\n')
with open(dir+'/config/status.txt','r',encoding='utf-8') as f:
    s = f.read()
status = s.split('\n')

filmname = "Мстители 3"
HOST = "irc.twitch.tv"
PORT = 6667
#NICK = 'barbar_bot'
#PASS = 'oauth:sg8p20t7nodc9j161lh8szlzkb95q6'
NICK = "possanbot"
PASS = 'oauth:dsh0bwfklly5w3gvuplakswthbh22d'

CHANNEL = 'possandglor'#input("Channel: ")

msgs = []
def send_message(message):
    print(str(datetime.now().strftime("%H:%M:%S")) +" \033[1;32;40m " + NICK + "\033[0;37;40m: " + message)
    s.send(bytes("PRIVMSG #" + CHANNEL + " :" + message + "\r\n", "UTF-8"))

class Sender(Thread):
    def __init__(self, name):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name
    def run(self):
        """Запуск потока"""
        while True:
            if len(msgs) > 0:
                send_message(msgs[0])
                msgs.pop(0)
                time.sleep(1.5)

s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #" + CHANNEL+" \r\n", "UTF-8"))

rulet = ['Тебя убили... Но ты выжил! DansGame','Осечка! KappaPride','Мимо!','Приставив ствол к виску ты обмочил штаны. Не осуждаю!','Здоровья погибшим, а ты скоро умрешь Kappa','/timeout']
while True:
    line = s.recv(1024).decode('utf-8')
    if "End of /NAMES list" in line:
        break
W
thread = Sender("Potok")
thread.start()

while True:
    for line in s.recv(1024).decode('utf-8').split('\\r\\n'):
        if 'PING :tmi.twitch.tv' in line:
            s.send(bytes('PONG :tmi.twitch.tv\r\n', "UTF-8"))

        parts = line.split(':')
        if len(parts) < 3:
            continue
        if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
            message = parts[2][:len(parts[2])].strip()
        usernamesplit = parts[1].split("!")
        username = usernamesplit[0]

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
        if message.startswith('!рулетка'):
            com = random.choice(rulet)
            if com=='/timeout':
                timeBan = random.randint(0,400)
                com += ' '+username+' '+str(timeBan)
                msgs.append(username+" отлетел на "+str(timeBan)+" KappaPride")
            msgs.append(com)
        if ' + ' in message:
            r = message.split('+')
            msgs.append(r[0]+'любит'+r[1]+' на '+str(random.randint(0,100))+'%')
        if ' !- ' in message:
            r = message.split('!-')
            msgs.append(r[0]+'ненавидит'+r[1]+' на '+str(random.randint(0,100))+'%')

        if ' <> ' in message:
            r = message.split('<>')
            msgs.append(random.choice(r))
        if message.startswith('!love'):
            r = message[6:]
            msgs.append(username+' любит '+r+' на '+str(random.randint(0,100))+'%')
        if message.startswith('!фильм'):
            msgs.append(filmname)
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
