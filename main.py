from pygame import *
from random import *


class GameSprite(sprite.Sprite):
    def __init__(self, player_img, player_x, player_y, width, height, speed=0):
        self.image = transform.scale(image.load(player_img), (width, height))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()

        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed

        if keys[K_s] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed

        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys[K_d] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed

        self.reset()


win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Лабіринт")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.set_volume(0.5)
mixer.music.play()

run = True
clock = time.Clock()

player = Player("costume.png", 200, 100, 100, 100, 5)
monster = GameSprite("cyborg3.png", 300, 200, 100, 100, 5)
gold = GameSprite("keys.png", win_width - 100, win_height - 100, 80, 80)

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False

    window.blit(background, (0, 0))
    player.update()
    monster.reset()
    gold.reset()

    display.update()
    clock.tick(60)
