from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_img, player_x, player_y, width, height, speed=0):
        super().__init__()
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

class Enemy(GameSprite):
    direction = "right"
    directionY = "up"
    run_x = 0
    run_y = 0
    cadr = 0
    points = [(150, 100), (550, 100), (550, 400), (150, 400)]
    point_index = 0

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        if self.direction == "left":
            self.rect.x -= self.speed
        if self.rect.x > 600:
            self.direction = "left"
        elif self.rect.x < 100:
            self.direction = "right"
        self.reset()

    def updateY(self):
        if self.directionY == "up":
            self.rect.y += self.speed
        if self.directionY == "down":
            self.rect.y -= self.speed
        if self.rect.y > 400:
            self.directionY = "down"
        elif self.rect.y < 100:
            self.directionY = "up"
        self.reset()

    def updateR(self):
        if self.cadr % 30 == 0:
            self.run_x = randint(-self.speed, self.speed)
            self.run_y = randint(-self.speed, self.speed)
        self.cadr += 1
        self.rect.x += self.run_x
        self.rect.y += self.run_y
        if self.rect.y < 0:
            self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y -= self.speed
        self.reset()

    def update_points(self):
        new_x, new_y = self.points[self.point_index]
        if self.rect.x < new_x:
            self.rect.x += self.speed
        elif self.rect.x > new_x:
            self.rect.x -= self.speed
        if self.rect.y < new_y:
            self.rect.y += self.speed
        elif self.rect.y > new_y:
            self.rect.y -= self.speed
        if abs(self.rect.x - new_x) < self.speed and abs(self.rect.y - new_y) < self.speed:
            self.point_index = (self.point_index + 1) % len(self.points)
        self.reset()

class Wall(sprite.Sprite):
    def __init__(self, color, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.image = Surface((wall_width, wall_height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Лабіринт")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.set_volume(0.5)
mixer.music.play()
moneySound = mixer.Sound("money.ogg")
kickSound = mixer.Sound("kick.ogg")

font.init()
font2 = font.Font(None, 50)
win = font2.render("Ти виграв,вітаю!", True, (0, 255, 0))
lose = font2.render("Ти програв!", True, (60, 200, 90))

run = True
clock = time.Clock()

player = Player("costume.png", 0, 10, 100, 100, 5)
monster = Enemy("cyborg3.png", 300, 200, 100, 100, 2)
monster2 = Enemy("cyborg.png", 150, 100, 100, 100, 2)
gold = GameSprite("keys.png", win_width - 100, win_height - 100, 80, 80)

wall_color = (51, 153, 102)
walls = [
    Wall(wall_color, 100, 100, 20, 100),
    Wall(wall_color, 100, 100, 100, 20),
    Wall(wall_color, 300, 300, 20, 100),
    Wall(wall_color, 300, 300, 100, 20),
    Wall(wall_color, 350, 0, 20, 50),
    Wall(wall_color, 0, 400, 50, 20),
    Wall(wall_color, 500, 400, 50, 20),
    Wall(wall_color, 600, 0, 50, 20),
    Wall(wall_color, 200, 200, 20, 50),
    Wall(wall_color, 200, 300, 50, 20),
    Wall(wall_color, 500, 200, 20, 50),
    Wall(wall_color, 100, 300, 20, 50),
    Wall(wall_color, 400, 200, 50, 20),
    Wall(wall_color, 500, 300, 20, 50),
    Wall(wall_color, 100, 400, 20, 50),
    Wall(wall_color, 650, 200, 50, 20),
    Wall(wall_color, 450, 200, 20, 50),
    Wall(wall_color, 0, 200, 50, 20)
]

finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish:
        window.blit(background, (0, 0))
        player.update()
        monster.updateR()
        monster.update()
        monster.updateY()
        gold.reset()
        monster2.update_points()

        for wall in walls:
            wall.reset()

        if sprite.collide_rect(player, gold):
            moneySound.play()
            window.blit(win, (200, 200))
            finish = True

        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, monster2) or any(sprite.collide_rect(player, wall) for wall in walls):
            kickSound.play()
            window.blit(lose, (200, 200))
            finish = True

    display.update()
    clock.tick(60)