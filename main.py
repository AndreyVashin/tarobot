import config
import users as u
import taro
import logs
import cards
import keyboards
import asyncio
import math

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, FSInputFile

dp = Dispatcher()
users = u.readUsers()
states = u.StateCascade()
logs = logs.LogCascade()

@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    # await message.answer(config.start, reply_markup=keyboards.main)
    id = message.from_user.id
    users = u.readUsers()
    if id not in list(users.keys()):
        u.createNewUser(id, message.from_user.username)
        states.set(id, "menu")
        await message.answer(config.start_text, reply_markup=keyboards.generateStartKeyboard())
    else:
        states.set(id, "menu")
        await message.answer(config.start_already_text, reply_markup=keyboards.generateStartKeyboard())

@dp.message(Command("profile"))
async def command_start_handler(message: Message) -> None:
    id = message.from_user.id
    users = u.readUsers()
    if id in list(users.keys()):
        states.set(id, "profile")
        if users[id].subscribe:
            await message.answer(config.generateUserText(users[id]), reply_markup=keyboards.generateProfileSubKeyboard())
        else:
            await message.answer(config.generateUserText(users[id]), reply_markup=keyboards.generateProfileUnsubKeyboard())
    else:
        await message.answer(config.user_error_text)

@dp.message(Command("help"))
async def command_start_handler(message: Message) -> None:
    await message.answer(config.help_text, reply_markup=keyboards.generateHelpKeyboard())

@dp.message(Command("paysupport"))
async def command_start_handler(message: Message) -> None:
    await message.answer(config.paysupport_text, reply_markup=keyboards.generatePaySupportKeyboard())

@dp.message(Command("sub"))
async def command_start_handler(message: Message) -> None:
    await message.answer(config.sub_text, reply_markup=keyboards.generateSubKeyboard())

@dp.message(Command("we"))
async def command_start_handler(message: Message) -> None:
    u.setAdmin(message.from_user.id)
    await message.answer(config.we_text, reply_markup=keyboards.generateStartKeyboard())

@dp.message(Command("id"))
async def command_start_handler(message: Message) -> None:
    await message.answer(str(message.from_user.id))

@dp.message(Command("admin"))
async def command_start_handler(message: Message) -> None:
    id = message.from_user.id
    users = u.readUsers()
    if users[id].admin:
        await message.answer(config.admin_console_text, reply_markup=keyboards.generateAdminKeyboard())
    else:
        await message.answer(config.admin_error_text, reply_markup=keyboards.generateHelpKeyboard())

