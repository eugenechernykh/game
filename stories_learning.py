import configparser
import random
from collections import namedtuple
from os import path
from re import search
from sys import exit

import MySQLdb
import pygame
import pymorphy2
from pymorphy2.shapes import restore_capitalization
from DBUtils.PooledDB import PooledDB
from win32api import LoadKeyboardLayout

pygame.init()
pygame.font.init()

# Set Russian as the default layout
LoadKeyboardLayout("00000419", 1)

# Directories initialisation
game_dir = path.dirname(__file__)
img_dir = path.join(game_dir, 'img')
data_dir = path.join(game_dir, 'data')

# DB config load and opening the connection
config = configparser.ConfigParser()
config.read('C:/Users/echernykh.ECHERNYKH/mysql/config.ini')
pool = PooledDB(creator=MySQLdb,
                mincached=1,
                maxcached=4,
                host=config['mysqlDB']['host'],
                user=config['mysqlDB']['user'],
                passwd=config['mysqlDB']['pass'],
                db=config['mysqlDB']['db'],
                charset='utf8')
db = pool.connection()

# FPS to decrease load
FPS = 10
clock = pygame.time.Clock()

# The main screen
WIDTH, HEIGHT = 1600, 900
W_STEP, H_STEP = WIDTH // 40, HEIGHT // 40
START, LINE = 10 * W_STEP, 8 * H_STEP

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Истории в картинках")

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 204, 255)


# Simplify image loading and resizing
def load_image(file, scale=None):
    if search(r'png', file):
        image = pygame.image.load(path.join(img_dir, file)).convert_alpha()
        if scale is not None:
            return pygame.transform.smoothscale(image, scale)
        else:
            return image
    else:
        image = pygame.image.load(path.join(img_dir, file)).convert()
        if scale is not None:
            return pygame.transform.smoothscale(image, scale)
        else:
            return image


# hero_scale = (WIDTH // 10, HEIGHT // 6 + HEIGHT // 90)
hero_scale = (120, 160)
Heroes = namedtuple("Hero", "name pic cover color")
heroes = [
    Heroes('Артёма', load_image('artem.png', hero_scale), 'кофта', 'синего'),
    Heroes('мамы', load_image('mama.png', hero_scale), 'футболка',
           'бордового'),
    Heroes('папы', load_image('papa.png', hero_scale), 'футболка', 'синего'),
    Heroes('медведя', load_image('bear.jpg', hero_scale), 'шкура',
           'коричневого'),
    Heroes('ГуммиБера', load_image('gummy.jpg', hero_scale), 'трусики',
           'оранжевого'),
    Heroes('льва', load_image('lion.jpg', hero_scale), 'грива', 'коричневого'),
    Heroes('Малыша', load_image('malysh.jpg', hero_scale), 'кофта',
           'красного'),
    Heroes('Пятачка', load_image('piglet.jpg', hero_scale), 'пятачок',
           'розового'),
    Heroes('кролика', load_image('rabbit.jpg', hero_scale), 'кофта',
           'красного'),
    Heroes('тигрёнка', load_image('tiger.jpg', hero_scale), 'полоски',
           'чёрного'),
    Heroes('черепахи', load_image('turtle.jpg', hero_scale), 'голова',
           'зелёного'),
    Heroes('Винни-Пуха', load_image('winny.png', hero_scale), 'лапа',
           'коричневого'),
    Heroes('монстра', load_image('monster.png', hero_scale), 'пузо',
           'зелёного'),
    Heroes('рыбы', load_image('fish.png', hero_scale), 'чешуя', 'зелёного'),
    Heroes('пчелы', load_image('bee.png', hero_scale), 'крылья', 'голубого'),
    Heroes('обезьяны', load_image('monkey.png', hero_scale), 'футболка',
           'жёлтого'),
    Heroes('клоуна', load_image('clown1.png', hero_scale), 'одежда',
           'зелёного'),
    Heroes('мальчика', load_image('boy2.png', hero_scale), 'шорты', 'серого'),
    Heroes('жирафа', load_image('giraffe.png', hero_scale), 'пятна',
           'коричневого'),
    Heroes('мальчика', load_image('boy.png', hero_scale), 'футболка',
           'голубого'),
    Heroes('тигра', load_image('tiger.png', hero_scale), 'шкура', 'белого'),
    Heroes('панды', load_image('panda.png', hero_scale), 'пузо', 'белого'),
    Heroes('девочки', load_image('girl_1.png', hero_scale), 'фартук',
           'красного'),
    Heroes('девочки', load_image('girl.png', hero_scale), 'платье', 'синего'),
    Heroes('дракона', load_image('dragon.png', hero_scale), 'пятка',
           'жёлтого'),
    Heroes('утки', load_image('duck2.png', hero_scale), 'перья', 'белого'),
    Heroes('утки', load_image('duck.png', hero_scale), 'перья', 'жёлтого'),
    Heroes('обезьяны', load_image('monkey2.png', hero_scale), 'шкура',
           'коричневого'),
    Heroes('волка', load_image('wolf.jpg', hero_scale), 'шарф', 'красного')]

