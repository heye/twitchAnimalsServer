
import os
import ssl
import asyncio
import uvloop
from sanic import Sanic
from sanic import response
import names
import sys
import threading

from server import Server
from bot import TwitchBot


def main():

    if len(sys.argv) != 5:
        print("Usage: twitchbot <username> <token> <channel> <port>")
        sys.exit(1)

    username  = sys.argv[1]
    token     = sys.argv[2]
    channel   = sys.argv[3]
    port   = int(sys.argv[4])

    #init cache
    names.cache.setup()

    #start the bot
    twitch_bot = TwitchBot(username, token, channel)
    TwitchBot.start_background(twitch_bot)

    #run server
    serv = Server()
    serv.run(port)


if __name__ == '__main__':
    main()