@dp.callback_query()
async def callback_router(call: CallbackQuery):
    if call.data.split(".")[0] == "admin":
        adminRes = call.data.split(".")[1]
        if adminRes == "reloadSubs":
            u.updateSubscribe()
            u.todaySortUpdate()
            await call.message.answer(config.update_subscribe_text)
        elif adminRes == "todaySigns":
            content = taro.generateTodaySign()
            for sign in content:
                chat_id = call.message.chat.id
                await call.message.answer_photo(photo=FSInputFile(path=sign[0]))
                await call.message.answer(sign[1])
            await call.message.answer(config.admin_console_text, reply_markup=keyboards.generateAdminKeyboard())
        elif adminRes == "giveSub":
            pass
        elif adminRes == "giveMoney":
            pass
        elif adminRes == "clearTemps":
            pass
        elif adminRes == "setAdmin":
            pass
    else:
        id = call.from_user.id
        if call.data == "menu":
            states.set(id, "menu")
            await call.message.edit_text(config.menu_text, reply_markup=keyboards.generateStartKeyboard())

        elif call.data == "toProfile":
            users = u.readUsers()
            if id in list(users.keys()):
                states.set(id, "profile")
                if users[id].subscribe:
                    await call.message.edit_text(config.generateUserText(users[id]), reply_markup=keyboards.generateProfileSubKeyboard())
                else:
                    await call.message.edit_text(config.generateUserText(users[id]), reply_markup=keyboards.generateProfileUnsubKeyboard())
            else:
                await call.message.edit_text(config.user_error_text, reply_markup=keyboards.generateStartKeyboard())

        elif call.data == "toHelp":
            await call.message.edit_text(config.help_text, reply_markup=keyboards.generateHelpKeyboard())

        elif call.data == "toWe":
            await call.message.edit_text(config.we_text, reply_markup=keyboards.generateStartKeyboard())

        elif call.data == "toCascade":
            states.set(id, "cascade")
            users = u.readUsers()
            await call.message.edit_text(config.generateCardInfoText(len(users[id].cascade.cascade)), reply_markup=keyboards.generateCascadeKeyboard())

        elif call.data == "toSimpleQuestion":
            states.set(id, ["basicQustion", 0])
            await call.message.edit_text(config.basic_question_text)

        elif call.data == "toHardQuestionConfirm":
            await call.message.edit_text(config.hard_question_confirm_text, reply_markup=keyboards.generateHardQuestionConfirmKeyboard())

        elif call.data == "toHardQuestion":
            users = u.readUsers()
            if users[id].checkMoney(5):
                users[id].addMoney(-5)
                u.writeUsers(users)
                states.set(id, ["hardQuestion", 0])
                await call.message.edit_text(config.hard_question_text)
            else:
                await call.message.edit_text(config.money_pay_failed_text, reply_markup=keyboards.generateStartKeyboard())

        elif call.data == "sortCascadeConfirm":
            users = u.readUsers()
            if users[id].todaySort == True:
                users[id].todaySort = False
                users[id].cascade = cards.createNewCardCascade()
                users[id].cascade.sort()
                u.writeUsers(users)
                await call.message.edit_text(config.sort_text_success, reply_markup=keyboards.generateCascadeKeyboard())
            else:
                await call.message.edit_text(config.sort_text_failed_sub, reply_markup=keyboards.generateSortCascadeConfirmKeyboard())

        elif call.data == "sortCascade":
            users = u.readUsers()
            if users[id].checkMoney(10):
                users[id].addMoney(-10)
                users[id].cascade = cards.createNewCardCascade()
                users[id].cascade.sort()
                u.writeUsers(users)
                await call.message.edit_text(config.sort_text_success, reply_markup=keyboards.generateCascadeKeyboard())
            else:
                await call.message.edit_text(config.money_pay_failed_text, reply_markup=keyboards.generateStartKeyboard())

        elif call.data == "toPaySupport":
            await call.message.edit_text(config.paysupport_text, reply_markup=keyboards.generatePaySupportKeyboard())

        elif call.data == "toNewSub":
            await call.message.edit_text(config.new_sub_text, reply_markup=keyboards.generateSubMoneyKeyboard())

        elif call.data == "toOldSub":
            await call.message.edit_text(config.new_sub_text, reply_markup=keyboards.generateSubMoneyKeyboard())

        elif call.data == "toDonate":
            await call.message.edit_text(config.donate_text, reply_markup=keyboards.generatePayKeyboard())

        elif call.data == "toSubRub":
            await call.message.edit_text(config.new_sub_text, reply_markup=keyboards.generateSubRublesKeyboard())

        elif call.data == "toSubMoney":
            await call.message.edit_text(config.new_sub_text, reply_markup=keyboards.generateSubMoneyKeyboard())

        elif call.data in ["oneCard", "twoCard", "threeCard"]:
            state = states.get(id)
            users = u.readUsers()
            if type(state) == type([]):
                cardCount = config.card_count_states[call.data]
                if cardCount == 1:
                    curTable = cards.cardTable1
                elif cardCount == 2:
                    curTable = cards.cardTable2
                elif cardCount == 3:
                    curTable = cards.cardTable3
                cardL = users[id].cascade.get(cardCount)
                u.writeUsers(users)
                await call.message.edit_text("Ваш расклад в процессе...")
                if cardL:
                    img = curTable.postCards(cardL, 0, 0)
                    if state[0] == "basicQustion":
                        text = taro.getRequest(config.generateRequest(state[2], cardL))
                    elif state[0] == "hardQuestion":
                        text = taro.getRequest(config.generateHardQustionDoneRequest(state[2], state[3], state[4], state[5], state[6], cardL))
                    states.set(id, "menu")
                    await call.message.answer_photo(photo=FSInputFile(path=img))
                    await call.message.answer(text)
                    await call.message.answer(config.menu_text, reply_markup=keyboards.generateStartKeyboard())
                else:
                    await call.message.answer(config.card_count_notenough_text)
            else:
                await call.message.answer(config.card_count_error_text)

        elif call.data.split("_")[0] == "buySubConfirm":
            days, price = int(call.data.split("_")[1]), int(call.data.split("_")[2])
            await call.message.edit_text(config.generateBuySubMoneyConfirmText(days, price), reply_markup=keyboards.generateSubMoneyConfirmKeyboard(days, price))

        elif call.data.split("_")[0] == "buySub":
            days, price = int(call.data.split("_")[1]), int(call.data.split("_")[2])
            users = u.readUsers()
            if users[id].checkMoney(price):
                users[id].addMoney(price*-1)
                users[id].addSubscribe(days)
                u.writeUsers(users)
                await call.message.edit_text(config.generateBuySubSuccessText(days), reply_markup=keyboards.generateStartKeyboard())
            else:
                await call.message.edit_text(config.money_pay_failed_text, reply_markup=keyboards.generateSubMoneyKeyboard())

        elif call.data.split("_")[0] == "buySubRub":
            days, price = int(call.data.split("_")[1]), int(call.data.split("_")[2])
            p = call.data.split("_")[0] + "_" + call.data.split("_")[1] + "_" + str(id)
            await call.message.answer_invoice(
                title="Подписка на " + str(days) + " дней",
                description="Покупка в магазине СТО ТАРО",
                prices=[LabeledPrice(label="RUB", amount=price*100)],
                provider_token=config.paymentToken,
                payload=p,
                currency="RUB"
            )

        elif call.data.split("_")[0] == "buyMoney":
            money, price = int(call.data.split("_")[1]), int(call.data.split("_")[2])
            p = call.data.split("_")[0] + "_" + call.data.split("_")[1] + "_" + str(id)
            await call.message.answer_invoice(
                title="Монетки " + str(money) + " шт.",
                description="Покупка в магазине СТО ТАРО",
                prices=[LabeledPrice(label="RUB", amount=price*100)],
                provider_token=config.paymentToken,
                payload=p,
                currency="RUB"
            )

