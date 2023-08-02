import random
import math
import pygame
from pygame import mixer


# Inicjalize
pygame.init()
# Create screen
width = 1200
heigh = 750
screen = pygame.display.set_mode((width, heigh))
FPS = 70
clock = pygame.time.Clock()

num_of_enemies = 15
num_of_bullets = 6
num_of_bombs = int(num_of_enemies/3)
speed_of_bullet = 1.5  # w ile sekund ma przebyc cala trase heigh
speed_of_bombs = 3  # w ile sekund ma przebyc cala trase heigh
shoots_per_second = num_of_bullets/speed_of_bullet
bombs_per_second = num_of_bombs/speed_of_bombs

delta1 = 0.0
delta2 = 1.0/shoots_per_second
delta3 = 0.0
go = True
k = 0

# BACKGROUND
background = pygame.image.load('background.jpg')
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1- play in loop


# TITLE AND ICON
pygame.display.set_caption("Space Invaters")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


# Klasy
class Player(object):

    def __init__(self):
        self.Img = pygame.image.load('PlayerImg.png')
        self.size = (64, 64)
        self.X = int(width / 2)
        self.Y = heigh - 80
        self.speed = 2  # w ile sekund ma przebyć całą trasę width
        self.X_change = width/(FPS * self.speed)

    def draw(self):
        screen.blit(self.Img, (int(self.X), int(self.Y)))

    def move(self, key):
        if key[pygame.K_d] and self.X < width - 64:
            self.X += self.X_change
        if key[pygame.K_a] and self.X > 0:
            self.X -= self.X_change


class Enemy(object):

    def __init__(self):
        self.Img = pygame.image.load('enemy.png')
        self.speed = 4  # w ile sekund ma przebyć całą trasę width
        self.size = (64, 58)
        self.X_change = width/(FPS*self.speed)
        self.Y_change = 40
        self.X = random.randint(30, width-63)
        self.Y = 30 + random.randint(1, 3)*40

    def draw(self):
        screen.blit(self.Img, (int(self.X), int(self.Y)))

    def move(self):
        self.X += self.X_change
        if self.X >= width-64 or self.X <= 0:
            self.X_change *= -1
            self.Y += self.Y_change


class Bomb(object):
    def __init__(self, enemyX, enemyY):
        self.state = "stay"
        self.size = (24, 24)
        self.Img = pygame.image.load('bomb.png')
        self.Y_change = heigh/(FPS * speed_of_bullet)
        self.pos = [enemyX, enemyY]

    def fall(self):
        self.state = "fall"
        screen.blit(self.Img, (int(self.pos[0]), int(self.pos[1])))

    def move(self):
        if self.state == "fall":
            self.fall()
            self.pos[1] += self.Y_change

        if self.pos[1] >= heigh:
            self.state = "stay"


class Bullet(object):

    def __init__(self):
        self.Img = pygame.image.load('bullet.png')
        self.size = (16, 32)
        self.X = 0
        self.Y = player.Y
        self.Y_change = heigh/(FPS * speed_of_bullet)
        self.state = "ready"

    def fire_bullet(self):
        self.state = "fire"
        screen.blit(self.Img, (int(self.X) + 16, int(self.Y) + 10))

    def move(self):
        if self.state == "fire":
            self.fire_bullet()
            self.Y -= self.Y_change

        if self.Y <= 0:
            self.Y = player.Y
            self.state = "ready"


class Score(object):
    def __init__(self):
        self.value = 0
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.textX = 10
        self.textY = 10
        self.text = 0

    def show(self):
        self.text = self.font.render("Score: " + str(self.value), True, self.text_color)
        screen.blit(self.text, (self.textX, self.textY))


class GameOver(object):
    def __init__(self):
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont("Consolas", 100)
        self.textX = int(width/2)-250
        self.textY = int(heigh/2)-100
        self.text = 0

    def show(self):
        self.text = self.font.render("GAME OVER!!!", 1, (255, 255, 255))
        screen.blit(self.text, (self.textX, self.textY))


player = Player()
game_over = GameOver()
score = Score()
bullet = [Bullet() for i in range(num_of_bullets)]
enemy = [Enemy() for j in range(num_of_enemies)]
bomb = [Bomb(0, 0) for i in range(num_of_bombs)]


def iscollision(x1, y1, size1, x2, y2, size2 ):
    if x1 < x2 + size2[0] and x1 + size1[0]  > x2 and y1 < y2 + size2[1] and y1 + size1[1] > y2:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    bombs_per_second = num_of_bombs / speed_of_bombs
    # BACKGROUND image
    screen.blit(background, (0, 0))

    # obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    if go ==  True:
        # TICKING MOVEMENT
        dt = clock.tick()
        delta1 += dt/1000
        delta2 += dt / 1000
        delta3 += dt/1000

        while delta1 > 1/FPS:
            # PLayer Movement
            key = pygame.key.get_pressed()
            player.move(key)

            # Movement of bullet
            if key[pygame.K_SPACE]:
                if delta2 > 1 / shoots_per_second:
                    delta2 = 0
                    for j in range(num_of_bullets):
                        if bullet[j].state == "ready":
                            bullet_Sound = mixer.Sound('laser.wav')
                            bullet_Sound.play()
                            bullet[j].X = player.X
                            bullet[j].fire_bullet()
                            break

            for i in range(num_of_bullets):
                bullet[i].move()

            # Movement of enemy
            for i in range(num_of_enemies):
                enemy[i].move()

            # Movement of bomb
            if delta3 > 1 / bombs_per_second:
                delta3 = 0
                for i in range(num_of_bombs):
                    if bomb[i].state == "stay":
                        x = random.randint(0, num_of_enemies-1)
                        bomb[i].pos = [enemy[x].X + int(enemy[x].size[0]/2), enemy[x].Y + enemy[x].size[1] - 20]
                        bomb[i].fall()
                        break

            for i in range(num_of_bombs):
                bomb[i].move()

            delta1 -= 1 / FPS




    # Enemies
    for i in range(num_of_enemies):
        # Collision
        for j in range(num_of_bullets):
            if iscollision(enemy[i].X, enemy[i].Y, enemy[i].size, bullet[j].X, bullet[j].Y, bullet[j].size):
                collision_Sound = mixer.Sound('explosion.wav')
                collision_Sound.play()
                bullet[j].Y = player.Y
                bullet[j].state = "ready"
                score.value += 1
                num_of_enemies += 1
                k += 1

                enemy.append(Enemy())
                if k == 3:
                    num_of_bombs += 1
                    bomb.append(Bomb(0, 0))
                    k = 0

                enemy[i].X = random.randint(30, width - 64)
                enemy[i].Y = random.randint(30, 150)

        # Drawing enemy
        enemy[i].draw()

        # Game Over
        for j in range(num_of_bombs):
            if enemy[i].Y > (heigh - 160) or iscollision(player.X, player.Y, player.size, bomb[j].pos[0], bomb[j].pos[1], bomb[j].size):
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(int(width/2)-250, int(heigh/2)-100, 650, 100))
                game_over.show()
                mixer.music.stop()
                go = False
                break

    pygame.draw.line(screen, (255, 0, 0), (0, heigh - 100), (width, heigh - 100), 5)
    player.draw()
    score.show()
    pygame.display.update()  # refreshing display