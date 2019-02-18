
import time
import sys
import irc.bot
import requests
import urllib.request
import urllib.parse
import traceback
import threading

class BotStore:
    bot = None
    stop = False


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, token, channel):
        self.token = token
        self.channel = '#' + channel

        self.rage_enabled = False

        self.voting = False
        self.vote_start = 0
        self.voted_users = []
        self.vote_duration = 20        
        self.vote_yes = 0
        self.vote_no = 0

        self.raging = []
        self.last_rage = int(time.time())
        self.rage_interval = 1800

        self.animals = []

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)
        

    def push_name(self, name: str):
        try:
            url = "http://159.69.20.162:8070/add/" + name
            f = urllib.request.urlopen(url)
            f.read().decode('utf-8')
        except:
            traceback.print_exc()
        

    def push_rage(self, name: str):
        try:
            url = "http://159.69.20.162:8070/rage/add/" + name
            f = urllib.request.urlopen(url)
            f.read().decode('utf-8')
        except:
            traceback.print_exc()
        

    def pull_animals(self):
        try:
            print("PULL ANIMALS")
            url = "http://159.69.20.162:8070/animals/get"
            f = urllib.request.urlopen(url)
            animals = f.read().decode('utf-8')
            animals_names = []
            for one_name in animals.splitlines():
                print("ANIMAL " + one_name)
                animals_names.append(one_name)

            self.animals = animals_names
        except:
            traceback.print_exc()


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
        print(name)
        self.push_name(name)

        if self.rage_enabled:
            self.check_rage_messages(connection, name, message)
    
        #ENABLE 
        if message == "!rage_enable" and name == "the_heye":
            self.rage_enabled = True
            self.last_rage = int(time.time())
            self.reset_voting()
            print("rage_enable")    

        #DISABLE
        if message == "!rage_disable" and name == "the_heye":
            self.rage_enabled = False
            self.reset_voting()
            print("rage_disable")    


    def check_rage_messages(self, c, name, message):

        #RAGE collect names
        if message == "!rage" and name not in self.raging and name in self.animals:
            self.raging.append(name)

        if message == "!rage" and not name in self.animals:
            c.privmsg(name, "du bist leider kein tier " + name)

        #START
        #start rage vote either automatically every 30 minutes or at command
        if ((self.last_rage + self.rage_interval < int(time.time()))
            or (message == "!rage_vote" and name == "the_heye")):

            #don't do anything if there is no one
            if len(self.raging) == 0:
                print("keiner da zum ragen")
                return
            
            self.last_rage = int(time.time())

            #print voting message
            vote_message = ""
            for one_name in self.raging:
                vote_message += "@" + one_name + " "
            vote_message += " sind durchgedreht und möchte(n) angreifen, dürfen die das? 1 oder 2?"
            c.privmsg(self.channel, vote_message)

            #setup voting
            self.reset_voting()
            self.voting = True
            self.vote_start = int(time.time())    
            print("rage_vote")    

        #voting for YES
        if self.voting and message == "1" and name not in self.voted_users:
            self.voted_users.append(name)
            self.vote_yes = self.vote_yes + 1
            print("yes")
            
        #voting for NO
        if self.voting and message == "2" and name not in self.voted_users:
            self.voted_users.append(name)
            self.vote_no = self.vote_no + 1
            print("no")
            
        #voting end

    def check_vote_end(self):
        if self.voting and self.vote_start + self.vote_duration < int(time.time()):
            #compute result
            vote_res = self.vote_yes/(self.vote_yes + self.vote_no)
            vote_attack = vote_res > 0.6
            print("VOTE" + str(vote_res))

            #write result message
            vote_message = "Vote Ende 1:" + str(self.vote_yes) + " 2:" + str(self.vote_no) 
            if vote_attack:
                vote_message += " bonjwaRIP bonjwaRIP bonjwaRIP"
            else:
                vote_message += " bonjwaSave bonjwaSave bonjwaSave"
            self.connection.privmsg(self.channel, vote_message)
            
            #reset voting
            self.reset_voting()

            for one_name in self.raging:
                self.push_rage(one_name)

            #reset raging again
            self.raging = []


    def reset_voting(self):
            self.voting = False
            self.voted_users = []
            self.vote_yes = 0
            self.vote_no = 0

    @classmethod
    def jobs(cls):
        while not BotStore.stop:
            try:
                if not BotStore.bot:
                    print("NO BOT")
                else:
                    BotStore.bot.do_jobs()

            except:
                traceback.print_exc()

            for i in range(0,10):
                if BotStore.stop:
                    return
                time.sleep(0.5)


    def do_jobs(self):
        print("DO JOB")
        self.pull_animals()
        self.check_vote_end();
        #self.connection.privmsg(self.channel, "halltesto")


def main():
    if len(sys.argv) != 4:
        print("Usage: twitchbot <username> <token> <channel>")
        sys.exit(1)

    username  = sys.argv[1]
    token     = sys.argv[2]
    channel   = sys.argv[3]

    bot = TwitchBot(username, token, channel)
    BotStore.bot = bot

    botJobThread = threading.Thread(target=TwitchBot.jobs)
    botJobThread.start()

    bot.start()


if __name__ == "__main__":
    main()