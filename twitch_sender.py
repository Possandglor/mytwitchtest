# coding: utf-8
import socket

HOST = "irc.twitch.tv"
PORT = 6667
NICK = 'barbar_bot'
PASS = 'oauth:sg8p20t7nodc9j161lh8szlzkb95q6'
CHANNEL = 'skorpak'

s = socket.socket()
def send_message(message):
    s.send(bytes("PRIVMSG #" + CHANNEL + " :" + message + "\r\n","UTF-8"))

s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n","UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n","UTF-8"))
s.send(bytes("JOIN #" + CHANNEL+" \r\n","UTF-8"))

while True:
    st = input()
    send_message(st)
