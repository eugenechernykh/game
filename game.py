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
WIDTH = 1200
HEIGHT = 900

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Стрелялка")

# images
bg = pygame.image.load(path.join(img_dir, 'space.jpg')).convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
my_sprite = pygame.image.load(path.join(img_dir, 'artem_space.png')).convert_alpha()
ship = pygame.image.load(path.join(img_dir, 'ship.png')).convert_alpha()
fireb = pygame.image.load(path.join(img_dir, 'fireball.png')).convert_alpha()

# sound
space_music = pygame.mixer.music.load(path.join(sound_dir, 'space.mp3'))
pygame.mixer.music.play(-1)

shoot_sound = pygame.mixer.Sound(path.join(sound_dir, 'bullet.wav'))
blow_sound = pygame.mixer.Sound(path.join(sound_dir, 'blow.wav'))
jump_sound = pygame.mixer.Sound(path.join(sound_dir, 'jump.wav'))
death_sound = pygame.mixer.Sound(path.join(sound_dir, 'deadscrm.wav'))

FPS = 30
clock = pygame.time.Clock()


def print_text(message, x, y, font_color=(255, 255, 255), font_type='Comic Sans MS', font_size=40):
    if isinstance(message, int):
        message = str(message)  # converting int in str
    font_type = pygame.font.SysFont(font_type, font_size)
    text = font_type.render(message, True, font_color)
    win.blit(text, (x, y))
    return text.get_width()


def drawSentence(sentence: tuple, x: int, y: int) -> None:
    for n in sentence:
        if isinstance(n, tuple):
            message, color = n
            x += print_text(message, x, y, color) + 20  # indent after drawing the text
        elif isinstance(n, pygame.Surface):
            surf = win.blit(n, (x, y - n.get_height() // 3))  # centering the surface in line
            x += surf.width + 20  # indent after drawing the surface
        else:
            x += print_text(n, x, y) + 20  # indent after drawing the text


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = my_sprite
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 8
        self.isJump = False
        self.jumpCount = 10
        self.lastMove = 'right'
        self.lives = 5
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.immortal = False
        self.immortal_timer = pygame.time.get_ticks()

    def immortal_mode(self):
        self.immortal = True
        self.immortal_timer = pygame.time.get_ticks()

    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH // 2, HEIGHT + 400)

    def shoot(self):
        bullet = Fireball(self.rect.centerx, self.rect.centery, facing, vertical)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def update(self):
        # показать, если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2500:
            self.hidden = False
            self.rect.centerx = WIDTH // 2
            self.rect.bottom = HEIGHT - 10

        if self.immortal and pygame.time.get_ticks() - self.immortal_timer > 2500:
            self.immortal = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 5:
            self.rect.x -= self.speed
            self.lastMove = 'left'
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 5:
            self.rect.x += self.speed
            self.lastMove = 'right'
        # Deny moving up and down during the jump
        if not self.isJump:
            if keys[pygame.K_UP] and self.rect.top > 5:
                self.rect.y -= self.speed
                self.lastMove = 'up'
            if keys[pygame.K_DOWN] and self.rect.bottom > - 5:
                self.rect.y += self.speed
                self.lastMove = 'down'
            if keys[pygame.K_SPACE]:
                self.isJump = True
        # Jump physics as a parabola
        else:
            jump_sound.play()
            if self.jumpCount >= - 10:
                if self.jumpCount < 0:
                    self.rect.y += (self.jumpCount ** 2) // 2
                else:
                    self.rect.y -= (self.jumpCount ** 2) // 2
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10


class Mob(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ship
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(0, HEIGHT)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(1, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, facing, vertical):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.smoothscale(fireb, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.facing = facing
        self.vertical = vertical
        self.speedx = 10 * facing
        self.speedy = 10 * vertical

    def update(self):
        if WIDTH > self.rect.centerx > 0 and HEIGHT > self.rect.centery > 0:
            self.rect.x += self.speedx
            self.rect.y -= self.speedy
        else:
            blow_sound.play()
            self.kill()


def drawWindow():
    win.blit(bg, (0, 0))
    win.blit(textsurface, (10, 10))  # Say Hi to Artem :)
    all_sprites.draw(win)
    drawSentence(('Scores:', score), 950, 30)
    drawSentence(('Lives:', player.lives), 550, 30)
    pygame.display.update()


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
player.immortal_mode()

all_sprites.add(player)
for i in range(3):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

facing = 1
vertical = 0
score = 0
lives = 5

run = True
while run:

    clock.tick(FPS)
    drawWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                if player.lastMove == 'right':
                    facing = 1
                    vertical = 0
                if player.lastMove == 'left':
                    facing = -1
                    vertical = 0
                if player.lastMove == 'up':
                    vertical = 1
                    facing = 0
                if player.lastMove == 'down':
                    vertical = -1
                    facing = 0
                player.shoot()

    all_sprites.update()

    # Проверка: попали ли по мобу
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    if hits:
        score += 1

    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    if not player.immortal:
        # Проверка: не ударил ли  игрока
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_rect)
        if hits:
            if player.lives > 0:
                player.lives -= 1
                death_sound.play()
                player.hide()
                player.immortal_mode()
            else:
                run = False


pygame.quit()
