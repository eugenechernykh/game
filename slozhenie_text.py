import random
from collections import namedtuple
from os import path
from re import search
from sys import exit

import pygame
import pymorphy2
from win32api import LoadKeyboardLayout

pygame.init()
pygame.font.init()

# set russian as default layout
LoadKeyboardLayout("00000419", 1)

# directories initialisation
game_dir = path.dirname(__file__)
img_dir = path.join(game_dir, 'img')

# FPS to decrease load
FPS = 30
clock = pygame.time.Clock()

# main_screen
WIDTH = 1200
HEIGHT = 900
W_STEP = WIDTH // 40
H_STEP = HEIGHT // 40
start = 10 * W_STEP
line = 8 * H_STEP

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Сложение")

# set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 204, 255)

# images
bg = pygame.image.load(path.join(img_dir, 'board1.jpg')).convert()
bg = pygame.transform.smoothscale(bg, (WIDTH, HEIGHT))


# Simplify image loading and resizing
def load_hero(file):
    if search(r'png', file):
        image = pygame.image.load(path.join(img_dir, file)).convert_alpha()
        return pygame.transform.smoothscale(image, (WIDTH // 10, HEIGHT // 6 + HEIGHT // 90))
    else:
        image = pygame.image.load(path.join(img_dir, file)).convert()
        return pygame.transform.smoothscale(image, (WIDTH // 10, HEIGHT // 6 + HEIGHT // 90))


Heroes = namedtuple("Hero", "name pic cover color")
heroes = [Heroes('Артёма', load_hero('artem.png'), 'кофта', 'синего'),
          Heroes('мамы', load_hero('mama.png'), 'футболка', 'бордового'),
          Heroes('папы', load_hero('papa.png'), 'футболка', 'синего'),
          Heroes('медведя', load_hero('bear.jpg'), 'шкура', 'коричневого'),
          Heroes('ГуммиБера', load_hero('gummy.jpg'), 'трусики', 'оранжевого'),
          Heroes('льва', load_hero('lion.jpg'), 'грива', 'коричневого'),
          Heroes('Малыша', load_hero('malysh.jpg'), 'кофта', 'красного'),
          Heroes('Пятачка', load_hero('piglet.jpg'), 'пятачок', 'розового'),
          Heroes('кролика', load_hero('rabbit.jpg'), 'кофта', 'красного'),
          Heroes('тигрёнка', load_hero('tiger.jpg'), 'полоски', 'чёрного'),
          Heroes('черепахи', load_hero('turtle.jpg'), 'голова', 'зелёного'),
          Heroes('Винни-Пуха', load_hero('winny.png'), 'лапа', 'коричневого'),
          Heroes('монстра', load_hero('monster.png'), 'пузо', 'зелёного'),
          Heroes('волка', load_hero('kitty.jpg'), 'шарф', 'красного')]


def load_item(file):
    if search(r'png', file):
        image = pygame.image.load(path.join(img_dir, file)).convert_alpha()
        return pygame.transform.smoothscale(image, (WIDTH // 10, WIDTH // 10))
    else:
        image = pygame.image.load(path.join(img_dir, file)).convert()
        return pygame.transform.smoothscale(image, (WIDTH // 10, WIDTH // 10))


Items = namedtuple("Item", "name pic color")
items = [Items('яблоко', load_item('apple.jpg'), 'жёлтое'),
         Items('банан', load_item('banana.jpg'), 'жёлтый'),
         Items('мяч', load_item('ball.jpg'), 'белый'),
         Items('шар', load_item('balloon.jpg'), 'красный'),
         Items('книга', load_item('book.png'), 'зелёная'),
         Items('торт', load_item('cake.jpg'), 'оранжевый'),
         Items('конфета', load_item('candy.jpg'), 'красная'),
         Items('карандаш', load_item('pen.jpg'), 'жёлтый'),
         Items('машина', load_item('car.jpg'), 'жёлтая')]


# Show text on a surface
def print_text(message, x, y, font_color=WHITE, font_type='Comic Sans MS', font_size=40):
    if isinstance(message, int):
        message = str(message)  # converting int in str
    font_type = pygame.font.SysFont(font_type, font_size)
    text = font_type.render(message, True, font_color)
    win.blit(text, (x, y))
    return text.get_width()


# Draw text and images as one line
def drawSentence(sentence: tuple, x: int, y: int) -> None:
    for n in sentence:
        if isinstance(n, tuple):
            message, color = n
            x += print_text(message, x, y, color) + W_STEP  # indent after drawing the text
        elif isinstance(n, pygame.Surface):
            surf = win.blit(n, (x, y - n.get_height() // 3))  # centering the surface in line
            x += surf.width + W_STEP  # indent after drawing the surface
        else:
            x += print_text(n, x, y) + W_STEP  # indent after drawing the text


# Show amount of solved tasks
def drawCount():
    drawSentence(('Привет! Ты правильно решил', (solved, RED),
                  'задач{}.'.format('у' if solved == 1 else ('и' if 1 < solved < 5 else ''))), 7 * W_STEP, H_STEP)


# Show success rate
def drawStatistics():
    drawSentence(('Успешность:', '0' if mistakes == 0 and solved == 0 else 100 * solved // (solved + mistakes), '%'),
                 26 * W_STEP, HEIGHT - 4 * H_STEP)


# Declension for names
def change(word: str, number: int) -> str:
    morph = pymorphy2.MorphAnalyzer()
    return morph.parse(word)[0].make_agree_with_number(number)[0]


# Past time for verb in accordance with gender
def verb_change(verb: str, noun: str, num: int) -> str:
    morph = pymorphy2.MorphAnalyzer()
    if num == 1:
        return morph.parse(verb)[0].inflect({'past', morph.parse(noun)[0].tag.gender})[0]
    if num > 1:
        return morph.parse(verb)[0].inflect({'past', 'neut'})[0]


class Task:

    def __init__(self, text_only=False):
        self.question = random.randint(1, 7)
        self.heroes = random.sample(heroes, 2)
        self.count1 = random.randint(1, 15)
        self.count2 = random.randint(1, 15)
        self.current_count = random.choice((self.count1, self.count2))
        self.item = random.choice(items)
        self.input_text = ''
        self.text_only = text_only
        if self.text_only:
            self.hero1 = self.heroes[0].name
            self.hero2 = self.heroes[1].name
            self.item1 = change(self.item.name, self.count1)
            self.item2 = change(self.item.name, self.count2)
            self.item_many = change(self.item.name, 5)
            self.item_current = change(self.item.name, self.current_count)
        else:
            self.hero1 = self.heroes[0].pic
            self.hero2 = self.heroes[1].pic
            self.item1 = self.item.pic
            self.item2 = self.item.pic
            self.item_many = self.item.pic
            self.item_current = self.item.pic

    def drawCondition(self):
        # show task's condition
        drawSentence(
            ('У', self.hero1, verb_change('быть', self.item.name, self.count1), self.count1, self.item1, '.'), start,
            line)
        drawSentence(
            ('А у', self.hero2, verb_change('быть', self.item.name, self.count2), self.count2, self.item2, '.'),
            start - W_STEP, 2 * line)
        # answer box
        drawSentence(('Ответ:', (self.input_text, BLUE)), start - 3 * W_STEP, 4 * line)
        # mistakes box
        drawSentence(('Ошибок:', (mistakes, RED)), 26 * W_STEP, 4 * line)

    def drawQuestion(self, num):
        if num == 1:
            drawSentence(('Сколько всего', self.item_many, 'у', self.hero1, 'и', self.hero2, '?'), start // 2 - W_STEP,
                         3 * line)
        if num == 2:
            drawSentence(('Что больше', self.count1, 'или', self.count2, '?'), start, 3 * line)
        if num == 3:
            drawSentence(('У кого', self.item_many, 'больше ?'), start, 3 * line)
        if num == 4:
            drawSentence(('У кого', self.item_many, 'меньше ?'), start, 3 * line)
        if num == 5:
            drawSentence(('Какого цвета', self.heroes[0].cover, 'у', self.hero1, '?'), start - W_STEP, 3 * line)
        if num == 6:
            drawSentence(('У кого', self.current_count, self.item_current, '?'), start, 3 * line)
        if num == 7:
            drawSentence(('Что меньше', self.count1, 'или', self.count2, '?'), start, 3 * line)

    # check the answer in accordance with the task question
    def checkAnswer(self, num, answer):
        if num == 1:  # how much together?
            return answer == str(self.count1 + self.count2)
        if num == 2:  # which number is greater?
            return answer == str(self.count1 if self.count1 >= self.count2 else self.count2)
        if num == 3:  # who has more?
            if self.count1 > self.count2:
                return answer == 'у ' + self.heroes[0].name
            elif self.count1 == self.count2:
                return answer == 'одинаково'
            else:
                return answer == 'у ' + self.heroes[1].name
        if num == 4:  # who has current_count of item?
            if self.count1 < self.count2:
                return answer == 'у ' + self.heroes[0].name
            elif self.count1 == self.count2:
                return answer == 'одинаково'
            else:
                return answer == 'у ' + self.heroes[1].name
        if num == 5:  # which color?
            return answer == self.heroes[0].color
        if num == 6:  # who has less?
            if self.count1 == self.count2:
                return answer == 'одинаково'
            elif self.current_count == self.count1:
                return answer == 'у ' + self.heroes[0].name
            else:
                return answer == 'у ' + self.heroes[1].name
        if num == 7:  # which number is lower?
            return answer == str(self.count1 if self.count1 <= self.count2 else self.count2)

        return False

    def drawWindow(self):
        win.blit(bg, (0, 0))
        drawCount()
        self.drawCondition()
        #        self.drawQuestion(3)
        self.drawQuestion(self.question)
        #        drawStatistics()
        pygame.display.update()


'''
        # draw net for position calculation:
        j = 40
        for i in range(1, j):
            pygame.draw.line(win, BLACK, (i * WIDTH // j, 0), (i * WIDTH // j, HEIGHT))
            pygame.draw.line(win, BLACK, (0, i * HEIGHT // j), (WIDTH, i * HEIGHT // j))
'''


# The main part of the game
def game_cycle():
    global mistakes

    clock.tick(FPS)

    need_input = True
    completed = False
    #    task = Task(True)
    task = random.choice((Task(True), Task()))
    answer = ''

    while not completed:
        task.drawWindow()
        print('TIK')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # process TAB key for showing stats
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                tab_pressed = True
                while tab_pressed:
                    drawStatistics()
                    pygame.display.update()
                    for e in pygame.event.get():
                        if e.type == pygame.KEYUP and e.key == pygame.K_TAB:
                            tab_pressed = False
            # checking the answer
            if need_input and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    answer = task.input_text
                    task.input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    task.input_text = task.input_text[:-1]
                elif len(task.input_text) < 20 and event.key != pygame.K_TAB:
                    task.input_text += event.unicode
        # exit from the cycle or mistakes calculation
        if answer != '':
            completed = task.checkAnswer(task.question, answer)
            answer = ''
            if not completed:
                mistakes += 1


solved = 0
mistakes = 0
game = True
while game:
    game_cycle()
    solved += 1
pygame.quit()
exit()
