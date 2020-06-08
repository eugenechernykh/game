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


# Simplify image loading and resizing
def load_image(file, scale=(None, None)):
    if search(r'png', file):
        image = pygame.image.load(path.join(img_dir, file)).convert_alpha()
        if scale[0] is not None and scale[1] is not None:
            return pygame.transform.smoothscale(image, scale)
        else:
            return image
    else:
        image = pygame.image.load(path.join(img_dir, file)).convert()
        if scale[0] is not None and scale[1] is not None:
            return pygame.transform.smoothscale(image, scale)
        else:
            return image


hero_scale = (WIDTH // 10, HEIGHT // 6 + HEIGHT // 90)
Heroes = namedtuple("Hero", "name pic cover color")
heroes = [Heroes('Артёма', load_image('artem.png', hero_scale), 'кофта', 'синего'),
          Heroes('мамы', load_image('mama.png', hero_scale), 'футболка', 'бордового'),
          Heroes('папы', load_image('papa.png', hero_scale), 'футболка', 'синего'),
          Heroes('медведя', load_image('bear.jpg', hero_scale), 'шкура', 'коричневого'),
          Heroes('ГуммиБера', load_image('gummy.jpg', hero_scale), 'трусики', 'оранжевого'),
          Heroes('льва', load_image('lion.jpg', hero_scale), 'грива', 'коричневого'),
          Heroes('Малыша', load_image('malysh.jpg', hero_scale), 'кофта', 'красного'),
          Heroes('Пятачка', load_image('piglet.jpg', hero_scale), 'пятачок', 'розового'),
          Heroes('кролика', load_image('rabbit.jpg', hero_scale), 'кофта', 'красного'),
          Heroes('тигрёнка', load_image('tiger.jpg', hero_scale), 'полоски', 'чёрного'),
          Heroes('черепахи', load_image('turtle.jpg', hero_scale), 'голова', 'зелёного'),
          Heroes('Винни-Пуха', load_image('winny.png', hero_scale), 'лапа', 'коричневого'),
          Heroes('монстра', load_image('monster.png', hero_scale), 'пузо', 'зелёного'),
          Heroes('волка', load_image('kitty.jpg', hero_scale), 'шарф', 'красного')]

item_scale = (WIDTH // 10, WIDTH // 10)
Items = namedtuple("Item", "name pic color")
items = [Items('яблоко', load_image('apple.jpg', item_scale), 'жёлтое'),
         Items('банан', load_image('banana.jpg', item_scale), 'жёлтый'),
         Items('мяч', load_image('ball.jpg', item_scale), 'белый'),
         Items('шар', load_image('balloon.jpg', item_scale), 'красный'),
         Items('книга', load_image('book.png', item_scale), 'зелёная'),
         Items('торт', load_image('cake.jpg', item_scale), 'оранжевый'),
         Items('конфета', load_image('candy.jpg', item_scale), 'красная'),
         Items('карандаш', load_image('pen.jpg', item_scale), 'жёлтый'),
         Items('машина', load_image('car.jpg', item_scale), 'жёлтая')]

image_scale = (600, 400)
Images = namedtuple("Images", "pic text who what_does what_hands where")
images = [Images(load_image('1_man_eat.jpg', image_scale), 'Дядя ест на кухне.', ('Кто на картинке?', 'дядя'), ('Что дядя делает?', 'ест'), ('Что у дяди в руках?', 'ложка'), ('Где дядя?', 'на кухне')),
          Images(load_image('1_woman_photo.png', image_scale), 'Тётя фотографирует на улице.', ('Кто на картинке?', 'тётя'), ('Что тётя делает?', 'фотографирует'), ('Что у тёти в руках?', 'фотоаппарат'), ('Где тётя?', 'на улице')),
          Images(load_image('1_man_cut.jpg', image_scale),'Дядя режет на кухне.', ('Кто на картинке?', 'дядя'), ('Что дядя делает?', 'режет'), ('Что у дяди в руках?', 'нож'), ('Где дядя?', 'на кухне')),
          Images(load_image('1_man_knock.jpg', image_scale),'Дядя стучит в комнате.', ('Кто на картинке?', 'дядя'), ('Что дядя делает?', 'стучит'), ('Что у дяди в руках?', 'молоток'), ('Где дядя?', 'в комнате'))
          ]

#background
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
        message = str(message)  # converting int in str
    font_type = pygame.font.SysFont(font_type, font_size)
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
                  change('задача', solved, case='accs') + '.'), 7 * W_STEP, H_STEP)


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
    return morph.parse(word)[0].inflect({case}).make_agree_with_number(number)[0]


# Past time for verb in accordance with gender
def verb_change(verb: str, noun: str, num: int) -> str:
    morph = pymorphy2.MorphAnalyzer()
    if num == 1:
        return morph.parse(verb)[0].inflect(
            {'past', morph.parse(noun)[0].tag.gender})[0]
    if num > 1:
        return morph.parse(verb)[0].inflect({'past', 'neut'})[0]


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