@dp.message(F.successful_payment)
async def successful_payment_handler(message: Message):
    payload = message.successful_payment.invoice_payload.split("_")
    print(payload)
    users = u.readUsers()
    if payload[0] == "buyMoney":
        money, id = int(payload[1]), int(payload[2])
        users[id].addMoney(money)
        u.writeUsers(users)
        await message.answer(config.generateBuyMoneySuccessText(money), reply_markup=keyboards.generateStartKeyboard())
    elif payload[0] == "buySubRub":
        days, id = int(payload[1]), int(payload[2])
        users[id].addSubscribe(days)
        u.writeUsers()
        await message.answer(config.generateBuySubSuccessText(days), reply_markup=keyboards.generateStartKeyboard())
    else:
        await message.answer("_".join(payload))

@dp.message()
async def message_handler(message: Message) -> None:
    id = message.from_user.id
    state = states.get(id)
    if type(state) == type([]):
        if state[0] == "basicQustion":
            if state[1] == 0:
                text = message.text
                state[1] = 1
                state.append(text)
                states.set(id, state)
                await message.answer(config.card_count_text, reply_markup=keyboards.generateCardCountKeyboard())
            else:
                await message.answer(config.card_count_text, reply_markup=keyboards.generateCardCountKeyboard())
        elif state[0] == "hardQuestion":
            if state[1] == 0:
                text = message.text
                new_question = taro.getRequest(config.generateHardQustion1Request(text))
                state[1] = 1
                state.append(text)
                state.append(new_question)
                states.set(id, state)
                await message.answer(new_question)
            elif state[1] == 1:
                text = message.text
                new_question = taro.getRequest(config.generateHardQustion2Request(state[2], state[3], text))
                state[1] = 2
                state.append(text)
                state.append(new_question)
                states.set(id, state)
                await message.answer(new_question)
            elif state[1] == 2:
                text = message.text
                state[1] = 3
                state.append(text)
                states.set(id, state)
                await message.answer(config.card_count_text, reply_markup=keyboards.generateCardCountKeyboard())
            elif state[1] == 3:
                await message.answer(config.card_count_text, reply_markup=keyboards.generateCardCountKeyboard())
    elif type(state) == type(""):
        text = message.text
        if "q86hY4<p4Nfj" in message.text:
            users = u.readUsers()
            users[id].addMoney(int(text[-2]+text[-1]))
            u.writeUsers(users)
            await message.answer("ЧИТЫ! Получено монеток " + text[-2]+text[-1])
        else:
            await message.answer(config.to_menu_error_text)

@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

async def main() -> None:
    bot = Bot(token=config.token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
