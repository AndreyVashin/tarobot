from datetime import *
import pickle
import cards
import config

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.money = 0
        self.registrationDate = datetime.now(config.curTimeZone)
        self.subscribe = False
        self.subscribeDate = None
        self.subscribeDays = 0
        self.admin = False
        self.cascade = None
        self.todaySort = True # Если сегодня можно перемешать карты - True, если нельзя - False

    def addMoney(self, money):
        self.money += money

    def addSubscribe(self, days):
        if self.subscribe:
            self.subscribeDays += days
        else:
            self.subscribe = True
            self.subscribeDate = datetime.now(config.curTimeZone)
            self.subscribeDays = days

    def removeSubscribe(self):
        self.subscribe = False
        self.subscribeDate = None
        self.subscribeDays = 0

    def getEndSubscribeDate(self):
        if self.subscribeDate == None:
            return None
        return self.subscribeDate + timedelta(days=self.subscribeDays)

    def checkMoney(self, money):
        if self.money >= money:
            return True
        else:
            return False

    def sortCascade(self, forMoney):
        if forMoney:
            if self.checkMoney(config.priceSort):
                self.money -= config.priceSort
                self.cascade = cards.createNewCardCascade()
                self.cascade.sort()
                return config.sort_text_success
            else:
                return config.sort_text_failed_money
        else:
            if self.todaySort:
                self.cascade = cards.createNewCardCascade()
                self.cascade.sort()
                return config.sort_text_success
            else:
                return config.sort_text_failed_sub

def readUsers():
    with open("data/users.txt", "rb") as f:
        l = pickle.load(f)
    return l

def writeUsers(users):
    with open("data/users.txt", "wb") as f:
        pickle.dump(users, f)

def createNewUser(id, name):
    users = readUsers()
    users[id] = User(id, name)
    users[id].cascade = cards.createNewCardCascade()
    users[id].cascade.sort()
    writeUsers(users)

def setAdmin(user):
    users = readUsers()
    users[user].admin = True
    writeUsers(users)

def todaySortUpdate():
    users = readUsers()
    for user in list(users.keys()):
        if users[user].subscribe:
            users[user].todaySort = True
    writeUsers(users)

def updateSubscribe():
    users = readUsers()
    now = datetime.now(config.curTimeZone)
    for user in list(users.keys()):
        if users[user].subscribe:
            now = now.timestamp()
            end = users[user].getEndSubscribeDate().timestamp()
            if now >= end:
                users[user].removeSubscribe()
    writeUsers(users)

class StateCascade:
    def __init__(self):
        self.states = {}
        self.readStates()

    def get(self, id):
        return self.states[id]

    def set(self, id, state):
        self.states[id] = state

    def readStates(self):
        with open("data/states.txt", "rb") as f:
            self.states = pickle.load(f)

    def writeStates(self):
        with open("data/states.txt", "wb") as f:
            pickle.dump(self.states, f)
