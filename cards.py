import random
import math
from PIL import Image, ImageDraw, ImageFilter

class Card:
    def __init__(self, index, name, ename, image, rare):
        self.index = index
        self.name = name
        self.ename = ename
        self.image = image
        self.rare = rare

class CardCascade:
    def __init__(self, cascade):
        self.cascade = cascade

    def get(self, count):
        if len(self.cascade) >= count:
            cards = []
            for i in range(count):
                cards.append(self.cascade.pop(0))
            return cards
        else:
            return False

    def createRaresList(self, rares):
        res = []
        for i in range(rares[0][0]):
            res.append(0)
        for i in range(rares[1][0]):
            res.append(1)
        for i in range(rares[2][0]):
            res.append(2)
        for i in range(rares[3][0]):
            res.append(3)
        for i in range(rares[4][0]):
            res.append(4)
        return res

    def getCard(self, rare, index, cascade):
        base = self.createCascadeBase(cascade)
        cur = 0
        while rare>0:
            rare -= 1
            cur += base[rare]
        cur += index
        return cascade[cur]

    def createCascadeBase(self, cascade):
        base = [0, 0, 0, 0, 0]
        for el in cascade:
            base[el.rare] += 1
        return base

    def reloadRares(self, rares, rare):
        rare0 = rares[0][0]
        rare1 = rares[1][0]
        rare2 = rares[2][0]
        rare3 = rares[3][0]
        rare4 = rares[4][0]
        if rare == 0:
            if rares[0][1] == 0:
                rares[0][0] = 0
                mn = 100/(sum([rare1, rare2, rare3, rare4])+1)
            else:
                rares[0][0] -= 20
                if rares[0][0] <= 0:
                    rares[0][0] = 2
                mn = (100-rares[0][0])/(sum([rare1, rare2, rare3, rare4])+1)
            rares[1][0] = math.ceil(rare1*mn)
            rares[2][0] = math.ceil(rare2*mn)
            rares[3][0] = math.ceil(rare3*mn)
            rares[4][0] = math.ceil(rare4*mn)
        elif rare == 1:
            if rares[1][1] == 0:
                rares[1][0] = 0
                if rare0 != 0:
                    mn = 100/(sum([(rare0+16), rare2, rare3, rare4])+1)
                else:
                    mn = 100/(sum([rare0, rare2, rare3, rare4])+1)
            else:
                rares[1][0] -= 16
                if rares[1][0] <= 0:
                    rares[1][0] = 1
                if rare0 != 0:
                    mn = (100-rares[1][0])/(sum([(rare0+16), rare2, rare3, rare4])+1)
                else:
                    mn = (100-rares[1][0])/(sum([rare0, rare2, rare3, rare4])+1)
                rares[0][0] = math.ceil(rare0*mn+16*int(bool(rare0)))
                rares[2][0] = math.ceil(rare2*mn)
                rares[3][0] = math.ceil(rare3*mn)
                rares[4][0] = math.ceil(rare4*mn)
        elif rare == 2:
            if rares[2][1] == 0:
                rares[2][0] = 0
                if rare0 != 0:
                    mn = 100/(sum([(rare0+16), rare1, rare3, rare4])+1)
                else:
                    mn = 100/(sum([rare0, rare1, rare3, rare4])+1)
            else:
                rares[2][0] -= 16
                if rares[2][0] <= 0:
                    rares[2][0] = 1
                if rare0 != 0:
                    mn = (100-rares[2][0])/(sum([(rare0+16), rare1, rare3, rare4])+1)
                else:
                    mn = (100-rares[2][0])/(sum([rare0, rare1, rare3, rare4])+1)
                rares[0][0] = math.ceil(rare0*mn+16*int(bool(rare0)))
                rares[1][0] = math.ceil(rare1*mn)
                rares[3][0] = math.ceil(rare3*mn)
                rares[4][0] = math.ceil(rare4*mn)
        elif rare == 3:
            if rares[3][1] == 0:
                rares[3][0] = 0
                if rare0 != 0:
                    mn = 100/(sum([(rare0+16), rare2, rare1, rare4])+1)
                else:
                    mn = 100/(sum([rare0, rare2, rare1, rare4])+1)
            else:
                rares[3][0] -= 16
                if rares[3][0] <= 0:
                    rares[3][0] = 1
                if rare0 != 0:
                    mn = (100-rares[3][0])/(sum([(rare0+16), rare2, rare1, rare4])+1)
                else:
                    mn = (100-rares[3][0])/(sum([rare0, rare2, rare1, rare4])+1)
                rares[0][0] = math.ceil(rare0*mn+16*int(bool(rare0)))
                rares[2][0] = math.ceil(rare2*mn)
                rares[1][0] = math.ceil(rare1*mn)
                rares[4][0] = math.ceil(rare4*mn)
        elif rare == 4:
            if rares[4][1] == 0:
                rares[4][0] = 0
                if rare0 != 0:
                    mn = 100/(sum([(rare0+16), rare2, rare3, rare1])+1)
                else:
                    mn = 100/(sum([rare0, rare2, rare3, rare1])+1)
            else:
                rares[4][0] -= 16
                if rares[4][0] <= 0:
                    rares[4][0] = 1
                if rare0 != 0:
                    mn = (100-rares[4][0])/(sum([(rare0+16), rare2, rare3, rare1])+1)
                else:
                    mn = (100-rares[4][0])/(sum([rare0, rare2, rare3, rare1])+1)
                rares[0][0] = math.ceil(rare0*mn+16*int(bool(rare0)))
                rares[2][0] = math.ceil(rare2*mn)
                rares[3][0] = math.ceil(rare3*mn)
                rares[1][0] = math.ceil(rare1*mn)
        return rares

    def sort(self):
        old = []
        for el in self.cascade:
            old.append(el)
        new = []
        rares = [[32, 22], [17, 14], [17, 14], [17, 14], [17, 14]]
        while len(new) < len(self.cascade):
            rare = random.choice(self.createRaresList(rares))
            count = rares[rare][1]
            if count == 0:
                continue
            card = self.getCard(rare, random.choice(range(0, count)), old)
            new.append(card)
            old.remove(card)
            rares[rare][1] -= 1
            rares = self.reloadRares(rares, rare)
            # print(card.rare, card.index, card.name, rares, len(new), len(self.cascade))
        self.cascade = new


