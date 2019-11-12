import pygame
import os
import random
import math
from pygame import mixer

current_path = os.path.dirname(__file__)  # Where your .py file is located
# The resource folder path
resource_path = os.path.join(current_path, 'resources')
image_path = os.path.join(resource_path, 'images')  # The image folder path
sound_path = os.path.join(resource_path, 'sounds')

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load(os.path.join(image_path, 'background.jpg'))

# Background sound
mixer.music.load(os.path.join(sound_path, 'soundback.wav'))
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders by #Paint")
pygame.display.set_icon(pygame.image.load(
    os.path.join(image_path, 'icon.png')))

# Player
playerImg = pygame.image.load(os.path.join(image_path, 'player.png'))
playerX = 370
playerY = 480
playerX_change = 0

# Alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
aliens_num = 6
for i in range(aliens_num):
    alienImg.append(pygame.image.load(os.path.join(image_path, 'alien.png')))
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(50, 150))
    alienX_change.append(3)
    alienY_change.append(40)

# Bullet
bulletImg = pygame.image.load(os.path.join(image_path, 'bullet.png'))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"
# ready state = cant see the bullet
# fire = mooving the file

# Score display
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
game_over = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    gg = game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gg, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt((math.pow(alienX-bulletX, 2)) + (math.pow(alienY-bulletY, 2)))
    if distance < 27:
        return True


running = True
while running:
    screen.fill((150, 0, 150))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard check
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -4
            if event.key == pygame.K_d:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound(
                        os.path.join(sound_path, 'laser.wav'))
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a:
                playerX_change = 0

    # Outofbound check
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy move
    for i in range(aliens_num):
         # Game Over
        if alienY[i] > 440:
            for j in range(aliens_num):
                alienY[j] = 2000
            game_over_text()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 3
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -3
            alienY[i] += alienY_change[i]

        # Collision
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound(os.path.join(sound_path, 'explosion.wav'))
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value+=1
            alienX[i] = random.randint(0, 735)
            alienY[i] = random.randint(50, 150)

        alien(alienX[i], alienY[i], i)

    # Bullet move
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
