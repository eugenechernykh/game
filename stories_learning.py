import random
from collections import namedtuple
from os import path
from re import search
from sys import exit

import pygame
import pymorphy2
from win32api import LoadKeyboardLayout
import configparser
import MySQLdb
from DBUtils.PooledDB import PooledDB

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
config.read('C:\\Users\echernykh.ECHERNYKH\mysql\config.ini')
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
FPS = 30
clock = pygame.time.Clock()

# The main screen
WIDTH, HEIGHT = 1600, 900
W_STEP, H_STEP = WIDTH // 40, HEIGHT // 40
start, line = 10 * W_STEP, 8 * H_STEP

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
         #         Items('банан', load_image('banana.jpg', item_scale), 'жёлтый'),
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

# Buttons
pictures = load_image('button_pictures.png')
pictures_pressed = load_image('button_pictures_isOver.png')
bt_tasks = load_image('button_tasks.png')
bt_tasks_pressed = load_image('button_tasks_isOver.png')


# Show text on a surface
def print_text(message, x, y, font_color=WHITE, font_type='Comic Sans MS',
               font_size=40, center='no'):
    if isinstance(message, int):
        message = str(message)  # converting int to str
    font_type = pygame.font.SysFont(font_type, font_size)
    if message.count('.') > 1:  # splitting several sentences
        splitted_message = message.split('.')
        splitted_message.pop()  # removing the last empty element in the list
        for i in range(len(splitted_message)):
            text = font_type.render(splitted_message[i] + '.', True,
                                    font_color)
            if center == 'yes':
                text_rect = text.get_rect(center=(x, y + i * 50))
                win.blit(text, text_rect)
            else:
                win.blit(text, (x, y + i * 50))
        return
    else:
        text = font_type.render(message, True, font_color)
        if center == 'yes':
            text_rect = text.get_rect(center=(x, y))
            win.blit(text, text_rect)
        else:
            win.blit(text, (x, y))

    return text.get_width()


