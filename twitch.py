# coding: utf-8
from math import e, pi
import random
import socket
import io
import time
import os
import json
import requests
import pytchat

from threading import Thread
from datetime import datetime
RG_API = ""
dir = os.path.abspath(os.curdir)
with open(dir+'/rgapi.txt', 'r', encoding='utf-8') as f:
    RG_API = f.read()
    print(RG_API)
fname = 'ball.txt'
with open(dir+'/config/'+fname, 'r', encoding='utf-8') as f:
    s = f.read()
foo = s.split('\n')
with open(dir+'/config/fact.txt', 'r', encoding='utf-8') as f:
    s = f.read()
facts = s.split('\n')
with open(dir+'/config/quotes.txt', 'r', encoding='utf-8') as f:
    s = f.read()
quotes = s.split('\n')
with open(dir+'/config/when.txt', 'r', encoding='utf-8') as f:
    s = f.read()
when = s.split('\n')
with open(dir+'/config/because.txt', 'r', encoding='utf-8') as f:
    s = f.read()
because = s.split('\n')
with open(dir+'/config/status.txt', 'r', encoding='utf-8') as f:
    s = f.read()
status = s.split('\n')

with open(dir+'/config/lolnicks.txt', 'r', encoding='utf-8') as f:
    s = f.read()
lolnicks = s.split('\n')
lolNicksArray = []
for i in lolnicks:
    lolNicksArray.append(i.split('|')[0])
with open(dir+'/config/nick.txt', 'r', encoding='utf-8') as f:
    nicks = f.read().split('\n')
global seks
seks = 0
filmname = "Мстители 3"
HOST = "irc.twitch.tv"
PORT = 6667
# NICK = 'barbar_bot'
# PASS = 'oauth:sg8p20t7nodc9j161lh8szlzkb95q6'
# NICK = 'barbarsbot'
# PASS = 'oauth:deks0qew7gr3u8ppaju6a99mnrjaau'
NICK = "possanbot"
PASS = 'oauth:dsh0bwfklly5w3gvuplakswthbh22d'
#''  #
CHANNEL = 'possandglor'# input("Channel: ")

msgs = []
chnls = []
pisun = {}
iqs={}

def send_message(chnnl,message):
    print(str(datetime.now().strftime("%H:%M:%S")) +
          " \033[1;32;40m "+chnnl+": " + NICK + "\033[0;37;40m: " + message)
    s.send(bytes("PRIVMSG #" + chnnl + " :" + message + "\r\n", "UTF-8"))


chat = pytchat.create(video_id="m3l94vZdUA0")


class YoutubeGetter(Thread):
    def __init__(self, name):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name

    def run(self):
        while chat.is_alive():
            mes = chat.get().json()
            mes = json.loads(mes)
            # print(mes)
            author = ""
            message = ""
            for i in mes:
                for key, value in i.items():
                    # print(key)
                    # print(value)
                    if key == "author":
                        for key1, value1 in value.items():
                            if key1 == "name":
                                author = value1
                    if key=="message":
                        message = value
                msgs.append(author + " говорит: "+message)
                chnls.append("terzief")
            time.sleep(1)
        

class Sender(Thread):
    def __init__(self, name):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name

    def run(self):
        """Запуск потока"""
        while True:
            if len(msgs) > 0:
                send_message(chnls[0],msgs[0])
                msgs.pop(0)
                chnls.pop(0)
                time.sleep(1.5)


s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))

for i in nicks:
    s.send(bytes("JOIN #" + i+" \r\n", "UTF-8"))
    time.sleep(1)
    # print(i)

rulet = ['Тебя убили... Но ты выжил! DansGame', 'Осечка! KappaPride', 'Мимо!',
         'Приставив ствол к виску ты обмочил штаны. Не осуждаю!', 'Здоровья погибшим, а ты скоро умрешь Kappa', '/timeout']
while True:
    line = s.recv(1024).decode('utf-8')
    if "End of /NAMES list" in line:
        break

thread = Sender("Potok")
thread.start()

thread1 = YoutubeGetter("PotokYoutube")
thread1.start()

