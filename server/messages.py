
from typing import Dict
import traceback
from file_storage import FileStorage


class cache:
    messages = {}


    @classmethod
    def add_message(cls, name: str, message:str) -> str:
        cls.messages.update({name: message})


    @classmethod
    def get_message(cls, name:str) -> str:
        message = ""
        try: 
            message = cls.messages.pop(name)
        except:
            print("no message for " + name)
            
        return message

