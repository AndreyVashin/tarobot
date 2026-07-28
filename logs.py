import pickle
from datetime import *
from config import curTimeZone

class Log:
    def __init__(self, type, user, question, cards, result):
        self.type = type # BASIC / HARD / SIGN
        self.user = user # В SIGN - ДАТА
        self.question = question # В SIGN - ЗНАК ЗОДИАКА, В HARD - СПИСОК ВОПРОСОВ И ОТВЕТОВ
        self.cards = cards
        self.result = result
        self.time = datetime.now(curTimeZone)

class LogCascade:
    def __init__(self):
        self.logs = {}
        self.readLogs()

    def readLogs(self):
        with open("data/logs.txt", "rb") as f:
            self.logs = pickle.load(f)

    def writeLogs(self):
        with open("data/logs.txt", "wb") as f:
            pickle.dump(self.logs, f)

    def createNew(self, user, question, cards, result):
        newLog = Log(user, qustion, cards, result)
        if user in list(self.logs.keys()):
            pass
        else:
            self.logs[user] = []
        self.logs[user].append(newLog)
        self.writeLogs()
