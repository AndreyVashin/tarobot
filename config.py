from datetime import *

# VARS
token = "8895043895:AAGAZuDZQXfTqxOVdkYB6to2vA_zKcu__Tk"
paymentToken = "390540012:LIVE:99710"
curTimeZone = timezone(timedelta(hours=3), name="MSK")

card_count_states = {"oneCard": 1, "twoCard": 2, "threeCard": 3}

# AI

req_ai = """Представь, что ты опытный таролог, к которому обратились с вопросом: '(question)', из колоды ты достаешь карты: (cards). Что это может значить? Опиши подробно примерно на 1000 символов и поддерживай стиль мистики и поддержки. Используй эмодзи и только кириллические символы"""

def generateRequest(question, cards):
    card_text = ", ".join([card.name for card in cards])
    res = req_ai.replace("(question)", question)
    res = res.replace("(cards)", card_text)
    return res

more_questions_req_1 = """Представь, что ты опытный таролог, к которому обратились с вопросом: '(question)', задай короткий уточняющий вопрос"""

def generateHardQustion1Request(question):
    return more_questions_req_1.replace("(question)", question)

more_questions_req_2 = """Представь, что ты опытный таролог, к которому обратились с вопросом: '(question)', ты задал уточняющий вопрос '(bot_question1)' и тебе ответили: '(answer1)', задай еще один короткий уточняющий вопрос"""

def generateHardQustion2Request(question, bot_question1, answer1):
    res = more_questions_req_2.replace("(question)", question)
    res = res.replace("(bot_question1)", bot_question1)
    res = res.replace("(answer1)", answer1)
    return res

more_questions_req_Done = """Представь, что ты опытный таролог, к которому обратились с вопросом: '(question)', ты задал уточняющий вопрос '(bot_question1)' и тебе ответили: '(answer1)', далее ты задал еще один вопрос '(bot_question2)' и тебе ответили: '(answer2)'. Из колоды ты достаешь карты: (cards). Что это может значить? Опиши подробно примерно на 1000 символов и поддерживай стиль мистики и поддержки. Используй эмодзи и только кириллические символы"""

def generateHardQustionDoneRequest(question, bot_question1, answer1, bot_question2, answer2, cards):
    card_text = ", ".join([card.name for card in cards])
    res = more_questions_req_Done.replace("(question)", question)
    res = res.replace("(bot_question1)", bot_question1)
    res = res.replace("(answer1)", answer1)
    res = res.replace("(bot_question2)", bot_question2)
    res = res.replace("(answer2)", answer2)
    res = res.replace("(cards)", card_text)
    return res

signs = [("Овен", "data/media/sign1.png"),
         ("Телец", "data/media/sign2.png"),
         ("Близнецы", "data/media/sign3.png"),
         ("Рак", "data/media/sign4.png"),
         ("Лев", "data/media/sign5.png"),
         ("Дева", "data/media/sign6.png"),
         ("Весы", "data/media/sign7.png"),
         ("Скорпион", "data/media/sign8.png"),
         ("Стрелец", "data/media/sign9.png"),
         ("Козерог", "data/media/sign10.png"),
         ("Водолей", "data/media/sign11.png"),
         ("Рыбы", "data/media/sign12.png")]

sign_req_ai = """Представь, что ты таролог и тебе нужно сделать предсказание для знака зодиака (sign) на текущий день, из колоды ты достаешь карты: (cards). Что это может значить? Опиши подробно примерно на 1000 символов и поддерживай стиль мистики и поддержки. Используй эмодзи и только кириллические символы"""

def generateSignRequest(sign, cards):
    card_text = ", ".join([card.name for card in cards])
    res = sign_req_ai.replace("(sign)", sign[0])
    res = res.replace("(cards)", card_text)
    return res

# TEXTS

start_text = """
Добро пожаловать!
"""

start_already_text = """
Вы уже зарегистрированы!
"""

to_menu_error_text = """
Используйте кнопки навигации в меню, для появления меню используйте команду /start
"""

menu_text = """
Вы перешли в меню
"""

help_text = """
Справка
Расклад

У вас есть персональная колода карт таро, изначально в ней 78 карт.
После каждого расклада количество карт в вашей колоде уменьшается.
Существует два типа раскладов: простой и с уточнениями.
Вы задаете вопрос колоде, при простом раскладе вы сразу выбираете количество карт, которые нужно достать из колоды (1-3) и она отвечает вам на вопрос.
При выборе вопроса с уточнениями вы тратите 5 монеток и вам задается два уточняющих вопроса, на которые следует ответить максимально честно и кратко, далее выбираете количество карт, и колода отвечает на ваш вопрос.

Перемешивание колоды карт, которое обновляет вашу персональную колоду, стоит 10 монеток, либо при наличии активной подписки колоду можно перемешать раз в день.

Профиль

В вашем профиле вы можете увидеть актуальную информации о количестве монеток, дате регистрации и наличии активной подписки.

Подписка

Подписку можно оформить как за монетки, так и непосредственно за рубли (/paysupport).
Наличие активной подписки дает возможность каждый день перемешивать колоду карт.

Платежи

Команда /paysupport
Мы не собираем информацию о наших пользователях и их платежных средствах, все платежи осуществляются через провайдера ЮКасса.
Конкретные вопросы можно задать администраторам в нашей группе (/we)

"""

paysupport_text = """
Здесь вы можете приобрести монетки, которые нужны для перемешивания колоды, офомления подписки, а также чтобы задавать вопросы с уточнениями;
Кроме этого вы можете оформить подписку непосредственно за рубли
"""

we_text = """
Наша группа в телеграм
https://t.me/+8nTSFuZ8m9VmNmQ6
"""