cards = [
    Card(0, "Шут", "The Fool", "data/media/card0.jpg", 0), #                      СТАРШИЕ АРКАНЫ
    Card(1, "Маг", "The Magician", "data/media/card1.jpg", 0),
    Card(2, "Жрица", "The High Priestess", "data/media/card2.jpg", 0),
    Card(3, "Императрица", "The Empress", "data/media/card3.jpg", 0),
    Card(4, "Император", "The Emperor", "data/media/card4.jpg", 0),
    Card(5, "Верховный жрец", "The Hierophant", "data/media/card5.jpg", 0),
    Card(6, "Влюбленные", "The Lovers", "data/media/card6.jpg", 0),
    Card(7, "Колесница", "The Chariot", "data/media/card7.jpg", 0),
    Card(8, "Справедливость", "Justice", "data/media/card8.jpg", 0),
    Card(9, "Отшельник", "The Hermit", "data/media/card9.jpg", 0),
    Card(10, "Колесо фортуны", "Wheel of Fortune", "data/media/card10.jpg", 0),
    Card(11, "Сила", "Strength", "data/media/card11.jpg", 0),
    Card(12, "Повешенный", "The Hanged Man", "data/media/card12.jpg", 0),
    Card(13, "Смерть", "Death", "data/media/card13.jpg", 0),
    Card(14, "Умеренность", "Temperance", "data/media/card14.jpg", 0),
    Card(15, "Дьявол", "The Devil", "data/media/card15.jpg", 0),
    Card(16, "Башня", "The Tower", "data/media/card16.jpg", 0),
    Card(17, "Звезда", "The Star", "data/media/card17.jpg", 0),
    Card(18, "Луна", "The Moon", "data/media/card18.jpg", 0),
    Card(19, "Солнце", "The Sun", "data/media/card19.jpg", 0),
    Card(20, "Суд", "Judgement", "data/media/card20.jpg", 0),
    Card(21, "Мир", "The World", "data/media/card21.jpg", 0),
    Card(22, "Король Жезлов", "King of Wands", "data/media/card22.jpg", 1), #      ЖЕЗЛЫ
    Card(23, "Королева Жезлов", "Queen of Wands", "data/media/card23.jpg", 1),
    Card(24, "Рыцарь Жезлов", "Knight of Wands", "data/media/card24.jpg", 1),
    Card(25, "Паж Жезлов", "Page of Wands", "data/media/card25.jpg", 1),
    Card(26, "Десятка Жезлов", "Ten of Wands", "data/media/card26.jpg", 1),
    Card(27, "Девятка Жезлов", "Nine of Wands", "data/media/card27.jpg", 1),
    Card(28, "Восьмерка Жезлов", "Eight of Wands", "data/media/card28.jpg", 1),
    Card(29, "Семерка Жезлов", "Seven of Wands", "data/media/card29.jpg", 1),
    Card(30, "Шестерка Жезлов", "Six of Wands", "data/media/card30.jpg", 1),
    Card(31, "Пятерка Жезлов", "Five of Wands", "data/media/card31.jpg", 1),
    Card(32, "Четверка Жезлов", "Four of Wands", "data/media/card32.jpg", 1),
    Card(33, "Тройка Жезлов", "Three of Wands", "data/media/card33.jpg", 1),
    Card(34, "Двойка Жезлов", "Two of Wands", "data/media/card34.jpg", 1),
    Card(35, "Туз Жезлов", "Aсe of Wands", "data/media/card35.jpg", 1),
    Card(36, "Король Кубков", "King of Cups", "data/media/card36.jpg", 2), #       КУБКИ
    Card(37, "Королева Кубков", "Queen of Cups", "data/media/card37.jpg", 2),
    Card(38, "Рыцарь Кубков", "Knight of Cups", "data/media/card38.jpg", 2),
    Card(39, "Паж Кубков", "Page of Cups", "data/media/card39.jpg", 2),
    Card(40, "Десятка Кубков", "Ten of Cups", "data/media/card40.jpg", 2),
    Card(41, "Девятка Кубков", "Nine of Cups", "data/media/card41.jpg", 2),
    Card(42, "Восьмерка Кубков", "Eight of Cups", "data/media/card42.jpg", 2),
    Card(43, "Семерка Кубков", "Seven of Cups", "data/media/card43.jpg", 2),
    Card(44, "Шестерка Кубков", "Six of Cups", "data/media/card44.jpg", 2),
    Card(45, "Пятерка Кубков", "Five of Cups", "data/media/card45.jpg", 2),
    Card(46, "Четверка Кубков", "Four of Cups", "data/media/card46.jpg", 2),
    Card(47, "Тройка Кубков", "Three of Cups", "data/media/card47.jpg", 2),
    Card(48, "Двойка Кубков", "Two of Cups", "data/media/card48.jpg", 2),
    Card(49, "Туз Кубков", "Aсe of Cups", "data/media/card49.jpg", 2),
    Card(50, "Король Мечей", "King of Swords", "data/media/card50.jpg", 3), #      МЕЧИ
    Card(51, "Королева Мечей", "Queen of Swords", "data/media/card51.jpg", 3),
    Card(52, "Рыцарь Мечей", "Knight of Swords", "data/media/card52.jpg", 3),
    Card(53, "Паж Мечей", "Page of Swords", "data/media/card53.jpg", 3),
    Card(54, "Десятка Мечей", "Ten of Swords", "data/media/card54.jpg", 3),
    Card(55, "Девятка Мечей", "Nine of Swords", "data/media/card55.jpg", 3),
    Card(56, "Восьмерка Мечей", "Eight of Swords", "data/media/card56.jpg", 3),
    Card(57, "Семерка Мечей", "Seven of Swords", "data/media/card57.jpg", 3),
    Card(58, "Шестерка Мечей", "Six of Swords", "data/media/card58.jpg", 3),
    Card(59, "Пятерка Мечей", "Five of Swords", "data/media/card59.jpg", 3),
    Card(60, "Четверка Мечей", "Four of Swords", "data/media/card60.jpg", 3),
    Card(61, "Тройка Мечей", "Three of Swords", "data/media/card61.jpg", 3),
    Card(62, "Двойка Мечей", "Two of Swords", "data/media/card62.jpg", 3),
    Card(63, "Туз Мечей", "Aсe of Swords", "data/media/card63.jpg", 3),
    Card(64, "Король Пентаклей", "King of Pentacles", "data/media/card64.jpg", 4), #       ПЕНТАКЛИ
    Card(65, "Королева Пентаклей", "Queen of Pentacles", "data/media/card65.jpg", 4),
    Card(66, "Рыцарь Пентаклей", "Knight of Pentacles", "data/media/card66.jpg", 4),
    Card(67, "Паж Пентаклей", "Page of Pentacles", "data/media/card67.jpg", 4),
    Card(68, "Десятка Пентаклей", "Ten of Pentacles", "data/media/card68.jpg", 4),
    Card(69, "Девятка Пентаклей", "Nine of Pentacles", "data/media/card69.jpg", 4),
    Card(70, "Восьмерка Пентаклей", "Eight of Pentacles", "data/media/card70.jpg", 4),
    Card(71, "Семерка Пентаклей", "Seven of Pentacles", "data/media/card71.jpg", 4),
    Card(72, "Шестерка Пентаклей", "Six of Pentacles", "data/media/card72.jpg", 4),
    Card(73, "Пятерка Пентаклей", "Five of Pentacles", "data/media/card73.jpg", 4),
    Card(74, "Четверка Пентаклей", "Four of Pentacles", "data/media/card74.jpg", 4),
    Card(75, "Тройка Пентаклей", "Three of Pentacles", "data/media/card75.jpg", 4),
    Card(76, "Двойка Пентаклей", "Two of Pentacles", "data/media/card76.jpg", 4),
    Card(77, "Туз Пентаклей", "Aсe of Pentacles", "data/media/card77.jpg", 4),
]

