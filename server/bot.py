
import time
import sys
import irc.bot
import requests
import urllib.request
import urllib.parse
import traceback
import threading
import names

class BotStore:
    bot = None
    stop = False


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, token, channel):
        self.token = token
        self.channel = '#' + channel
        self.thread = None

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)
                

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)


    def on_pubmsg(self, connection, event):
        try:
            tags = {}
            for one_tag in event.tags:
                key = one_tag.get("key", "")
                value = one_tag.get("value", "")
                tags.update({key:value})

            name = tags.get("display-name", "")
            message = event.arguments[0]
            

            self.handle_message(name, message, connection)
        except:
            traceback.print_exc()


    def handle_message(self, name, message, connection):
        print("FROM " + name)
        names.cache.add_name(name)

        #TODO: add name to cache


    @classmethod
    def start_background(cls, bot):

        bot.thread = threading.Thread(target=bot.start)
        bot.thread.start()


    @classmethod
    def stop_background(cls, bot):
        print("TODO")

        
  