admin_console_text = """
Вы успешно вошли в консоль администратора, выберите действие
"""

admin_error_text = """
Похоже, вы не являетесь администратором. Вам тут нечего делать)
"""

update_subscribe_text = """
Подписки пользователей успешно обновлены
"""

user_error_text = """
Произошла ошибка при чтении вашего профиля, попробуйте использовать /start
"""

user_base_text = """
👋🏼 Приветствую, (name)

📆 Вы вместе с нами, начиная с (reg_date)
У вас (money) монет 🪙
(sub_info)

Надеюсь, вы довольны использованием данного сервиса
Для подробной информации используйте команду /help
Для информации по поводу платежей используйте команду /paysupport
Чтобы перейте в наш канал и продолжать получать полезную информацию - используйте /we
(admin)
"""

sub_info_text_true = """
Статус подписки активен
Она работает с (date)
Закончится (end)
Чтобы получить информацию о подписке или продлить её - используйте /sub
"""

sub_info_text_false = """
Статус подписки отсутствует
Чтобы получить информацию о подписке или продлить её - используйте /sub
"""

admin_text = """
Вы являетесь администратором. Подробнее /admin
"""

def generateSubInfoText(user):
    if user.subscribe:
        res = sub_info_text_true
        date1 = user.subscribeDate.strftime("%d.%m.%Y %H:%M")
        subEndDate = user.getEndSubscribeDate()
        date2 = subEndDate.strftime("%d.%m.%Y %H:%M")
        res = res.replace("(date)", date1)
        res = res.replace("(end)", date2)
        return res
    else:
        return sub_info_text_false

def generateUserText(user):
    name = user.name
    reg_date = user.registrationDate.strftime("%d.%m.%Y %H:%M")
    money = str(user.money)
    sub_info = generateSubInfoText(user)
    if user.admin:
        admin = admin_text
    else:
        admin = ""
    res = user_base_text
    res = res.replace("(name)", name)
    res = res.replace("(reg_date)", reg_date)
    res = res.replace("(money)", money)
    res = res.replace("(sub_info)", sub_info)
    res = res.replace("(admin)", admin)
    return res

hard_question_confirm_text = "Купить вопрос с уточнениями за 5 монеток?"

sort_text_success = "Колода карт успешно перемешана\nТеперь в вашей колоде 78 карт"
sort_text_failed_sub = "Похоже, вы не можете бесплатно перемешать колоду\nКупить перемешивание колоды за 10 монеток?"

money_pay_failed_text = "Похоже, у вас не хватает монет. Для информации по поводу платежей используйте команду /paysupport"

card_info_text = """
В вашей колоде осталось (count) карт(count_letter)
Чтобы обновить количество карт необходимо перемешать колоду

Выберите, что вы хотите сделать:
Простой вопрос - вы задаете один вопрос;
Вопрос с уточнениями (Стоимость 5 Монеток) - вы задаете вопрос, после чего вам будут заданы два вопроса для уточнений, на которые нужно будет честно ответить;
Перемешать (Стоимость 10 Монеток / Подписка) - обновление и перемешивание вашей персональной колоды.
"""

def generateCardInfoText(count):
    if str(count)[-1] == "1":
        count_letter = "а"
    elif str(count)[-1] in ["2", "3", "4"]:
        count_letter = "ы"
    else:
        count_letter = ""
    res = card_info_text.replace("(count)", str(count))
    res = res.replace("(count_letter)", count_letter)
    return res

card_count_text = """
Теперь выберите, сколько карт вы хотите достать из колоды
"""

card_count_error_text = """
Похоже, сейчас вы не можете выбрать количество карт, попробуйте использовать /start
"""

card_count_notenough_text = """
Похоже, в вашей персональной колоде не хватает карт, вы можете выбрать меньше карт или перемешать колоду
"""

basic_question_text = """
Вы выбрали простой вопрос
Теперь задайте свой вопрос колоде
"""

hard_question_text = """
Вы успешно выбрали вопрос с уточнениями
Теперь задайте свой вопрос колоде
"""

buy_sub_money_confirm_text = "Купить (days) дней подписки за (price) монеток?"

def generateBuySubMoneyConfirmText(days, price):
    res = buy_sub_money_confirm_text.replace("(days)", str(days))
    res = res.replace("(price)", str(price))
    return res

buy_sub_success_text = "Подписка на (days) дней успешно оформлена"

def generateBuySubSuccessText(days):
    return buy_sub_success_text.replace("(days)", str(days))

buy_money_success_text = "Вы успешно купили (money) монеток"

def generateBuyMoneySuccessText(money):
    return buy_money_success_text.replace("(money)", str(money))

new_sub_text = "Выберите, на сколько дней вы хотите оформить подписку"
donate_text = "Выберите, сколько монеток вы хотите приобрести"

# PRICES
pricesSub = [("🔆", 7, 50), # EMOJY, DAYS, PRICE(MONEY)
             ("🔆", 15, 90),
             ("🔆", 30, 150),
             ("🔥", 90, 400),
             ("🔥", 180, 700),
             ("💣", 365, 1200)]
pricesSubRub = [("🔆", 7, 149), # EMOJY, DAYS, PRICE(RUBLES)
                ("🔆", 15, 275),
                ("🔆", 30, 438),
                ("🔥", 90, 1066),
                ("🔥", 180, 1802),
                ("💣", 365, 2866)]
pricesMoney = [("🔆", 30, 93), # EMOJY, MONEY, PRICE(RUBLES)
               ("🔆", 50, 149),
               ("🔥", 100, 289),
               ("🔥", 200, 533),
               ("🔥", 500, 1269),
               ("💣", 1000, 2333)]
