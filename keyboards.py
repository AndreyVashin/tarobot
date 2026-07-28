from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config

def generateStartKeyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✨ Перейти к раскладу", callback_data="toCascade"))
    builder.row(InlineKeyboardButton(text="🧝🏼 Профиль", callback_data="toProfile"))
    builder.row(InlineKeyboardButton(text="ℹ️ Информация", callback_data="toHelp"))
    builder.row(InlineKeyboardButton(text="💵 Платежная информация", callback_data="toPaySupport"))
    builder.row(InlineKeyboardButton(text="🔮 Наш канал", callback_data="toWe"))
    builder.adjust(1)
    return builder.as_markup()

def generateCascadeKeyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="❔ Задать простой вопрос", callback_data="toSimpleQuestion"))
    builder.row(InlineKeyboardButton(text="❓ Задать вопрос с уточнениями", callback_data="toHardQuestionConfirm"))
    builder.row(InlineKeyboardButton(text="🙌🏼 Перемешать колоду", callback_data="sortCascadeConfirm"))
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="menu"))
    builder.adjust(1)
    return builder.as_markup()

def generateHardQuestionConfirmKeyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✨ Купить", callback_data="toHardQuestion"))
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="toCascade"))
    builder.adjust(1)
    return builder.as_markup()

def generateSortCascadeConfirmKeyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✨ Купить", callback_data="sortCascade"))
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="toCascade"))
    builder.adjust(1)
    return builder.as_markup()

def generateCardCountKeyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="☝🏼 Тянуть одну карту", callback_data="oneCard"))
    builder.row(InlineKeyboardButton(text="✌🏼 Тянуть две карты", callback_data="twoCard"))
    builder.row(InlineKeyboardButton(text="👌🏼 Тянуть три карты", callback_data="threeCard"))
    builder.adjust(1)
    return builder.as_markup()

def generateProfileUnsubKeyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🃏 Оформить подписку", callback_data="toNewSub"))
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="menu"))
    builder.adjust(1)
    return builder.as_markup()

def generateProfileSubKeyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🃏 Продлить подписку", callback_data="toOldSub"))
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="menu"))
    builder.adjust(1)
    return builder.as_markup()

def generateHelpKeyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="menu"))
    builder.adjust(1)
    return builder.as_markup()

def generateSubMoneyConfirmKeyboard(days, price):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✨ Купить", callback_data="buySub_" + str(days) + "_" + str(price)))
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="toSubMoney"))
    builder.adjust(1)
    return builder.as_markup()

def generatePaySupportKeyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🪙 Купить монетки", callback_data="toDonate"))
    builder.row(InlineKeyboardButton(text="🃏 Оформить подписку", callback_data="toSubRub"))
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="menu"))
    builder.adjust(1)
    return builder.as_markup()

def generateSubMoneyKeyboard():
    builder = InlineKeyboardBuilder()
    for el in config.pricesSub:
        emojy, days, price = el
        text = emojy + " " + str(days) + " ДНЕЙ - " + str(price) + " МОНЕТОК"
        state = "buySubConfirm_" + str(days) + "_" + str(price)
        builder.row(InlineKeyboardButton(text=text, callback_data=state))
    builder.row(InlineKeyboardButton(text="👛 Подписаться за рубли", callback_data="toSubRub"))
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="menu"))
    builder.adjust(1)
    return builder.as_markup()

def generateSubRublesKeyboard():
    builder = InlineKeyboardBuilder()
    for el in config.pricesSubRub:
        emojy, days, price = el
        text = emojy + " " + str(days) + " ДНЕЙ - " + str(price) + " РУБЛЕЙ"
        state = "buySubRub_" + str(days) + "_" + str(price)
        builder.row(InlineKeyboardButton(text=text, callback_data=state))
    builder.row(InlineKeyboardButton(text="🪙 Подписаться за монетки", callback_data="toSubMoney"))
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="menu"))
    builder.adjust(1)
    return builder.as_markup()

def generatePayKeyboard():
    builder = InlineKeyboardBuilder()
    for el in config.pricesMoney:
        emojy, money, price = el
        text = emojy + " " + str(money) + " МОНЕТОК - " + str(price) + " РУБЛЕЙ"
        state = "buyMoney_" + str(money) + "_" + str(price)
        builder.row(InlineKeyboardButton(text=text, callback_data=state))
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="menu"))
    builder.adjust(1)
    return builder.as_markup()

def generateAdminKeyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Обновить подписки", callback_data="admin.reloadSubs"))
    builder.row(InlineKeyboardButton(text="Ежедневный гороскоп", callback_data="admin.todaySigns"))
    builder.row(InlineKeyboardButton(text="Выдать подписки", callback_data="admin.giveSub"))
    builder.row(InlineKeyboardButton(text="Выдать монетки", callback_data="admin.giveMoney"))
    builder.row(InlineKeyboardButton(text="Очистить картинки", callback_data="admin.clearTemps"))
    builder.row(InlineKeyboardButton(text="Назначить админа", callback_data="admin.setAdmin"))
    builder.row(InlineKeyboardButton(text="↩️ Назад", callback_data="menu"))
    builder.adjust(1)
    return builder.as_markup()
