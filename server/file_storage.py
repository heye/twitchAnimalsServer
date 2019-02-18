
from typing import Dict, Tuple, List
import os
import traceback

temp_path = "/home/he/temp/"

def setup():
    try:
        os.mkdir(temp_path)
    except FileExistsError:
        return
    except:
        traceback.print_exc()

        
#add data to a temporary file
def write_file(data: str) -> bool:
    result = False

    try:    
        file_path = temp_path + "names.txt"

        with open(file_path, 'w+') as temp_file:
            temp_file.write(data)
            result = True
    except:
        traceback.print_exc()
    
    return result


def append_file(data: str) -> bool:
    result = False

    try:    
        file_path = temp_path + "names.txt"

        with open(file_path, 'a+') as temp_file:
            temp_file.write(data)
            result = True
    except:
        traceback.print_exc()
    
    return result


def read_file() -> bytes:
    data = ""

    try:
        file_path = temp_path + "names.txt"

        if not os.path.isfile(file_path):
            return data
    
        with open(file_path, 'r+') as temp_file:
            data = temp_file.read()
    except:
        traceback.print_exc()
    return data


