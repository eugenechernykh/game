import random, sys
from os import path
from collections import namedtuple

import pygame

pygame.init()
pygame.font.init()

# main_screen
WIDTH = 1200
HEIGHT = 900
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Сложение")

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

hero_in_class = random.sample(heroes, 2)
for i in 0, 1:
    hero_in_class[i]._replace(picture = pygame.transform.smoothscale(heroes[i].picture, (120, 160)))

print(1 == 2 or 1 == 3)