def createNewCardCascade():
    return CardCascade(cards)

# c = CardCascade(cards)
# c.sort()
# print("Карты перемешаны")
# for el in c.cascade:
#     print(el.name)

class CardTable:
    def __init__(self, number, coords, image):
        self.number = number
        self.coords = coords
        self.image = image

    def postCards(self, cards, isSign, backImage):
        if isSign:
            back = Image.open(backImage, "r")
        else:
            back = Image.open(self.image, "r")
        if self.number == len(cards):
            for i in range(len(cards)):
                card = cards[i]
                pos = self.coords[i]
                img = Image.open(card.image, "r")
                img = img.resize((pos.width, pos.height))
                back.paste(img, pos.pos1)
                img.close()
            name = "temps/temp" + str(random.choice(range(9999))) + ".png"
            back.save(name)
            back.close()
            return name
        else:
            return "Ошибка"

    def postSign(self, sign):
        back = Image.open(self.image, "r")
        img = Image.open(sign, "r")
        maskCenterX, maskCenterY = 600, 85
        maskWidth = 150
        maskHeight = 110
        img = img.resize((maskWidth+20, maskHeight+20))
        mask_im = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse((10, 10, maskWidth, maskHeight), fill=255)
        mask_im_blur = mask_im.filter(ImageFilter.GaussianBlur(10))
        back.paste(img, (int(maskCenterX-maskWidth/2)-10, int(maskCenterY-maskHeight/2)-10), mask_im_blur)
        img.close()
        name = "temps/stemp" + str(random.choice(range(9999))) + ".png"
        back.save(name)
        back.close()
        return name