item_scale = (120, 120)
Items = namedtuple("Item", "name pic color")
items = [Items('яблоко', load_image('apple.jpg', item_scale), 'жёлтое'),
         Items('банан', load_image('banana2.png', item_scale), 'жёлтый'),
         Items('клубника', load_image('strawberry.png', item_scale),
               'красного  '),
         Items('мяч', load_image('ball.jpg', item_scale), 'белый'),
         Items('шар', load_image('balloon.jpg', item_scale), 'красный'),
         Items('книга', load_image('book.png', item_scale), 'зелёная'),
         Items('торт', load_image('cake.jpg', item_scale), 'оранжевый'),
         Items('конфета', load_image('candy.jpg', item_scale), 'красная'),
         Items('карандаш', load_image('pen.jpg', item_scale), 'жёлтый'),
         Items('груша', load_image('pear.png', item_scale), 'жёлтый'),
         Items('помидор', load_image('tomato.png', item_scale), 'жёлтый'),
         Items('апельсин', load_image('orange.png', item_scale), 'жёлтый'),
         Items('машина', load_image('car.jpg', item_scale), 'жёлтая')]

Images = namedtuple("Images", "pic text questions")


def load_files(text_file_name, scale):
    my_images = []
    with open(path.join(data_dir, text_file_name), 'r',
              encoding='utf8') as inFile:
        for line in inFile:
            my_list = list(line.strip().split(','))
            if line == '\n':
                continue
            pic, text, que = my_list[0], my_list[1], my_list[2:]
            questions = {}
            for i in range(len(que)):
                if i % 2 == 1:
                    questions[que[i - 1]] = que[i]
            my_images.append(Images(load_image(pic, scale), text, questions))

    return my_images


# Load images list with other data from csv file
# images = load_files('images_1.csv', image_scale)


# Background
bg = load_image('board1.jpg', (WIDTH, HEIGHT))


def print_text(
        message, x, y, font_color=WHITE, font_type='Comic Sans MS',
        font_size=40, center='no'):
    if isinstance(message, int):
        message = str(message)  # converting number to string
    font_type = pygame.font.SysFont(font_type, font_size)
    # splitting several sentences is required for picture descriptions
    if message.count('.') > 1:
        splitted_message = message.split('.')
        splitted_message.pop()  # removing the last empty element in the list
        for i in range(len(splitted_message)):
            text = font_type.render(splitted_message[i] + '.', True,
                                    font_color)
            if center == 'yes':
                text_rect = text.get_rect(center=(x, y + i*50))
                win.blit(text, text_rect)
            else:
                win.blit(text, (x, y + i*50))
        return
    else:
        text = font_type.render(message, True, font_color)
        if center == 'yes':
            text_rect = text.get_rect(center=(x, y))
            win.blit(text, text_rect)
        else:
            win.blit(text, (x, y))


