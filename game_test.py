import random
from collections import namedtuple
from os import path
from re import search
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
bg = pygame.image.load(path.join(img_dir, 'board1.jpg')).convert()
bg = pygame.transform.smoothscale(bg, (WIDTH, HEIGHT))
ship = pygame.image.load(path.join(img_dir, 'ship.png')).convert_alpha()
print(type(ship))
# directories initialisation
game_dir = path.dirname(__file__)
img_dir = path.join(game_dir, 'img')

Heroes = namedtuple("Hero", "name picture cover color")
heroes = [Heroes('Артём', pygame.image.load(path.join(img_dir, 'artem.png')).convert_alpha(), 'кофта', 'синяя'),
          Heroes('Мама', pygame.image.load(path.join(img_dir, 'mama.png')).convert_alpha(), 'футболка', 'бардовая'),
          Heroes('Папа', pygame.image.load(path.join(img_dir, 'papa.png')).convert_alpha(), 'футболка', 'синяя'),
          Heroes('медведь', pygame.image.load(path.join(img_dir, 'bear.jpg')).convert, '', 'коричневый'),
          Heroes('ГуммиБер', pygame.image.load(path.join(img_dir, 'gummy.jpg')).convert, '', 'зелёный'),
          Heroes('лев', pygame.image.load(path.join(img_dir, 'lion.jpg')).convert, '', 'жёлтый'),
          Heroes('Малыш', pygame.image.load(path.join(img_dir, 'malysh.jpg')).convert, 'кофта', 'красная'),
          Heroes('Пятачок', pygame.image.load(path.join(img_dir, 'piglet.jpg')).convert, '', 'розовый'),
          Heroes('кролик', pygame.image.load(path.join(img_dir, 'rabbit.jpg')).convert, 'кофта', 'красная'),
          Heroes('тигрёнок', pygame.image.load(path.join(img_dir, 'tiger.jpg')).convert, '', 'жёлтый'),
          Heroes('черепаха', pygame.image.load(path.join(img_dir, 'turtle.jpg')).convert, '', 'зелёная'),
          Heroes('Винни-Пух', pygame.image.load(path.join(img_dir, 'winny.png')).convert, '', 'коричневый'),
          Heroes('монстр', pygame.image.load(path.join(img_dir, 'monster.png')).convert, '', 'зелёный'),
          ]
W_STEP = WIDTH // 40
H_STEP = HEIGHT // 40

def drawSentence(list, x, y):
    for n in list:
        if isinstance(n, tuple):
            text, color = n
            if isinstance(text, str):
                x += print_text(text, x, y, color) + W_STEP // 2
        if isinstance(n, int):
            n = str(n)
        if isinstance(n, str):
            x += print_text(n, x, y) + W_STEP // 2
        if isinstance(n, pygame.Surface):
            surf = win.blit(n, (x, y))
            x += surf.width + W_STEP // 2


def print_text(message, x, y, font_color=(255, 255, 255), font_type='Comic Sans MS', font_size=40):
    font_type = pygame.font.SysFont(font_type, font_size)
    text = font_type.render(message, True, font_color)
    win.blit(text, (x, y))
    return text.get_width()

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    win.blit(bg, (0, 0))
#    print_text('Hello World!!!', 100, 100)
    drawSentence(['Hello World!!!', 5, ('RED', (255, 0, 0)), 'abc', ship, ship], 100, 100)
    pygame.display.update()
pygame.quit()
exit()