import socket
import threading
import time
from queue import Queue
import os
from utils.singleton import SingletonMeta

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
NICK = os.getenv("NICK")
PASS = os.getenv("PASS")

class IRCClient(metaclass=SingletonMeta):
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.nick = NICK
        self.password = PASS
        self.socket = socket.socket()
        self.message_queue = Queue()
        self.is_running = True

    def connect(self):
        """Подключается к IRC-серверу Twitch."""
        self.socket.connect((self.host, self.port))
        self.socket.send(f"PASS {self.password}\r\n".encode("utf-8"))
        self.socket.send(f"NICK {self.nick}\r\n".encode("utf-8"))

        threading.Thread(target=self.process_messages, daemon=True).start()

        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        while self.is_running:
            try:
                response = self.socket.recv(1024).decode('utf-8')
                if 'PING' in response:
                    self.socket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

            except Exception as e:
                print(e)

    def join_channel(self, channel):
        """Присоединяется к указанному Twitch-каналу."""
        self.socket.send(f"JOIN #{channel}\r\n".encode("utf-8"))

    def leave_channel(self, channel):
        self.socket.send(f"PART #{channel}\r\n".encode("UTF-8"))

    def send_message(self, channel, message):
        """Добавляет сообщение в общую очередь."""
        self.message_queue.put((channel, message))

    def process_messages(self):
        """Обрабатывает очередь сообщений и отправляет их в Twitch."""
        while self.is_running:
            if not self.message_queue.empty():
                channel, message = self.message_queue.get()
                try:
                    self.socket.send(f"PRIVMSG #{channel} :{message}\r\n".encode("utf-8"))
                except Exception as e:
                    print(f"Ошибка отправки сообщения: {e}")
                time.sleep(1.5)  # Защита от спама

    def disconnect(self):
        """Останавливает отправку сообщений и закрывает соединение."""
        self.is_running = False
        self.socket.close()