class ImageCoords:
    def __init__(self, pos1, pos2, pos3, pos4):
        self.pos1 = pos1 # ВЕРХ-ЛЕВО
        self.pos2 = pos2 # ВЕРХ-ПРАВО
        self.pos3 = pos3 # НИЗ-ЛЕВО
        self.pos4 = pos4 # НИЗ-ПРАВО
        self.width = self.pos2[0]-self.pos1[0]
        self.height = self.pos3[1]-self.pos1[1]

ct1Ipos1 = ImageCoords((1000, 620), (1400, 620), (1000, 1200), (1400, 1200))
cardTable1 = CardTable(1, [ct1Ipos1], "data/media/table1.png")

ct2Ipos1 = ImageCoords((410, 320), (590, 320), (410, 580), (590, 580))
ct2Ipos2 = ImageCoords((620, 320), (780, 320), (620, 580), (780, 580))
cardTable2 = CardTable(2, [ct2Ipos1, ct2Ipos2], "data/media/table2.png")

ct3Ipos1 = ImageCoords((390, 350), (510, 350), (390, 550), (510, 550))
ct3Ipos2 = ImageCoords((540, 350), (660, 350), (540, 550), (660, 550))
ct3Ipos3 = ImageCoords((690, 350), (810, 350), (690, 550), (810, 550))
cardTable3 = CardTable(3, [ct3Ipos1, ct3Ipos2, ct3Ipos3], "data/media/table3.png")

cardSignTable = CardTable(3, [ct3Ipos1, ct3Ipos2, ct3Ipos3], "data/media/tableSign3.png")
