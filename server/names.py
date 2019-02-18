
from typing import Dict
import traceback
import file_storage


class cache:
    ret = ""
    names = []

    @classmethod
    def setup(cls):
        file_storage.setup()
        cls.ret = file_storage.read_file()

        for one_name in cls.ret.splitlines():
            if one_name not in cls.names:
                cls.names.append(one_name)
        
        print("INIT")
        print("READ " + cls.ret)
        print("PARSED " + str(cls.names))


    @classmethod
    def list_str(cls) -> str:
        return cls.ret


    @classmethod
    def add_name(cls, name: str) -> str:

        if name not in cls.names:
            cls.names.append(name)        
            cls.ret += name + '\n'
            if len(cls.names) > 80:
                cls.names.pop(0)
                
                fist_line_length = 0
                for c in cls.ret:
                    fist_line_length  = fist_line_length + 1
                    if c == '\n':
                        break
                cls.ret = cls.ret[fist_line_length:]

            file_storage.write_file(cls.ret)
            return "added"

        else:
            cls.names.remove(name)
            cls.names.append(name)

            #double buffer, so the returned list is always full
            new_ret = ""
            for one_name in cls.names:
                new_ret += one_name + "\n"
                cls.ret = new_ret

        return "already_exists"

    @classmethod
    def clear_all(cls) -> str:
        cls.ret = ""
        cls.names = []
        file_storage.write_file("")
        return "cleared"

