import random, sys
from os import path

import pygame

pygame.init()
pygame.font.init()

# directories initialisation
game_dir = path.dirname(__file__)
img_dir = path.join(game_dir, 'img')
# sound_dir = path.join(game_dir, 'sound')
'''
#set clock block for future
FPS = 30
clock = pygame.time.Clock()
'''
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

pictures = [pygame.image.load(path.join(img_dir, 'artem.png')).convert_alpha(),
            pygame.image.load(path.join(img_dir, 'mama.png')).convert_alpha(),
            pygame.image.load(path.join(img_dir, 'papa.png')).convert(),
            pygame.image.load(path.join(img_dir, 'bear.jpg')).convert(),
            pygame.image.load(path.join(img_dir, 'bee.jpg')).convert(),
            pygame.image.load(path.join(img_dir, 'gummy.jpg')).convert(),
            pygame.image.load(path.join(img_dir, 'lion.jpg')).convert(),
            pygame.image.load(path.join(img_dir, 'malysh.jpg')).convert(),
            pygame.image.load(path.join(img_dir, 'piglet.jpg')).convert(),
            pygame.image.load(path.join(img_dir, 'rabbit.jpg')).convert(),
            pygame.image.load(path.join(img_dir, 'tiger.jpg')).convert(),
            pygame.image.load(path.join(img_dir, 'turtle.jpg')).convert(),
            pygame.image.load(path.join(img_dir, 'winny.png')).convert_alpha(),
            pygame.image.load(path.join(img_dir, 'monster.png')).convert_alpha()]

items = [pygame.image.load(path.join(img_dir, 'apple.jpg')).convert(),
         pygame.image.load(path.join(img_dir, 'banana.jpg')).convert(),
         pygame.image.load(path.join(img_dir, 'car.jpg')).convert(),
         pygame.image.load(path.join(img_dir, 'ball.jpg')).convert(),
         pygame.image.load(path.join(img_dir, 'balloon.jpg')).convert(),
         pygame.image.load(path.join(img_dir, 'book.png')).convert(),
         pygame.image.load(path.join(img_dir, 'cake.jpg')).convert(),
         pygame.image.load(path.join(img_dir, 'candy.jpg')).convert(),
         pygame.image.load(path.join(img_dir, 'pen.jpg')).convert()]


# show amount of solved tasks
def drawCount():
    print_text('Привет! Ты правильно решил', WIDTH // 10, HEIGHT // 100)
    print_text(str(solved), (3 * WIDTH) // 5, HEIGHT // 100, RED)
    if solved == 1:
        print_text('задачу.', 3 * WIDTH // 5 + 50, HEIGHT // 100)
    elif 1 < solved < 5:
        print_text('задачи.', 3 * WIDTH // 5 + 50, HEIGHT // 100)
    else:
        print_text('задач.', 3 * WIDTH // 5 + 50, HEIGHT // 100)


class Task:

    def __init__(self):
        self.heroes = random.sample(pictures, 2)
        self.count1 = random.randint(1, 15)
        self.count2 = random.randint(1, 15)
        self.item = pygame.transform.smoothscale(random.choice(items), (120, 120))
        self.summa = self.count1 + self.count2
        self.input_text = ''
        for i in 0, 1:
            self.heroes[i] = pygame.transform.smoothscale(self.heroes[i], (120, 160))

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
        win.blit(self.heroes[0], (first_column, first_line - 60))
        print_text('был{}  '.format('o' if self.count1 != 1 else '') + str(self.count1), start + 350, first_line)
        win.blit(self.item, (second_column, first_line - 30))
        print_text('А у ', start, second_line)
        win.blit(self.heroes[1], (first_column, second_line - 40))
        print_text('был{}  '.format('o' if self.count2 != 1 else '') + str(self.count2), start + 350, second_line)
        win.blit(self.item, (second_column, second_line - 20))
        print_text('Сколько всего ', start, third_line)
        win.blit(self.item, (first_column + 180, third_line - 20))
        print_text(' у ', start + 490, third_line)
        win.blit(self.heroes[0], (second_column, third_line - 20))
        print_text(' и ', start + 730, third_line)
        win.blit(self.heroes[1], (third_column, third_line - 20))
        print_text('?', WIDTH - 120, third_line)
        # answer box
        print_text('Ответ: ', start, HEIGHT - HEIGHT // 5)
        print_text(self.input_text, start + 150, HEIGHT - HEIGHT // 5)

    def drawWindow(self):
        win.blit(bg, (0, 0))
        drawCount()
        self.drawCondition()

        pygame.display.update()


# show text on a surface
def print_text(message, x, y, font_color=WHITE, font_type='Comic Sans MS', font_size=40):
    font_type = pygame.font.SysFont(font_type, font_size)
    text = font_type.render(message, True, font_color)
    win.blit(text, (x, y))


# The main part of the code
def game_cycle():
    need_input = True
    answer = 0
    task = Task()

    while answer != task.summa:
        # clock.tick(FPS)
        task.drawWindow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # checking the answer
            if need_input and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        answer = int(task.input_text)
                    except:
                        task.input_text = ''
                    task.input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    task.input_text = task.input_text[:-1]
                else:
                    if len(task.input_text) < 2:
                        task.input_text += event.unicode
    return 1


game = True
solved = 0
while game:
    solved += game_cycle()
pygame.quit()
sys.exit()