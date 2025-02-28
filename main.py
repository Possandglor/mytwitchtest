from flask import Flask, request

from service.irc import IRCClient
from twitch.twitch import TwitchBot

app = Flask(__name__)

started_bots = {}

irc = IRCClient()
irc.connect()

@app.post("/run")
def start_new_user_chat():
    user_name = request.json["user_name"]
    started_bots[user_name] = TwitchBot(user_name)
    return {"message":"ok"},200

@app.post("/stop")
def stop_user():
    user_name = request.json["user_name"]
    started_bots[user_name].disconnect()
    del started_bots[user_name]
    return {"message":"ok"},200

if __name__ == "__main__":
    app.run()

