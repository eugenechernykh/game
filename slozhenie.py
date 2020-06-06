import random
from collections import namedtuple
from os import path
from sys import exit

import pygame
from win32api import LoadKeyboardLayout

pygame.init()
pygame.font.init()

# set russian as default layout
LoadKeyboardLayout("00000419", 1)

# directories initialisation
game_dir = path.dirname(__file__)
img_dir = path.join(game_dir, 'img')

# main_screen
WIDTH = 1200
HEIGHT = 900
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Сложение")

# set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# images
bg = pygame.image.load(path.join(img_dir, 'board1.jpg')).convert()
bg = pygame.transform.smoothscale(bg, (WIDTH, HEIGHT))

Heroes = namedtuple("Hero", "name pic cover color")
heroes = [Heroes('Артёма', pygame.image.load(path.join(img_dir, 'artem.png')).convert_alpha(), 'кофта', 'синего'),
          Heroes('мамы', pygame.image.load(path.join(img_dir, 'mama.png')).convert_alpha(), 'футболка', 'бордового'),
          Heroes('папы', pygame.image.load(path.join(img_dir, 'papa.png')).convert_alpha(), 'футболка', 'синего'),
          Heroes('медведя', pygame.image.load(path.join(img_dir, 'bear.jpg')).convert(), 'шкура', 'коричневого'),
          Heroes('ГуммиБера', pygame.image.load(path.join(img_dir, 'gummy.jpg')).convert(), 'трусики', 'оранжевого'),
          Heroes('льва', pygame.image.load(path.join(img_dir, 'lion.jpg')).convert(), 'грива', 'коричневого'),
          Heroes('Малыша', pygame.image.load(path.join(img_dir, 'malysh.jpg')).convert(), 'кофта', 'красного'),
          Heroes('Пятачка', pygame.image.load(path.join(img_dir, 'piglet.jpg')).convert(), 'пятачок', 'розового'),
          Heroes('кролика', pygame.image.load(path.join(img_dir, 'rabbit.jpg')).convert(), 'кофта', 'красного'),
          Heroes('тигрёнка', pygame.image.load(path.join(img_dir, 'tiger.jpg')).convert(), 'полоски', 'чёрного'),
          Heroes('черепахи', pygame.image.load(path.join(img_dir, 'turtle.jpg')).convert(), 'голова', 'зелёного'),
          Heroes('Винни-Пуха', pygame.image.load(path.join(img_dir, 'winny.png')).convert_alpha(), 'лапа',
                 'коричневого'),
          Heroes('монстра', pygame.image.load(path.join(img_dir, 'monster.png')).convert_alpha(), 'пузо', 'зелёного'),
          Heroes('волка', pygame.image.load(path.join(img_dir, 'kitty.jpg')).convert(), 'шарф', 'красного')
          ]

# colors = ['белый', 'чёрный', 'бежевый', 'бордовый', 'желтый', 'зеленый',
#          'золотой', 'красный', 'оранжевый', 'серый', 'розовый', 'синий',
#          'фиолетовый', 'голубой']
Items = namedtuple("Item", "name pic color")
items = [Items('яблоко', pygame.image.load(path.join(img_dir, 'apple.jpg')).convert(), 'жёлтое'),
         Items('банан', pygame.image.load(path.join(img_dir, 'banana.jpg')).convert(), 'жёлтый'),
         Items('мяч', pygame.image.load(path.join(img_dir, 'ball.jpg')).convert(), 'белый'),
         Items('шар', pygame.image.load(path.join(img_dir, 'balloon.jpg')).convert(), 'красный'),
         Items('книга', pygame.image.load(path.join(img_dir, 'book.png')).convert_alpha(), 'зелёная'),
         Items('торт', pygame.image.load(path.join(img_dir, 'cake.jpg')).convert(), 'оранжевый'),
         Items('конфета', pygame.image.load(path.join(img_dir, 'candy.jpg')).convert(), 'красная'),
         Items('карандаш', pygame.image.load(path.join(img_dir, 'pen.jpg')).convert(), 'жёлтый'),
         Items('машина', pygame.image.load(path.join(img_dir, 'car.jpg')).convert(), 'жёлтая')]


