import random
from os import path

import pygame

game_dir = path.dirname(__file__)
img_dir = path.join(game_dir, 'img')
sound_dir = path.join(game_dir, 'sound')

pygame.init()
pygame.font.init()

# text and fonts
myfont = pygame.font.SysFont('Comic Sans MS', 30)
textsurface = myfont.render('ПРИВЕТ, АРТЁМ !!!', False, (255, 255, 255))

# main_screen
screen = (800, 600)
win = pygame.display.set_mode(screen)
pygame.display.set_caption("Стрелялка")

# images
bg = pygame.image.load(path.join(img_dir, 'space.jpg')).convert()
bg = pygame.transform.scale(bg, (screen))
my_sprite = pygame.image.load(path.join(img_dir, 'artem.png')).convert_alpha()
ship = pygame.image.load(path.join(img_dir, 'ship.png')).convert_alpha()
ship_center = (random.randint(0, 700), random.randint(0, 500))

# sound
space_music = pygame.mixer.music.load(path.join(sound_dir, 'space.mp3'))
pygame.mixer.music.play(-1)

shoot_sound = pygame.mixer.Sound(path.join(sound_dir, 'bullet.wav'))
blow_sound = pygame.mixer.Sound(path.join(sound_dir, 'blow.wav'))
jump_sound = pygame.mixer.Sound(path.join(sound_dir, 'jump.wav'))

RED = (255, 0, 0)

# Player
width = 40
height = 53
speed = 10

x = 50
y = screen[1] - 5 - height
radius = 10

FPS = 30
clock = pygame.time.Clock()

isJump = False
jumpCount = 10

bullets = []
lastMove = 'right'

class Mob():

    def __init__(self):
        #        pygame.sprite.Sprite.__init__(self)
        self.image = ship
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen[0] - self.rect.width)
        self.rect.y = random.randrange(0, screen[1])
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > screen[1] + 10 or self.rect.top < 0 or self.rect.right > screen[0] + 20:
            self.rect.x = random.randrange(screen[0] - self.rect.width)
            self.rect.y = random.randrange(0, screen[1])
            self.speedy = random.randrange(1, 8)


class fireball():
    def __init__(self, x, y, radius, color, facing, vertical):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vertical = vertical
        self.vel = 8 * facing
        self.fly = 8 * vertical

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def drawWindow():
    win.blit(bg, (0, 0))
    win.blit(my_sprite, (x, y))
    win.blit(m.image, (m.rect.x, m.rect.y))
    win.blit(textsurface, (10, 10))
    #    win.fill((0, 0, 0))
    #    pygame.draw.rect(win, (255, 255, 255), (x, y, width, height))
    #    pygame.draw.circle(win, (0, 0, 255), (x, y), radius, 3)
    for bullet in bullets:
        bullet.draw(win)

    m.update()


    pygame.display.update()


m = Mob()


run = True
while run:

    clock.tick(FPS)
    drawWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < screen[0] and bullet.x > 0 and bullet.y < screen[1] and bullet.y > 0:
            bullet.x += bullet.vel
            bullet.y -= bullet.fly

        else:
            blow_sound.play()
            bullets.pop(bullets.index(bullet))

    # проверка нажатия клавиш
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LCTRL]:
        if lastMove == 'right':
            facing = 1
            vertical = 0
        if lastMove == 'left':
            facing = -1
            vertical = 0
        if lastMove == 'up':
            vertical = 1
            facing = 0
        if lastMove == 'down':
            vertical = -1
            facing = 0

        if len(bullets) <= 5:
            bullets.append(
                fireball(round(x + width // 2), round(y + height // 2), radius, (255, 0, 0), facing, vertical))

        shoot_sound.play()

    if keys[pygame.K_LEFT] and x > 5:
        x -= speed
        lastMove = 'left'

    if keys[pygame.K_RIGHT] and x < screen[0] - width - 5:
        x += speed
        lastMove = 'right'

    if keys[pygame.K_1]:
        win.blit(textsurface, (100, 100))
        pygame.display.update()

    # оставляем возможность двигаться влево и вправо во время прыжка
    if not (isJump):
        if keys[pygame.K_UP] and y > 5:
            y -= speed
            lastMove = 'up'
        if keys[pygame.K_DOWN] and y < screen[1] - height - 5:
            y += speed
            lastMove = 'down'
        if keys[pygame.K_SPACE]:
            isJump = True
    # сам прыжок
    else:
        jump_sound.play()
        if jumpCount >= - 10:
            if jumpCount < 0:
                y += (jumpCount ** 2) / 2
            else:
                y -= (jumpCount ** 2) / 2
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

pygame.quit()