# Draw text and images as one line
def drawSentence(sentence: tuple, x: int, y: int) -> None:
    for n in sentence:
        if isinstance(n, tuple):
            message, color = n
            x += print_text(message, x, y,
                            color) + W_STEP  # indent after drawing the text
        elif isinstance(n, pygame.Surface):
            surf = win.blit(n, (
                x, y - n.get_height() // 3))  # centering the surface in line
            x += surf.width + W_STEP  # indent after drawing the surface
        else:
            x += print_text(n, x, y) + W_STEP  # indent after drawing the text


# Show amount of solved tasks
def drawCount():
    drawSentence(('Привет! Ты правильно решил', (solved, RED),
                  change('задача', solved, case='accs') + '.'), 7 * W_STEP,
                 H_STEP)


# Show success rate
def drawStatistics():
    drawSentence(('Успешность:',
                  '0' if mistakes == 0 and solved == 0 else 100 * solved // (
                          solved + mistakes), '%'),
                 26 * W_STEP, HEIGHT - 4 * H_STEP)
    pygame.display.update()


# Declension for names
def change(word: str, number: int, case='nomn') -> str:
    morph = pymorphy2.MorphAnalyzer()
    return morph.parse(word)[0].inflect({case}).make_agree_with_number(number)[
        0]


# Past time for verb in accordance with gender
def verb_change(verb: str, noun: str, num: int) -> str:
    morph = pymorphy2.MorphAnalyzer()
    if num == 1:
        return morph.parse(verb)[0].inflect(
            {'past', morph.parse(noun)[0].tag.gender})[0]
    if num > 1:
        return morph.parse(verb)[0].inflect({'past', 'neut'})[0]


def congratulations():
    win.blit(bg, (0, 0))
    message = random.choice(('ВЕЛИКОЛЕПНО !!!', 'ЗДОРОВО !!!',
                             'ЗАМЕЧАТЕЛЬНО !!!', 'ОТЛИЧНО !!!', 'МОЛОДЕЦ !!!',
                             'ПРАВИЛЬНО !!!', 'УМНИЦА !!!'))
    print_text(message, WIDTH // 2, 2 * line, center='yes', font_size=90)
    pygame.display.update()
    pygame.time.delay(300)


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def draw_button(self):
        win.blit(self.image, self.rect)

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.rect.x < pos[0] < self.rect.x + self.rect.width:
            if self.rect.y < pos[1] < self.rect.y + self.rect.height:
                return True

        return False


class PicturesOld:
    def __init__(self, text_only=False):
        self.image = random.choice(images)
        self.text_only = text_only
        self.text = self.image.text
        self.picture = self.image.pic
        self.rect = self.picture.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.dict = self.image.questions
        self.question = random.choice(list(self.dict.keys()))
        while self.question == '':
            self.question = random.choice(list(self.dict.keys()))
        self.answer = self.dict[self.question]
        self.input_text = ''

    def drawQuestion(self):
        win.blit(bg, (0, 0))
        if self.text_only:
            print_text(self.text, WIDTH // 2, 2 * line, center='yes')
        else:
            win.blit(self.picture, self.rect)
        # Question box
        print_text(self.question, WIDTH // 2, 3.5 * line, center='yes')
        # Answer box
        drawSentence(('Ответ:', (self.input_text, BLUE)), start - 3 * W_STEP,
                     4 * line)
        # Mistakes box
        drawSentence(('Ошибок:', (mistakes, RED)), 26 * W_STEP, 4 * line)

    def checkAnswer(self, answer):
        if answer == self.answer:
            return True
        return


class Pictures:
    def __init__(self, text_only=False):
        image_scale = (600, 400)
        self.image_name, self.text, self.question, self.answer = self.picture_generation_from_db()
        self.text_only = text_only
        self.picture = load_image(self.image_name, image_scale)
        self.rect = self.picture.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.input_text = ''

    def drawQuestion(self):
        win.blit(bg, (0, 0))
        if self.text_only:
            print_text(self.text, WIDTH // 2, 2 * line, center='yes')
        else:
            win.blit(self.picture, self.rect)
        # Question box
        print_text(self.question, WIDTH // 2, 3.5 * line, center='yes')
        # Answer box
        drawSentence(('Ответ:', (self.input_text, BLUE)), start - 3 * W_STEP,
                     4 * line)
        # Mistakes box
        drawSentence(('Ошибок:', (mistakes, RED)), 26 * W_STEP, 4 * line)

    def checkAnswer(self, answer):
        return answer == self.answer

    def picture_generation_from_db(self):
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
        return pic, text, question, answer


class Task:

    @staticmethod
    def generate_question():
        return random.randint(1, 15)

    def __init__(self, text_only=False, items_amount=2):
#        self.question = self.generate_question()
        #        self.question = 10
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
        self.text_only = text_only
        if self.text_only:
            self.hero1 = self.heroes[0].name
            self.hero2 = self.heroes[1].name
            self.item1 = change(self.item_stuff1.name, self.count1)
            self.item2 = change(self.item_stuff2.name, self.count2)
            self.item_many1 = change(self.item_stuff1.name, 5)
            self.item_many2 = change(self.item_stuff2.name, 5)
        else:
            self.hero1 = self.heroes[0].pic
            self.hero2 = self.heroes[1].pic
            self.item1 = self.item_stuff1.pic
            self.item2 = self.item_stuff2.pic
            self.item_many1 = self.item_stuff1.pic
            self.item_many2 = self.item_stuff2.pic

        self.input_text = ''
        self.draw = True

    #        print(self.question, self.count1, self.count2, self.text_only)

    def drawCondition(self):

        # Show task's condition
        drawSentence(
            ('У', self.hero1,
             verb_change('быть', self.item_stuff1.name, self.count1),
             self.count1, self.item1, '.'), start,
            line)
        drawSentence(
            ('А у', self.hero2,
             verb_change('быть', self.item_stuff2.name, self.count2),
             self.count2,
             self.item2, '.'),
            start - W_STEP, 2 * line)
        # Answer box
        drawSentence(('Ответ:', (self.input_text, BLUE)), start - 3 * W_STEP,
                     4 * line)
        # Mistakes box
        drawSentence(('Ошибок:', (mistakes, RED)), 26 * W_STEP, 4 * line)

    def drawQuestion(self, num):
        if num == 1 and self.items_amount == 1:
            drawSentence(
                ('Сколько всего', self.item_many1, 'было ?'),
                start // 2 - W_STEP, 3 * line
            )
        elif num == 1 and self.items_amount > 1:
            drawSentence(
                ('Сколько всего', self.item_many1, 'и', self.item_many2,
                 'было ?'),
                start // 2 - W_STEP, 3 * line
            )
        elif num == 2:
            drawSentence(('Что больше', self.count1, 'или', self.count2, '?'),
                         start, 3 * line)
        elif num == 3 and self.items_amount == 1:
            drawSentence(('У кого', self.item_many1, 'больше ?'), start,
                         3 * line)
        elif num == 4 and self.items_amount == 1:
            drawSentence(('У кого', self.item_many1, 'меньше ?'), start,
                         3 * line)
        elif num == 5 and not self.text_only:
            drawSentence(
                ('Какого цвета', self.heroes[0].cover, 'у', self.hero1, '?'),
                start - W_STEP, 3 * line)
        elif num == 6:
            drawSentence(
                ('У кого', self.count1, self.item1, '?'), start,
                3 * line)
        elif num == 14:
            drawSentence(
                ('У кого', self.count2, self.item2, '?'), start,
                3 * line)
        elif num == 7:
            drawSentence(('Что меньше', self.count1, 'или', self.count2, '?'),
                         start, 3 * line)
        elif num == 8:
            drawSentence(('Сколько', self.item_many1, 'у', self.hero1, '?'),
                         start, 3 * line)
        elif num == 9:
            drawSentence(('Сколько', self.item_many2, 'у', self.hero2, '?'),
                         start, 3 * line)
        elif num == 10 and self.items_amount == 1 and self.count1 != self.count2:
            if self.count1 > self.count2:
                drawSentence(('На сколько', self.item_many1, 'у', self.hero1,
                              'было больше, чем у', self.hero2, '?'
                              ),
                             W_STEP * 3, 3 * line
                             )
            if self.count1 < self.count2:
                drawSentence(('На сколько', self.item_many2, 'у', self.hero2,
                              'было больше, чем у', self.hero1, '?'
                              ),
                             W_STEP * 3, 3 * line
                             )
        elif num == 11 and self.items_amount == 1 and self.count1 != self.count2:
            if self.count1 < self.count2:
                drawSentence(('На сколько', self.item_many1, 'у', self.hero1,
                              'было меньше, чем у', self.hero2, '?'
                              ),
                             W_STEP * 3, 3 * line
                             )
            else:
                drawSentence(('На сколько', self.item_many2, 'у', self.hero2,
                              'было меньше, чем у', self.hero1, '?'
                              ),
                             W_STEP * 3, 3 * line
                             )
        elif num == 12 and self.items_amount > 1 and self.count1 != self.count2:
            if self.count1 > self.count2:
                drawSentence(('На сколько', self.item_many1,
                              'было больше, чем',
                              self.item_many2, '?'
                              ),
                             W_STEP * 3, 3 * line
                             )
            else:
                drawSentence(('На сколько', self.item_many2,
                              'было больше, чем', self.item_many1, '?'
                              ),
                             W_STEP * 3, 3 * line
                             )
        elif num == 13 and self.items_amount > 1 and self.count1 != self.count2:
            if self.count1 < self.count2:
                drawSentence(('На сколько', self.item_many1,
                              'было меньше, чем', self.item_many2, '?'
                              ),
                             W_STEP * 3, 3 * line
                             )
            else:
                drawSentence(('На сколько', self.item_many2,
                              'было меньше, чем', self.item_many1, '?'
                              ),
                             W_STEP * 3, 3 * line
                             )
        else:
            return
        self.draw = False


    # Check the answer in accordance with the task question
    def checkAnswer(self, num, answer):
        if num == 1:  # How much together?
            return answer == str(self.count1 + self.count2)
        if num == 2:  # Which number is greater?
            return answer == str(
                self.count1 if self.count1 >= self.count2 else self.count2)
        if num == 3:  # Who has more?
            if self.count1 > self.count2:
                return answer == 'у ' + self.heroes[0].name
            elif self.count1 == self.count2:
                return answer == 'одинаково'
            else:
                return answer == 'у ' + self.heroes[1].name
        if num == 4:  # Who has current_count of item?
            if self.count1 < self.count2:
                return answer == 'у ' + self.heroes[0].name
            elif self.count1 == self.count2:
                return answer == 'одинаково'
            else:
                return answer == 'у ' + self.heroes[1].name
        if num == 5:  # Which color?
            return answer == self.heroes[0].color
        if num == 6:  # Who has? Hero[0]
            if self.count1 == self.count2 and self.items_amount == 1:
                return answer == 'одинаково'
            else:
                return answer == 'у ' + self.heroes[0].name
        if num == 14:  # Who has? Hero[1]
            if self.count1 == self.count2 and self.items_amount == 1:
                return answer == 'одинаково'
            else:
                return answer == 'у ' + self.heroes[1].name

        if num == 7:  # Which number is lower?
            return answer == str(
                self.count1 if self.count1 <= self.count2 else self.count2)
        if num == 8:  # How many items does hero1 have?
            return answer == str(self.count1)
        if num == 9:  # How many items does hero2 have?
            return answer == str(self.count2)
        if num == 10:  # How many more?
            return answer == 'на ' + str(abs(self.count1 - self.count2))
        if num == 11:  # How many less?
            return answer == 'на ' + str(abs(self.count1 - self.count2))
        if num == 12:  # How many more?
            return answer == 'на ' + str(abs(self.count1 - self.count2))
        if num == 13:  # How many less?
            return answer == 'на ' + str(abs(self.count1 - self.count2))

        return

    def drawWindow(self):
        win.blit(bg, (0, 0))
        drawCount()
        self.drawCondition()
        #        self.drawQuestion(3)
        while self.draw:
            self.question = self.generate_question()
            self.drawQuestion(self.question)
        self.drawQuestion(self.question)

        pygame.display.update()


'''
        # draw net for position calculation:
        j = 40
        for i in range(1, j):
            pygame.draw.line(win, BLACK, (i * WIDTH // j, 0), (i * WIDTH // j, HEIGHT))
            pygame.draw.line(win, BLACK, (0, i * HEIGHT // j), (WIDTH, i * HEIGHT // j))
'''


# The game menu
def title_scene():
    clock.tick(FPS)
    button_pictures = Button(WIDTH // 2, HEIGHT // 3, pictures)
    button_tasks = Button(WIDTH // 2, HEIGHT // 3 - 100, bt_tasks)

    run = True
    while run:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEMOTION:
                if button_pictures.isOver(pos):
                    button_pictures.image = pictures_pressed
                else:
                    button_pictures.image = pictures
                if button_tasks.isOver(pos):
                    button_tasks.image = bt_tasks_pressed
                else:
                    button_tasks.image = bt_tasks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_pictures.isOver(pos):
                    pictures_scene()
                if button_tasks.isOver(pos):
                    tasks_scene()

        win.blit(bg, (0, 0))
        button_pictures.draw_button()
        button_tasks.draw_button()
        pygame.display.update()


# The game for questions per picture
def pictures_scene():
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
                        if pics.text_only:
                            pics.text_only = False
                        else:
                            pics.text_only = True
                    # Processing TAB key for showing stats
                    if event.key == pygame.K_TAB:
                        tab_pressed = True
                        while tab_pressed:
                            drawStatistics()
                            for e in pygame.event.get():
                                if e.type == pygame.KEYUP and e.key == pygame.K_TAB:
                                    tab_pressed = False
                    # Checking the answer
                    elif event.key == pygame.K_RETURN:
                        answer = pics.input_text
                        pics.input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        pics.input_text = pics.input_text[:-1]
                    elif len(pics.input_text) < 20:
                        pics.input_text += event.unicode

            # Next task or mistakes calculation
            if answer != '':
                completed = pics.checkAnswer(answer)
                answer = ''
                if not completed:
                    mistakes += 1

            pics.drawQuestion()
            drawCount()
            pygame.display.update()
        solved += 1
        congratulations()


# The tasks game
def tasks_scene():
    run = True

    while run:
        global mistakes, solved

        clock.tick(FPS)
        completed = False
        #    task = Task(True)
        items_amount = random.randint(1, 2)
        task = random.choice((Task(True, items_amount), Task(items_amount)))
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
                    if event.key == pygame.K_LCTRL:
                        if task.text_only:
                            task.text_only = False
                        else:
                            task.text_only = True
                    # Processing TAB key for showing stats
                    if event.key == pygame.K_TAB:
                        tab_pressed = True
                        while tab_pressed:
                            drawStatistics()
                            for e in pygame.event.get():
                                if e.type == pygame.KEYUP and \
                                        e.key == pygame.K_TAB:
                                    tab_pressed = False
                    # Checking the answer
                    elif event.key == pygame.K_RETURN:
                        answer = task.input_text
                        task.input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        task.input_text = task.input_text[:-1]
                    elif len(task.input_text) < 20:
                        task.input_text += event.unicode
            # Next task or mistakes calculation
            if answer != '':
                completed = task.checkAnswer(task.question, answer)
                answer = ''
                if not completed:
                    mistakes += 1
            task.drawWindow()
            pygame.display.update()
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
