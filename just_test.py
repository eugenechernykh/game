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

win = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("Истории в картинках")


game_dir = path.dirname(__file__)
data_dir = path.join(game_dir, 'data')
img_dir = path.join(game_dir, 'img')

Images = namedtuple("Images", "pic text questions")
image_scale = (600, 400)

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


def load_img(text_file_name, scale):
    my_images = []
    with open(path.join(data_dir, text_file_name), 'r', encoding='utf8') as inFile:
        for line in inFile:
            my_list = list(line.split(','))
            pic, text, que = my_list[0], my_list[1], my_list[2:]
            que = [question.strip() for question in que]
            questions = {}
            for i in range(len(que)):
                if i % 2 == 1:
                    questions[que[i-1]] = que[i]
            my_images.append(Images(load_image(str(pic), scale), text, questions))
    return my_images


images = load_img('images_1.csv', image_scale)