posList = [", ня!", ", кавай!", ", братик!", ", семпай", ", оничан Kreygasm"]
while True:
    for line in s.recv(1024).decode('utf-8').split('\\r\\n'):
        try:
            if 'PING :tmi.twitch.tv' in line:
                s.send(bytes('PONG :tmi.twitch.tv\r\n', "UTF-8"))
            # print(line)
            parts = line.split(':')
            if len(parts) < 3:
                continue
            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                message = parts[2][:len(parts[2])].strip()
                chnl = parts[1].split(' ')[2].replace("#","")
            usernamesplit = parts[1].split("!")
            username = usernamesplit[0]
            # print(line)
            print(str(datetime.now().strftime('%H:%M:%S')) +
                ' \033[1;32;40m '+chnl+": "+username + "\033[0;37;40m: " + message)
            if message.startswith(u'!шар'):
                if 'когда' in message:
                    msgs.append(random.choice(when))
                    chnls.append(chnl)
                elif 'почему' in message:
                    msgs.append(random.choice(because))
                    chnls.append(chnl)
                else:
                    msgs.append(random.choice(foo))
                    chnls.append(chnl)
            if message.startswith('!факт'):
                msgs.append(random.choice(facts))
                chnls.append(chnl)
            if message.startswith('!статус'):
                msgs.append(random.choice(status))
                chnls.append(chnl)
            if message.startswith('!писюн'):
                if username in pisun:
                    msgs.append(pisun[username])
                else:
                    pisun[username]="Писюн " + username+" длинной целых " + str(random.randint(1, 35))+" см! PogChamp"
                    msgs.append(pisun[username])
                chnls.append(chnl)
            if message.startswith('!рулетка'):
                com = random.choice(rulet)
                if com == '/timeout':
                    timeBan = random.randint(0, 400)
                    com += ' '+username+' '+str(timeBan)
                    msgs.append(username+" отлетел на "+str(timeBan)+" KappaPride")
                    chnls.append(chnl)
                msgs.append(com)
                chnls.append(chnl)
            if ' + ' in message:
                r = message.split('+')
                msgs.append(r[0]+'любит'+r[1]+' на ' +
                            str(random.randint(0, 100))+'%')
                chnls.append(chnl)
            if ' !- ' in message:
                r = message.split('!-')
                msgs.append(r[0]+'ненавидит'+r[1]+' на ' +
                            str(random.randint(0, 100))+'%')
                chnls.append(chnl)
            if '!set' in message:
                global chat
                chat = pytchat.create(video_id=message.split(' ')[1])
                thread1
            if '!секс' in message:
                seks= seks+1
                msgs.append("Секс "+ seks)
                chnls.append(chnl)
            if '!elo' in message:
                try:
                    sumnick = message[6+len(message.split(' ')[1]):len(message)]
                    serv = message.split(' ')[1]
                    if sumnick+'hghj' in lolNicksArray:
                        for i in lolnicks:
                            if sumnick in i:
                                puuid = i.split('|')[1]
                                id = i.split('|')[2]
                                serv = i.split('|')[3]
                    else :
                        print(sumnick+"+")
                        my_url = 'https://'+serv+'.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + \
                            sumnick+'?api_key='+RG_API
                        print(my_url)
                        response = requests.get(
                            my_url,
                            headers={
                                "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.102 Safari/537.36",
                                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                                "Origin": "https://developer.riotgames.com"
                            }
                        )
                        # print(response.content)
                        my_json = json.loads(response.content)
                        # print(my_json)
                        print("\n")
                        for key, value in my_json.items():
                            if key == "puuid":
                                puuid = value
                            if key == "id":
                                id = value
                        print(puuid)
                        print(id)
                        f = open("config/lolnicks.txt","a+")
                        f.write(sumnick+"|"+puuid+"|"+id+"|"+serv+"\n")
                        lolnicks.append(sumnick+"|"+puuid+"|"+id+"|"+serv)
                        lolNicksArray.append(sumnick)
                        f.close()
                    my_url = 'https://'+serv+'.api.riotgames.com/lol/league/v4/entries/by-summoner/' + \
                        id+'?api_key='+RG_API
                    print(my_url)
                    response1 = requests.get(
                    my_url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.102 Safari/537.36",
                        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                        "Origin": "https://developer.riotgames.com"
                    }
                    )
                    eloes = json.loads(response1.content)
                    print(response1.content)
                    text = ""
                    series = ""
                    for i in eloes:
                        print(i)
                        for key, value in i.items():
                            if key == "queueType":
                                text += value.split('_')[1][0]+value.split(
                                    '_')[1][1:len(value.split('_')[1])].lower() + ": "
                            if key == "tier":
                                text += value[0]+value[1:len(value)].lower()+" "
                            if key == "rank":
                                text += value + ", "
                            if key == "leaguePoints":
                                text += str(value) + " LP, "
                            if key == "wins":
                                wins = value
                            if key == "losses":
                                losses = value
                            if key == "hotStreak":
                                if value == True:
                                    text += "winstreak, "
                            if key == "miniSeries":
                                series = "серия: "
                                for key1, value1 in value.items():
                                    if key1 == "wins":
                                        series += "побед: "+str(value1)+", "
                                        print 
                                    if key1 == "losses":
                                        series += "поражений: "+str(value1)+", "                                    
                                    if key1 == "progress":
                                        series += str(value1)+""
                        # games = int(wins)+int(losses)
                        countGames = (wins+losses)
                        text += " WR = " + str(int(wins*1000.0/(wins+losses))/10.0)+"%, "+str(countGames)+" игр"
                        if series != "":
                            text+=", "+series
                        text+="; "
                    # my_url = 'https://'+message.split(' ')[1]+'.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/'+id+'?api_key='+RG_API
                    # print(my_url)
                    # response2 = requests.get(
                    #     my_url,
                    #     headers={
                    #         "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.102 Safari/537.36",
                    #         "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    #         "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                    #         "Origin": "https://developer.riotgames.com"
                    #     }
                    # )
                    # match = json.loads(response2.content)
                    # print(match)

                    # my_url = 'https://EUROPE.api.riotgames.com/lol/match/v5/matches/by-puuid/'+puuid+'/ids?api_key='+RG_API
                    # print(my_url)
                    # response2 = requests.get(
                    #     my_url,
                    #     headers={
                    #         "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.102 Safari/537.36",
                    #         "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    #         "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                    #         "Origin": "https://developer.riotgames.com"
                    #     }
                    # )
                    # match = json.loads(response2.content)
                    # print(match)

                    # my_url = 'https://EUROPE.api.riotgames.com/lol/match/v5/matches/'+match[0]+'?api_key='+RG_API
                    # print(my_url)
                    # response3 = requests.get(
                    #     my_url,
                    #     headers={
                    #         "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.102 Safari/537.36",
                    #         "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    #         "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                    #         "Origin": "https://developer.riotgames.com"
                    #     }
                    # )
                    # idss = json.loads(response3.content)
                    # print(idss)
                    msgs.append(text)
                    chnls.append(chnl)
                except:
                    msgs.append("Что-то не так")
                    chnls.append(chnl)
            if ' <> ' in message:
                r = message.split('<>')
                msgs.append(random.choice(r))
                chnls.append(chnl)
            if message.startswith('!join'):
                r = message[6:]
                s.send(bytes("JOIN #" + r+" \r\n", "UTF-8"))
                f = open("config/nick.txt","a+")
                f.write(r+"\n")
                f.close()
            if message.startswith('!leave') :
                s.send(bytes("PART #" + chnl+" \r\n", "UTF-8"))
                f = open("config/nick.txt","r+")
                sss = f.readlines()
                f.close()
                print(sss)
                sss.remove(chnl+"\n")

                f = open("config/nick.txt","w+")
                for a in sss:
                    f.write(a)
                f.close()
            if message.startswith('!прогноз'):
                r = message[9:]
                msgs.append(r+' вероятно на ' +
                            str(random.randint(0, 100))+'%')
                chnls.append(chnl)
            if message.startswith('!love'):
                r = message[6:]
                msgs.append(username+' любит '+r+' на ' +
                            str(random.randint(0, 100))+'%')
                chnls.append(chnl)
            if message.startswith('!шанс'):
                msgs.append("Шанс вырастить дополнительную хромосому у "+username+' составляет ' +
                            str(random.randint(0, 100))+'% PogChamp')
                chnls.append(chnl)
            if message.startswith('!фильм'):
                msgs.append(filmname)
                chnls.append(chnl)
            if message.startswith('!цитата'):
                if len(message) > 7:
                    cit = []
                    print(message.split(' ')[1])
                    for i in quotes:
                        if message.split(' ')[1] in i:
                            cit.append(i)
                            print(i)
                    msgs.append(random.choice(cit))
                    chnls.append(chnl)
                else:
                    msgs.append(random.choice(quotes))
                    chnls.append(chnl)
            if message.startswith('!фап '):
                msgs.append(message[5:] + ' фапабельно на ' +
                            str(random.randint(0, 100)) + '%')
                chnls.append(chnl)
            if message.startswith('!+ '):
                quotes.append(message[3:])
                with open(dir+'/config/quotes.txt', 'a+',encoding="utf-8") as f:
                    f.write(message[3:]+"\n")
                msgs.append("Цитата добавлена")
                chnls.append(chnl)
            if message.startswith('!iq'):
                if 3 < len(message):
                    msgs.append('IQ '+message[4:]+' = ' +
                                str(random.randint(0, 200)))
                    chnls.append(chnl)
                else:
                    if username in iqs:
                        msgs.append(iqs[username])
                    else:
                        iqs[username]='IQ '+username+' = '+str(random.randint(0, 200))
                        msgs.append(iqs[username])
                    chnls.append(chnl)
            if username == "possandglor":
                msgs[-1] += random.choice(posList)
        except:
            print("")