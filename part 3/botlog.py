from datetime import datetime
from time import time

class BotLog(object):

    def __init__(self):
        pass

    def timestamp(self):
        return "[ " + datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S') + " ]\t"

    def log(self, message, type="info"):
        return
        timestamp = self.timestamp()

        message = timestamp + message

        if type == "success":
            message = "\033[92m" + message
        elif type == "error":
            message = "\033[91m" + "ERROR: " + message

        message += "\033[0m"

        print(message)
        # pass