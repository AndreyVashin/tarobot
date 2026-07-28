from openai import OpenAI
from datetime import *
import cards
import config

def getRequest(prompt):
    client = OpenAI(
    	api_key="AQVNzc-JYEwgCfOitYSRoVgDOsQ9wu-E1432jleY",
    	base_url="https://ai.api.cloud.yandex.net/v1",
    	project="b1giq834ssua5dlvnd1b"
    )

    response = client.responses.create(
    	prompt={
    		"id": "fvt1nmc9tgltu92ip1l2",
    	},
    	input=prompt,
    )

    return response.output_text


def generateTodaySign():
    content = []
    for sign in config.signs:
        c = cards.createNewCardCascade()
        c.sort()
        print(sign[0], end=" - ")
        table = cards.cardSignTable
        tableName = table.postSign(sign[1])
        cardL = c.get(3)
        img = table.postCards(cardL, True, tableName)
        text = getRequest(config.generateSignRequest(sign, cardL))
        first = sign[0] + " " + datetime.now(config.curTimeZone).strftime("%d.%m.%Y") + "\n"
        card_text = "Выпали карты: " + ", ".join([card.name for card in cardL]) + "\n"
        res = first+card_text+text
        content.append([img, res])
    return content

if __name__ == "__main__":
    c = cards.createNewCardCascade()
    while True:
        a = input("Введите ваш вопрос: ")
        if a=="Перемешать":
            c = cards.createNewCardCascade()
            c.sort()
            print("Колода успешно перемешана")
            continue

        b = int(input("Сколько взять карт (1-3): "))
        cardL = c.get(b)
        if b==1:
            curTable = cards.cardTable1
        if b==2:
            curTable = cards.cardTable2
        if b==3:
            curTable = cards.cardTable3

        for card in cardL:
            print("Вам выпало: " + card.name)

        print(curTable.postCards(cardL, 0, 0))
        print(getRequest(config.generateRequest(a, cardL)))


    # generateTodaySign()

    # state = [0]
    # c = cards.createNewCardCascade()
    # while True:
    #     a = input("Введите ваш вопрос: ")
    #     if a=="Перемешать":
    #         c = cards.createNewCardCascade()
    #         c.sort()
    #         print("Колода успешно перемешана")
    #         continue
    #     else:
    #         if state[0] == 0:
    #             new_question = getRequest(config.generateHardQustion1Request(a))
    #             state[0] = 1
    #             state.append(a)
    #             state.append(new_question)
    #             print(new_question)
    #         elif state[0] == 1:
    #             state[0] = 2
    #             state.append(a)
    #             new_question = getRequest(config.generateHardQustion2Request(state[1], state[2], a))
    #             state.append(new_question)
    #             print(new_question)
    #         elif state[0] == 2:
    #             b = int(input("Сколько взять карт (1-3): "))
    #             cardL = []
    #             if b==1:
    #                 curTable = cards.cardTable1
    #                 cardL.append(c.get())
    #             if b==2:
    #                 curTable = cards.cardTable2
    #                 cardL.append(c.get())
    #                 cardL.append(c.get())
    #             if b==3:
    #                 curTable = cards.cardTable3
    #                 cardL.append(c.get())
    #                 cardL.append(c.get())
    #                 cardL.append(c.get())
    #
    #             for card in cardL:
    #                 print("Вам выпало: " + card.name)
    #
    #             print(curTable.postCards(cardL, 0, 0))
    #             print(getRequest(config.generateHardQustionDoneRequest(state[1], state[2], state[3], state[4], a, cardL)))
    #             state = [0]
