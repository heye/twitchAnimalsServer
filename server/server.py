import os
import ssl
import asyncio
import uvloop
from sanic import Sanic
from sanic import response
import names

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

class Server:

    def __init__(self):
        self.app = Sanic()
        self.channel = ""

        #main functionality add and get names 
        @self.app.route('/<channel>/', methods=['GET'])
        async def handle_request(request, channel):

            #safety
            if channel != self.channel:
                return response.text("")

            return response.text(names.cache.list_str())


    def run(self, port = 8070, channel = ""):
        self.channel = channel
        hostAddr = '0.0.0.0'
        self.app.run(host=hostAddr, port=port, workers=1)