class Pictures:
    def __init__(self, text_only=False):
        self.image = random.choice(images)
        self.text_only = text_only
        self.text = self.image[1]
        self.picture = self.image[0]
        self.rect = self.picture.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.question_answer = random.choice(self.image[2:])
        self.question = self.question_answer[0]
        self.answer = self.question_answer[1]
        self.input_text = ''

    def drawQuestion(self):
        win.blit(bg, (0, 0))
        if self.text_only:
            print_text(self.text, WIDTH // 2, 2 * line, center='yes')
        else:
            win.blit(self.picture, self.rect)
        # Question box
        print_text(self.question, WIDTH // 2, 3.5 * line, center='yes')

        # answer box
        drawSentence(('Ответ:', (self.input_text, BLUE)), start - 3 * W_STEP,
                     4 * line)
        # mistakes box
        drawSentence(('Ошибок:', (mistakes, RED)), 26 * W_STEP, 4 * line)

    def checkAnswer(self, answer):
        if answer == self.answer:
            return True
        return


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
            ('У', self.hero1, verb_change('быть', self.item.name, self.count1),
             self.count1, self.item1, '.'), start,
            line)
        drawSentence(
            ('А у', self.hero2,
             verb_change('быть', self.item.name, self.count2), self.count2,
             self.item2, '.'),
            start - W_STEP, 2 * line)
        # answer box
        drawSentence(('Ответ:', (self.input_text, BLUE)), start - 3 * W_STEP,
                     4 * line)
        # mistakes box
        drawSentence(('Ошибок:', (mistakes, RED)), 26 * W_STEP, 4 * line)

    def drawQuestion(self, num):
        if num == 1:
            drawSentence((
                'Сколько всего', self.item_many, 'у', self.hero1, 'и',
                self.hero2, '?'), start // 2 - W_STEP,
                                  3 * line)
        if num == 2:
            drawSentence(('Что больше', self.count1, 'или', self.count2, '?'),
                         start, 3 * line)
        if num == 3:
            drawSentence(('У кого', self.item_many, 'больше ?'), start,
                         3 * line)
        if num == 4:
            drawSentence(('У кого', self.item_many, 'меньше ?'), start,
                         3 * line)
        if num == 5:
            drawSentence(
                ('Какого цвета', self.heroes[0].cover, 'у', self.hero1, '?'),
                start - W_STEP, 3 * line)
        if num == 6:
            drawSentence(
                ('У кого', self.current_count, self.item_current, '?'), start,
                3 * line)
        if num == 7:
            drawSentence(('Что меньше', self.count1, 'или', self.count2, '?'),
                         start, 3 * line)

    # check the answer in accordance with the task question
    def checkAnswer(self, num, answer):
        if num == 1:  # how much together?
            return answer == str(self.count1 + self.count2)
        if num == 2:  # which number is greater?
            return answer == str(
                self.count1 if self.count1 >= self.count2 else self.count2)
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
            return answer == str(
                self.count1 if self.count1 <= self.count2 else self.count2)

        return False

    def drawWindow(self):
        win.blit(bg, (0, 0))
        drawCount()
        self.drawCondition()
        #        self.drawQuestion(3)
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

        pics = Pictures()
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
                    # process TAB key for showing stats
                    if event.key == pygame.K_TAB:
                        tab_pressed = True
                        while tab_pressed:
                            drawStatistics()
                            for e in pygame.event.get():
                                if e.type == pygame.KEYUP and e.key == pygame.K_TAB:
                                    tab_pressed = False
                    # checking the answer
                    elif event.key == pygame.K_RETURN:
                        answer = pics.input_text
                        pics.input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        pics.input_text = pics.input_text[:-1]
                    elif len(pics.input_text) < 20:
                        pics.input_text += event.unicode

            # next task or mistakes calculation
            if answer != '':
                completed = pics.checkAnswer(answer)
                answer = ''
                if not completed:
                    mistakes += 1

            pics.drawQuestion()
            drawCount()

            pygame.display.update()
        solved += 1


# The tasks game
def tasks_scene():
    run = True

    while run:
        global mistakes, solved

        clock.tick(FPS)
        completed = False
        #    task = Task(True)
        task = random.choice((Task(True), Task()))
        answer = ''

        while not completed:
            task.drawWindow()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                # process TAB key for showing stats
                    if event.key == pygame.K_TAB:
                        tab_pressed = True
                        while tab_pressed:
                            drawStatistics()
                            for e in pygame.event.get():
                                if e.type == pygame.KEYUP and e.key == pygame.K_TAB:
                                    tab_pressed = False
                    # checking the answer
                    elif event.key == pygame.K_RETURN:
                        answer = task.input_text
                        task.input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        task.input_text = task.input_text[:-1]
                    elif len(task.input_text) < 20:
                        task.input_text += event.unicode
            # next task or mistakes calculation
            if answer != '':
                completed = task.checkAnswer(task.question, answer)
                answer = ''
                if not completed:
                    mistakes += 1

            pygame.display.update()
        solved += 1


# The main part of the game
solved = 0
mistakes = 0
game = True

while game:
    title_scene()
    #tasks_scene()
    #pictures_scene()

pygame.quit()
exit()
