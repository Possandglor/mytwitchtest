import os
import time
import random
import socket
import threading
from datetime import datetime
from operator import indexOf
from queue import Queue

from gemini.gemini import send_message_to_ai
from riot.riot import get_riot_rank
from gemini.Message import Message
from service.arrays_from_files import *
from service.irc import IRCClient

list_for_ruletka = ['Тебя убили... Но ты выжил! DansGame', 'Осечка! KappaPride', 'Мимо!',
                    'Приставив ствол к виску ты обмочил штаны. Не осуждаю!',
                    'Здоровья погибшим, а ты скоро умрешь Kappa', '/timeout']

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
NICK = os.getenv("NICK")
PASS = os.getenv("PASS")

class TwitchBot:
    def __init__(self, channel):
        self.channel = channel
        self.irc_client = IRCClient()
        self.socket = socket.socket()
        self.message_queue = Queue()
        self.message_history = []
        self.pisun = {}
        self.iqs = {}
        self.last_message_time = time.time()
        self.is_started = True
        self.connect()

        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        while self.is_started:
            try:
                response = self.socket.recv(1024).decode('utf-8')
                if 'PING' in response:
                    self.socket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                    continue

                parts = response.split(':')
                if len(parts) < 3:
                    continue

                username = parts[1].split('!')[0]
                message = parts[2].strip()

                self.process_message_new(username, message)
            except Exception as e:
                print(f"Error: {e}")

    def connect(self):
        self.irc_client.join_channel(self.channel)
        self.socket.connect((HOST, PORT))
        self.socket.send(f"PASS {PASS}\r\n".encode("utf-8"))
        self.socket.send(f"NICK {NICK}\r\n".encode("utf-8"))
        self.socket.send(f"JOIN #{self.channel}\r\n".encode("utf-8"))

    def disconnect(self):
        self.irc_client.leave_channel(self.channel)
        self.socket.send(f"PART #{self.channel}\r\n".encode("UTF-8"))
        self.is_started = False

    def send_messages(self):
        while True:
            message_obj = self.message_queue.get()
            self.message_history.append(message_obj)
            if message_obj:
                self.socket.send(f"PRIVMSG #{message_obj.channel} :{message_obj.message}\r\n".encode("utf-8"))
            time.sleep(1.5)

    def process_message_new(self,username,message):
        self.message_history.append(Message(message,self.channel, username))
        last_message_time = time.time()
        # print(line)
        print(f"{datetime.now().strftime('%H:%M:%S')} \033[1;32;40m ' {self.channel}: {username} \033[0;37;40m: {message}")
        if message.startswith(u'!шар'):
            if 'когда' in message:
                self.queue_message(random.choice(when), username)
            elif 'почему' in message:
                self.queue_message(random.choice(because), username)
            else:
                self.queue_message(random.choice(foo), username)

        if (not "@possanbot" in message
                and not message.startswith("!")
                and "<>" not in message and random.randint(0, 100) < 10)\
                and len(self.message_history)>15:
            self.queue_message(send_message_to_ai(self.message_history,message,self.channel, username),username)

        if "@possanbot" in message:
            self.queue_message(send_message_to_ai(self.message_history,message,self.channel, username),username)

        if message.startswith("!ai"):
            self.queue_message(send_message_to_ai(self.message_history,message,self.channel, username),username)
        if message.startswith('!факт'):
            self.queue_message(random.choice(facts),  username)
        if message.startswith('!статус'):
            self.queue_message(random.choice(status), username)
        if message.startswith('!писюн'):
            if username in self.pisun:
                self.queue_message(self.pisun[username], username)
            else:
                self.queue_message("Писюн " + username + " длинной целых " + str(random.randint(1, 35)) + " см! PogChamp",username)
                self.pisun[username] = "Писюн " + username + " длинной целых " + str(
                    random.randint(1, 35)) + " см! PogChamp"
        if message.startswith('!рулетка'):
            com = random.choice(list_for_ruletka)
            if com == '/timeout':
                timeBan = random.randint(0, 400)
                com += ' ' + username + ' ' + str(timeBan)
                self.queue_message(username + " отлетел на " + str(timeBan) + " KappaPride",  username)
            self.queue_message(com,  username)
        if ' + ' in message:
            r = message.split('+')
            self.queue_message(r[0] + 'любит' + r[1] + ' на ' +str(random.randint(0, 100)) + '%',  username)
        if ' !- ' in message:
            r = message.split('!-')
            self.queue_message(r[0] + 'ненавидит' + r[1] + ' на ' +str(random.randint(0, 100)) + '%', username)

        if message.startswith("!leave"):
            self.disconnect()

        if ' <> ' in message:
            r = message.split('<>')
            self.queue_message(random.choice(r), username)

        if message.startswith('!прогноз'):
            r = message[9:]
            self.queue_message(r + ' вероятно на ' +str(random.randint(0, 100)) + '%',  username)
        if message.startswith('!elo'):
            server = message.split(' ')[-1]
            rank = get_riot_rank(message[5:message.index(server)-1], server)

            self.queue_message(rank, username)
        if message.startswith('!love'):
            r = message[6:]
            self.queue_message(username + ' любит ' + r + ' на ' +str(random.randint(0, 100)) + '%',  username)
        if message.startswith('!шанс'):
            self.queue_message(f"Шанс вырастить дополнительную хромосому у {username} составляет {random.randint(0, 100)}% PogChamp",username)

        if message.startswith('!цитата'):
            if len(message) > 7:
                cit = []
                print(message.split(' ')[1])
                for i in quotes:
                    if message.split(' ')[1] in i:
                        cit.append(i)
                        print(i)
                self.queue_message(random.choice(cit), username)
            else:
                self.queue_message(random.choice(quotes), username)
        if message.startswith('!фап '):
            self.queue_message(f"{message[5:]} фапабельно на {random.randint(0, 100)} %",  username)
        if message.startswith('!+ '):
            quotes.append(message[3:])
            with open(os.curdir + '/config/quotes.txt', 'a+', encoding="utf-8") as f:
                f.write(message[3:] + "\n")
            self.queue_message("Цитата добавлена", username)
        if message.startswith('!iq'):
            if 3 < len(message):
                self.queue_message(f"IQ {message[4:]} = {random.randint(0, 200)}", username)
            else:
                if not username in self.iqs:
                    self.iqs[username] = f"IQ {username} = {random.randint(0, 200)}"
                self.queue_message(self.iqs[username], username)

    def process_message(self, username, message):
        self.last_message_time = time.time()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {self.channel}: {username}: {message}")

        if message.startswith('!факт'):
            self.queue_message(random.choice(["Факт 1", "Факт 2"]), username)
        elif message.startswith('!шанс'):
            self.queue_message(f"Шанс у {username} – {random.randint(0, 100)}%", username)
        # elif message.startswith('!рулетка'):
        #     result = random.choice(list_for_ruletka)
        #     if result == '/timeout':
        #         timeBan = random.randint(0, 400)
        #         result = f"{username} отлетел на {timeBan} KappaPride"
        #     self.queue_message(result, username)
        elif message.startswith('!писюн'):
            if username not in self.pisun:
                self.pisun[username] = f"Писюн {username} длинной {random.randint(1, 35)} см! PogChamp"
            self.queue_message(self.pisun[username], username)
        elif message.startswith('!ai'):
            self.queue_message(send_message_to_ai(self.message_history,message[3:], self.channel, username),username)
        elif message.startswith('!elo'):
            server = message.split(' ')[-1]
            rank = get_riot_rank(message[5:message.index(server)],server)

            self.queue_message(rank, username)
        elif message.startswith('!love'):
            self.queue_message(f"{username} любит {message[6:]} на {random.randint(0, 100)}%", username)

    def queue_message(self, message, username):
        self.irc_client.send_message(self.channel,message)
        # self.message_queue.put(Message(message, self.channel, username))