def drawSentence(sentence: tuple, x: int, y: int, center: str = 'yes') -> None:
    # Draw text and images as one line
    x_position = 0
    surface_list = []
    font_type = pygame.font.SysFont('Comic Sans MS', 40)
    max_height = 0

    for n in sentence:
        if isinstance(n, tuple):
            message, color = n
            colored_text_surf = font_type.render(str(message), True, color)
            x_position += colored_text_surf.get_width() + W_STEP  # indent after drawing the text
            surface_list.append(colored_text_surf)
            if colored_text_surf.get_height() > max_height:
                max_height = colored_text_surf.get_height()
        elif isinstance(n, pygame.Surface):
#            surf = win.blit(n, (
#                x, y - n.get_height() // 3))  # centering the surface in line
            x_position += n.get_width() + W_STEP  # indent after drawing the surface
            surface_list.append(n)
            if n.get_height() > max_height:
                max_height = n.get_height()
        else:
            text_surf = font_type.render(str(n), True, WHITE)
            x_position += text_surf.get_width() + W_STEP  # indent after drawing the text
            surface_list.append(text_surf)
            if text_surf.get_height() > max_height:
                max_height = text_surf.get_height()

    united_surface = pygame.Surface((x_position - W_STEP, max_height), pygame.SRCALPHA)
    current_x = 0

    for surf in surface_list:
        united_surface.blit(surf, (current_x, 0))
        current_x += surf.get_width() + W_STEP

    if center == 'no':
        win.blit(united_surface, (x, y))
    if center == 'yes':
        win.blit(united_surface, ((WIDTH - united_surface.get_width())//2, y))
    if center == '1half':
        win.blit(united_surface, ((WIDTH - 2*united_surface.get_width())//4, y))
    if center == '2half':
        win.blit(united_surface, ((3*WIDTH - united_surface.get_width())//4, y))






def drawSolvedBox():
    drawSentence(('Привет! Ты правильно решил', (solved, RED),
                  agree_noun_with_number('задача', solved, case='accs') + '.'), 7 * W_STEP,
                 H_STEP)


def drawMistakesBox():
    drawSentence(('Ошибок:', (mistakes, RED)), 26 * W_STEP, 4 * LINE, center='2half')


def drawStatistics():
    # Show success rate
    drawSentence(('Успешность:',
                  '0' if mistakes == 0 and solved == 0 else 100 * solved // (
                          solved + mistakes), '%'),
                 26 * W_STEP, HEIGHT - 4*H_STEP, center='no')
    pygame.display.update()


def drawAnswerBox(input_text):
    drawSentence(('Ответ:', (input_text, BLUE)), START - 3*W_STEP,
                 4 * LINE, center='no')


def agree_noun_with_number(word: str, number: int, case='nomn') -> str:
    # Declension for names
    morph = pymorphy2.MorphAnalyzer()
    return morph.parse(word)[0].inflect({case}).make_agree_with_number(number)[
        0]


def noun_declension(noun, case='nomn'):
    morph = pymorphy2.MorphAnalyzer()
    return restore_capitalization( morph.parse(noun)[0].inflect({case})[0], noun)


def verb_change(verb: str, noun: str = 'он', count: int = 1, plural: bool = False) -> str:
    # Past time for verb in accordance with a noun gender or plural
    morph = pymorphy2.MorphAnalyzer()
    if plural:
        return morph.parse(verb)[0].inflect({'past', 'plur'})[0]
    if count == 1:
        return morph.parse(verb)[0].inflect(
            {'past', morph.parse(noun)[0].tag.gender})[0]
    if count > 1:
        return morph.parse(verb)[0].inflect({'past', 'neut'})[0]




def congratulations():
    win.blit(bg, (0, 0))
    message = random.choice(('ВЕЛИКОЛЕПНО !!!', 'ЗДОРОВО !!!',
                             'ЗАМЕЧАТЕЛЬНО !!!', 'ОТЛИЧНО !!!', 'МОЛОДЕЦ !!!',
                             'ПРАВИЛЬНО !!!', 'УМНИЦА !!!'))
    print_text(message, WIDTH // 2, 2 * LINE, center='yes', font_size=90)
    pygame.display.update()
    pygame.time.delay(300)


class Button:
    def __init__(self, x, y, image, pressed):
        self.image = image
        self.original = image
        self.pressed = pressed
        self.rect = self.image.get_rect(center=(x, y))

    def isOver(self, mouse_position: tuple) -> bool:
        # mouse_position is a tuple of (x,y) coordinates
        return self.rect.x < mouse_position[0] < self.rect.x + self.rect.width \
               and self.rect.y < mouse_position[
                   1] < self.rect.y + self.rect.height

    def changeOnOver(self, pos):
        # Changing the button image once the mouse is over it
        self.image = self.pressed if self.isOver(pos) else self.original

    def drawButton(self):
        win.blit(self.image, self.rect)


class Pictures:
    @staticmethod
    def picture_generation_from_db():
        # Generating the picture related data
        pics_id, pic, text, question, answer = 0, '', '', '', ''
        cursor = db.cursor()
        while pic == '' or text == '' or question == '' or answer == '':
            try:
                cursor.execute(
                    "SELECT pics_id, name, description from pictures ORDER BY RAND() LIMIT 1")
                pics_id, pic, text = cursor.fetchone()
                cursor.execute(
                    "SELECT question, answer from questions WHERE pics_id = %s",
                    (pics_id,))
                question, answer = random.choice(cursor.fetchall())
            except MySQLdb.OperationalError:
                print('It looks like we can\'t connect to DB')
            except Exception:
                print(
                    'can\'t get data from database with pics_id {} and name{}'.format(
                        pics_id, pic))
                continue
        cursor.close()
        return pic, text, question, answer

    def __init__(self, text_only=False):
        __image_scale = (600, 400)
        self.image_name, self.text, self.question, self.answer \
            = self.picture_generation_from_db()
        self.text_only = text_only
        self.picture = load_image(self.image_name, __image_scale)
        self.rect = self.picture.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.input_text = ''

    def checkAnswer(self, answer):
        return answer == self.answer

    def drawCondition(self):
        if self.text_only:
            print_text(self.text, WIDTH // 2, 2 * LINE, center='yes')
        else:
            win.blit(self.picture, self.rect)

    def drawQuestion(self):
        print_text(self.question, WIDTH // 2, 3.5 * LINE, center='yes')

    def drawWindow(self):
        win.blit(bg, (0, 0))

        drawSolvedBox()
        drawMistakesBox()
        drawAnswerBox(self.input_text)
        self.drawCondition()
        self.drawQuestion()

        pygame.display.update()


class Task:
    @staticmethod
    def generate_question_id():
        return random.randint(1, 15)

    def __init__(self, text_only=False, items_amount=2):
        self.heroes = random.sample(heroes, 2)
        self.count1, self.count2 = random.randint(1, 15), random.randint(1, 15)
        self.current_count = random.choice((self.count1, self.count2))
        self.items = random.sample(items, 2)
        self.items_amount = items_amount
        if self.items_amount == 1:
            self.item_stuff1 = self.items[0]
            self.item_stuff2 = self.items[0]
        else:
            self.item_stuff1 = self.items[0]
            self.item_stuff2 = self.items[1]
#        self.text_only = True
        self.text_only = text_only
        if self.text_only:
            self.hero1 = self.heroes[0].name
            self.hero2 = self.heroes[1].name
            self.item1 = agree_noun_with_number(self.item_stuff1.name, self.count1)
            self.item2 = agree_noun_with_number(self.item_stuff2.name, self.count2)
            self.item_many1 = agree_noun_with_number(self.item_stuff1.name, 5)
            self.item_many2 = agree_noun_with_number(self.item_stuff2.name, 5)
        else:
            self.hero1 = self.heroes[0].pic
            self.hero2 = self.heroes[1].pic
            self.item1 = self.item_stuff1.pic
            self.item2 = self.item_stuff2.pic
            self.item_many1 = self.item_stuff1.pic
            self.item_many2 = self.item_stuff2.pic
        self.question, self.answer = self.generateQuestionAnswer()

        self.input_text = ''
        self.draw = True

    #        print(self.question, self.count1, self.count2, self.text_only)
    def generateCondition(self):
        condition_line1 = (
            ('У', self.hero1,
             verb_change('быть', self.item_stuff1.name, self.count1),
             self.count1, self.item1, '.'), START,
            LINE)
        condition_line2 = (
            ('А у', self.hero2,
             verb_change('быть', self.item_stuff2.name, self.count2),
             self.count2,
             self.item2, '.'),
            START - W_STEP, 2 * LINE)
        return condition_line1, condition_line2

    def drawCondition(self, args):
        for arg in args:
            drawSentence(*arg)

    def two_items_not_equal_amount(self):
        return self.items_amount > 1 and self.count1 != self.count2

    def one_item_not_equal_amount(self):
        return self.items_amount == 1 and self.count1 != self.count2

    def generateQuestionAnswer(self):
        question, answer = (), ''
        while question == ():
            num = self.generate_question_id()
            if num == 1 and self.items_amount == 1:
                question = (('Сколько всего', self.item_many1, 'было ?'),
                            START // 2 - W_STEP, 3 * LINE)
                answer = str(self.count1 + self.count2)
            if num == 1 and self.two_items_not_equal_amount():
                question = (('Сколько всего', self.item_many1, 'и',
                             self.item_many2, 'было ?'), START // 2 - W_STEP,
                            3 * LINE)
                answer = str(self.count1 + self.count2)
            if num == 2:
                question = (
                    ('Что больше', self.count1, 'или', self.count2, '?'), START,
                    3 * LINE)
                answer = str(
                    self.count1 if self.count1 >= self.count2 else self.count2)
            if num == 3 and self.one_item_not_equal_amount():
                question = (
                    ('У кого', self.item_many1, 'больше ?'), START, 3 * LINE)
                answer = 'у ' + self.heroes[
                    0].name if self.count1 > self.count2 else 'у ' + \
                                                              self.heroes[
                                                                  1].name
            if num == 4 and self.one_item_not_equal_amount():
                question = (('У кого', self.item_many1, 'меньше ?'), START,
                            3 * LINE)
                answer = 'у ' + self.heroes[
                    0].name if self.count1 < self.count2 else 'у ' + \
                                                              self.heroes[
                                                                  1].name
            if num == 5 and not self.text_only:
                question = (
                    ('Какого цвета', self.heroes[0].cover, 'у', self.hero1, '?'),
                    START - W_STEP, 3 * LINE)
                answer = self.heroes[0].color
            if num == 6:
                question = (
                    ('У кого', self.count1, self.item1, '?'), START, 3 * LINE)
                if self.count1 == self.count2 and self.items_amount == 1:
                    answer = 'одинаково'
                else:
                    answer = 'у ' + self.heroes[0].name
            if num == 7:
                question = (
                    ('У кого', self.count2, self.item2, '?'), START, 3 * LINE)
                if self.count1 == self.count2 and self.items_amount == 1:
                    answer = 'одинаково'
                else:
                    answer = 'у ' + self.heroes[1].name
            if num == 8:
                question = (
                    ('Что меньше', self.count1, 'или', self.count2, '?'),
                    START, 3 * LINE)
                answer = str(
                    self.count1 if self.count1 <= self.count2 else self.count2)
            if num == 9:
                question = (('Сколько', self.item_many1, 'у', self.hero1, '?'),
                            START, 3 * LINE)
                answer = str(self.count1)
            if num == 10:
                question = (('Сколько', self.item_many2, 'у', self.hero2, '?'),
                            START, 3 * LINE)
                answer = str(self.count2)
            if num == 11 and self.one_item_not_equal_amount():
                if self.count1 > self.count2:
                    question = (
                        ('На сколько', self.item_many1, 'у', self.hero1,
                     'было больше, чем у', self.hero2, '?'
                     ),
                        3 * W_STEP, 3 * LINE
                    )
                else:
                    question = (
                        ('На сколько', self.item_many2, 'у', self.hero2,
                     'было больше, чем у', self.hero1, '?'
                     ),
                        3 * W_STEP, 3 * LINE
                    )
                answer = 'на ' + str(abs(self.count1 - self.count2))
            if num == 12 and self.one_item_not_equal_amount():
                if self.count1 < self.count2:
                    question = (
                        ('На сколько', self.item_many1, 'у', self.hero1,
                     'было меньше, чем у', self.hero2, '?'
                     ),
                        3 * W_STEP, 3 * LINE
                    )
                else:
                    question = (
                        ('На сколько', self.item_many2, 'у', self.hero2,
                     'было меньше, чем у', self.hero1, '?'
                     ),
                        3 * W_STEP, 3 * LINE
                    )
                answer = 'на ' + str(abs(self.count1 - self.count2))
            if num == 13 and self.two_items_not_equal_amount():
                if self.count1 > self.count2:
                    question = (('На сколько', self.item_many1,
                                 'было больше, чем',
                                 self.item_many2, '?'
                                 ),
                                3 * W_STEP, 3 * LINE
                                )
                else:
                    question = (('На сколько', self.item_many2,
                                 'было больше, чем', self.item_many1, '?'
                                 ),
                                3 * W_STEP, 3 * LINE
                                )
                answer = 'на ' + str(abs(self.count1 - self.count2))
            if num == 14 and self.two_items_not_equal_amount():
                if self.count1 < self.count2:
                    question = (('На сколько', self.item_many1,
                                 'было меньше, чем', self.item_many2, '?'
                                 ),
                                3 * W_STEP, 3 * LINE
                                )
                else:
                    question = (('На сколько', self.item_many2,
                                 'было меньше, чем', self.item_many1, '?'
                                 ),
                                3 * W_STEP, 3 * LINE
                                )
                answer = 'на ' + str(abs(self.count1 - self.count2))
        return question, answer

    def drawQuestion(self):
        drawSentence(*self.question)

    def checkAnswer(self, answer):
        return answer == self.answer

    def drawWindow(self):
        win.blit(bg, (0, 0))

        drawSolvedBox()
        drawMistakesBox()
        drawAnswerBox(self.input_text)
        self.drawCondition(self.generateCondition())
        self.drawQuestion()

        pygame.display.update()


class ActionTask(Task):
    ACTIONS = ('присесть', 'подпрыгнуть', 'умыться', 'улыбнуться', 'зевнуть',
               'поесть', 'подтянуться', 'прибраться', 'пробежать', 'попить',
               'поплакать', 'кричать', 'посмеяться', 'погулять', 'постучать'
               )

    @staticmethod
    def generate_actions():
        return random.sample(ActionTask.ACTIONS, 2)

    def __init__(self, text_only=True, items_amount=2, action=True):
        self.action_mode = action
        self.action = self.generate_actions()
        self.items_amount = items_amount
        print(self.action)
        if self.items_amount == 1:
            self.action1 = self.action[0]
            self.action2 = self.action[0]
        else:
            self.action1 = self.action[0]
            self.action2 = self.action[1]
        print(self.action1, self.action2)
        super().__init__(text_only, items_amount)
        self.heroes = random.sample(heroes, 2)
        if self.items_amount == 1:
            self.hero1 = noun_declension(self.heroes[0].name)
            self.hero2 = self.hero1
        else:
            self.hero1 = noun_declension(self.heroes[0].name)
            self.hero2 = noun_declension(self.heroes[1].name)
        print(self.hero1, self.hero2)
        self.question, self.answer = self.generateQuestionAnswer()

    def generateCondition(self):
        if self.hero1 != self.hero2:
            condition_line1 = (' '.join(('Однажды', self.hero1, verb_change(self.action1, self.hero1), str(self.count1), agree_noun_with_number('раз', self.count1) + '.')), WIDTH // 2, LINE)
            condition_line2 = (' '.join(('А', self.hero2, verb_change(self.action2, self.hero2), str(self.count2), agree_noun_with_number('раз', self.count2) + '.')), WIDTH // 2, 2 * LINE)
        else:
            condition_line1 = (' '.join(('Сначала', self.hero1, verb_change(self.action1, self.hero1), str(self.count1), agree_noun_with_number('раз', self.count1) + '.')), WIDTH // 2, LINE)
            condition_line2 = (' '.join(('Потом', self.hero2, verb_change(self.action2, self.hero2), str(self.count2), agree_noun_with_number('раз', self.count2) + '.')), WIDTH // 2, 2 * LINE)
        return condition_line1, condition_line2

    def drawCondition(self, args):
        for arg in args:
            print_text(*arg, center='yes')

    def drawQuestion(self):
        print_text(*self.question, center='yes')

    def same_action_different_hero_count(self):
        return self.action1 == self.action2 and self.hero1 != self.hero2 and self.count1 != self.count2

    def generateQuestionAnswer(self):
        question, answer = (), ''
        while question == ():
#            num = self.generate_question_id()
            num = random.randint(1, 7)
#            num = 7
#            self.action1 = self.action2

            if num == 1:
                message = ' '.join(('Сколько всего раз', self.hero1,
                             verb_change(self.action1, self.hero1) + '?'))
                question = (message, WIDTH//2, 3 * LINE)
                if self.hero1 == self.hero2 and self.action1 == self.action2:
                    answer = str(self.count1 + self.count2)
                else:
                    answer = str(self.count1)
            if num == 2 and self.same_action_different_hero_count():
                message = ' '.join(('Кто больше раз', verb_change(self.action1), '?'))
                question = (message, WIDTH//2, 3 * LINE)
                answer = self.hero1 if self.count1 > self.count2 else self.hero2
            if num == 3 and self.action1 != self.action2:
                message = ' '.join(('Кто', verb_change(self.action1) + '?'))
                question = (message, WIDTH // 2, 3 * LINE)
                answer = self.hero1
            if num == 4 and self.action1 != self.action2:
                message = ' '.join(('Кто', verb_change(self.action2) + '?'))
                question = (message, WIDTH // 2, 3 * LINE)
                answer = self.hero2
            if num == 5 and self.action1 == self.action2 and self.hero1 != self.hero2:
                message = ' '.join(('Сколько всего раз', self.hero1, 'и', self.hero2, verb_change(self.action1, plural=True) + '?'))
                question = (message, WIDTH // 2, 3 * LINE)
                answer = str(self.count1 + self.count2)
            if num == 6 and self.same_action_different_hero_count():
                message = ' '.join(('Кто', verb_change(self.action1),  str(self.count1), 'раз?'))
                question = (message, WIDTH // 2, 3 * LINE)
                answer = self.hero1
            if num == 7 and self.same_action_different_hero_count():
                message = ' '.join(('Кто', verb_change(self.action2),  str(self.count2), 'раз?'))
                question = (message, WIDTH // 2, 3 * LINE)
                answer = self.hero2
        return question, answer


'''
        # draw net for position calculation:
        j = 40
        for i in range(1, j):
            pygame.draw.line(win, BLACK, (i * WIDTH // j, 0), (i * WIDTH // j, HEIGHT))
            pygame.draw.line(win, BLACK, (0, i * HEIGHT // j), (WIDTH, i * HEIGHT // j))
'''

# Buttons
bt_pictures = load_image('button_pictures.png')
bt_pictures_pressed = load_image('button_pictures_isOver.png')
bt_tasks = load_image('button_tasks.png')
bt_tasks_pressed = load_image('button_tasks_isOver.png')



def title_scene():
    # The game menu
    clock.tick(FPS)

    button_pictures = Button(WIDTH // 2, HEIGHT // 3, bt_pictures,
                             bt_pictures_pressed)
    button_tasks = Button(WIDTH // 2, HEIGHT//3 - 100, bt_tasks,
                          bt_tasks_pressed)

    run = True
    while run:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEMOTION:
                button_pictures.changeOnOver(pos)
                button_tasks.changeOnOver(pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_pictures.isOver(pos):
                    pictures_scene()
                    # Let's change the button color back to the original one
                    # on return coz I like it
                    button_pictures.image = button_pictures.original
                if button_tasks.isOver(pos):
                    tasks_scene()
                    button_tasks.image = button_tasks.original

        win.blit(bg, (0, 0))
        button_pictures.drawButton()
        button_tasks.drawButton()
        pygame.display.update()


def pictures_scene():
    # The game for questions per picture
    run = True

    while run:
        global mistakes, solved
        pics = random.choice((Pictures(), Pictures(True)))
        completed = False
        answer = ''

        while not completed:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    # Left Ctrl to switch between text and pics mode
                    if event.key == pygame.K_LCTRL:
                        pics.text_only = False if pics.text_only else True
                    # Processing TAB key for showing stats
                    if event.key == pygame.K_TAB:
                        tab_pressed = True
                        while tab_pressed:
                            drawStatistics()
                            for e in pygame.event.get():
                                if e.type == pygame.KEYUP and e.key == pygame.K_TAB:
                                    tab_pressed = False
                    # Filling the answer once Enter is pressed
                    elif event.key == pygame.K_RETURN:
                        answer = pics.input_text
                        pics.input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        pics.input_text = pics.input_text[:-1]
                    # Don't expect answer more than 20 symbols
                    elif len(pics.input_text) <= 20:
                        pics.input_text += event.unicode

            # Next task or mistakes calculation
            if answer != '':
                completed = pics.checkAnswer(answer)
                answer = ''
                if not completed:
                    mistakes += 1

            pics.drawWindow()
        solved += 1
        congratulations()



def tasks_scene():
    # The tasks game
    run = True

    while run:
        global mistakes, solved

        clock.tick(FPS)
        completed = False
        #    task = Task(True)
        items_amount = random.randint(1, 2)
        task = random.choice(
            (Task(True, items_amount), Task(False, items_amount), ActionTask()))
#        task = ActionTask()
        answer = ''

        while not completed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    # Left Ctrl to switch between text and pics mode
                    #                    if event.key == pygame.K_LCTRL:
                    #                        task.text_only = False if task.text_only else True
                    # Processing TAB key for showing stats
                    if event.key == pygame.K_TAB:
                        tab_pressed = True
                        while tab_pressed:
                            drawStatistics()
                            for e in pygame.event.get():
                                if e.type == pygame.KEYUP and \
                                        e.key == pygame.K_TAB:
                                    tab_pressed = False
                    # Filling the answer once Enter is pressed
                    elif event.key == pygame.K_RETURN:
                        answer = task.input_text
                        task.input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        task.input_text = task.input_text[:-1]
                    # Don't expect answer more than 20 symbols
                    elif len(task.input_text) <= 20:
                        task.input_text += event.unicode

            # Next task or mistakes calculation
            if answer != '':
                completed = task.checkAnswer(answer)
                answer = ''
                if not completed:
                    mistakes += 1

            task.drawWindow()
        solved += 1
        congratulations()


# Finally the game starts here
solved = 0
mistakes = 0
game = True

while game:
    title_scene()
#    tasks_scene()
#    pictures_scene()

pygame.quit()
db.close()
exit()