# show amount of solved tasks
def drawCount():
    print_text('Привет! Ты правильно решил', WIDTH // 10, HEIGHT // 100)
    # shift the box if number has two or more digits
    if solved < 10:
        print_text(str(solved), (3 * WIDTH) // 5, HEIGHT // 100, RED)
        print_text('задач{}.'.format('у' if solved == 1 else ('и' if 1 < solved < 5 else '')),
                   3 * WIDTH // 5 + 50, HEIGHT // 100)
    else:
        print_text(str(solved), (3 * WIDTH) // 5, HEIGHT // 100, RED)
        print_text('задач{}.'.format('у' if solved == 1 else ('и' if 1 < solved < 5 else '')),
                   3 * WIDTH // 5 + 65, HEIGHT // 100)


# show success rate
def drawStatistics():
    print_text('Успешность:', WIDTH - WIDTH // 3 + 20, HEIGHT - HEIGHT // 8)
    if mistakes == 0 and solved == 0:
        print_text('0%', WIDTH - WIDTH // 10, HEIGHT - HEIGHT // 8, RED)
    else:
        print_text(str(100 * solved // (solved + mistakes)) + '%', WIDTH - WIDTH // 10, HEIGHT - HEIGHT // 8, RED)


class Task:

    def __init__(self):
        self.question = random.randint(1, 7)
        self.heroes = random.sample(heroes, 2)
        self.count1 = random.randint(1, 15)
        self.count2 = random.randint(1, 15)
        self.current_count = random.choice((self.count1, self.count2))
        self.item = random.choice(items)
        self.input_text = ''
        self.mistakes = 0

        # we need to adjust image sizes
        self.item = self.item._replace(pic=pygame.transform.smoothscale(self.item.pic, (120, 120)))
        for i in 0, 1:
            self.heroes[i] = self.heroes[i]._replace(pic=pygame.transform.smoothscale(self.heroes[i].pic, (120, 160)))

    def drawCondition(self):
        start = 100
        first_column = 250
        second_column = 680
        third_column = 920

        first_line = 180
        second_line = 360
        third_line = 540

        # show task's condition
        print_text('У ', start + 50, first_line)
        win.blit(self.heroes[0].pic, (first_column, first_line - 60))
        print_text('был{}  '.format('o' if self.count1 != 1 else '') + str(self.count1), start + 350, first_line)
        win.blit(self.item.pic, (second_column, first_line - 30))
        print_text('А у ', start, second_line)
        win.blit(self.heroes[1].pic, (first_column, second_line - 40))
        print_text('был{}  '.format('o' if self.count2 != 1 else '') + str(self.count2), start + 350, second_line)
        win.blit(self.item.pic, (second_column, second_line - 20))
        # answer box
        print_text('Ответ: ', start, HEIGHT - HEIGHT // 5)
        print_text(self.input_text, start + 150, HEIGHT - HEIGHT // 5)
        # mistakes box
        print_text('Ошибок:', WIDTH - WIDTH // 4, HEIGHT - HEIGHT // 5)
        print_text(str(mistakes), WIDTH - WIDTH // 10, HEIGHT - HEIGHT // 5, RED)

    def drawWindow(self):
        win.blit(bg, (0, 0))
        drawCount()
        self.drawCondition()
        #        self.drawQuestion(3)
        self.drawQuestion(self.question)
        #        drawStatistics()
        pygame.display.update()

    def drawQuestion(self, num):
        start = 100
        first_column = 250
        second_column = 680
        third_column = 920

        first_line = 180
        second_line = 360
        third_line = 540

        if num == 1:
            print_text('Сколько всего ', start, third_line)
            win.blit(self.item.pic, (first_column + 180, third_line - 20))
            print_text(' у ', start + 490, third_line)
            win.blit(self.heroes[0].pic, (second_column, third_line - 20))
            print_text(' и ', start + 730, third_line)
            win.blit(self.heroes[1].pic, (third_column, third_line - 20))
            print_text('?', WIDTH - 120, third_line)
        if num == 2:
            print_text('Что больше {} или {} ?'.format(self.count1, self.count2), start, third_line)
        if num == 3:
            print_text('У кого', start, third_line)
            win.blit(self.item.pic, (first_column, third_line - 20))
            print_text('больше ?', first_column + 150, third_line)
        if num == 4:
            print_text('У кого ' + str(self.current_count), start, third_line)
            win.blit(self.item.pic, (first_column + 50, third_line - 20))
            print_text('?', first_column + 200, third_line)
        if num == 5:
            print_text('Какого цвета ' + str(self.heroes[0].cover) + ' у', start, third_line + 20)
            win.blit(self.heroes[0].pic, (second_column - 80, third_line - 20))
            print_text('?', second_column + 70, third_line + 20)
        if num == 6:
            print_text('У кого', start, third_line)
            win.blit(self.item.pic, (first_column, third_line - 20))
            print_text('меньше ?', first_column + 150, third_line)
        if num == 7:
            print_text('Что меньше {} или {} ?'.format(self.count1, self.count2), start, third_line)

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
            if self.count1 == self.count2:
                return answer == 'одинаково'
            elif self.current_count == self.count1:
                return answer == 'у ' + self.heroes[0].name
            else:
                return answer == 'у ' + self.heroes[1].name
        if num == 5:  # which color?
            return answer == self.heroes[0].color
        if num == 6:  # who has less?
            if self.count1 < self.count2:
                return answer == 'у ' + self.heroes[0].name
            elif self.count1 == self.count2:
                return answer == 'одинаково'
            else:
                return answer == 'у ' + self.heroes[1].name
        if num == 7:  # which number is lower?
            return answer == str(self.count1 if self.count1 <= self.count2 else self.count2)

        return False


# show text on a surface
def print_text(message, x, y, font_color=WHITE, font_type='Comic Sans MS', font_size=40):
    font_type = pygame.font.SysFont(font_type, font_size)
    text = font_type.render(message, True, font_color)
    win.blit(text, (x, y))


# The main part of the game
def game_cycle():
    global mistakes

    need_input = True
    completed = False
    task = Task()
    answer = ''

    while not completed:
        # clock.tick(FPS)
        task.drawWindow()

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
        if answer != '':
            completed = task.checkAnswer(task.question, answer)
            answer = ''
            if not completed:
                mistakes += 1

    return 1


solved = 0
mistakes = 0
game = True
while game:
    solved += game_cycle()
pygame.quit()
exit()
