import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800,600))

# Title and Icon
pygame.display.set_caption('Star Invade Wars')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Space background
background = pygame.image.load('planetEarth.png')

mixer.music.load('rebel-theme.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('battleship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('missile.png')
bulletX = 0
bulletY = playerY
bulletY_change = 1
bullet_state = 'ready'

# Score
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 640
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)
gameOverX = 200
gameOverY = 250
gameOv = False

# Restart text
restart_font = pygame.font.Font('freesansbold.ttf',32)

# Enemy Fighter
enemyFighterImg = []
enemyFighterX = []
enemyFighterY = []
enemyFighterX_change = []
enemyFighterY_change = []
numFighters = 3

for i in range(numFighters):
    enemyFighterImg.append(pygame.image.load('aircraft.png'))
    enemyFighterX.append(random.randint(0,736))
    enemyFighterY.append(random.randint(50, 150))
    enemyFighterX_change.append(0)
    enemyFighterY_change.append(.5)

# Enemy Bomber
enemyBomberImg = []
enemyBomberX = []
enemyBomberY = []
enemyBomberX_change = []
enemyBomberY_change = []
numBombers = 3

# Enemy Fire
bombImg = pygame.image.load('atomic-bomb.png')
bombX = 0
bombY = 0
bombX_change = 0
bombY_change = .5
bomb_state = 'ready'


for i in range(numBombers):
    enemyBomberImg.append(pygame.image.load('tie.png'))
    enemyBomberX.append(random.randint(0,736))
    enemyBomberY.append(random.randint(20, 50))
    enemyBomberX_change.append(.3)
    enemyBomberY_change.append(60)

# Death star
deathStarImg = pygame.image.load('death-star2.png')

def player(x,y):
    screen.blit(playerImg, (x, y))

def fireBullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def enemyBomb(x,y,i):
    global bomb_state
    bomb_state = 'fire'
    screen.blit(bombImg, (x+16, y + 10))

def enemyFighter(x,y,i):
    screen.blit(enemyFighterImg[i], (x,y))

def enemyBomber(x,y, i):
    screen.blit(enemyBomberImg[i],(x,y))

def deathStar():
    screen.blit(deathStarImg,(20,10))

def isCollisionBomber(enemyBomberX, enemyBomberY, bulletX, bulletY):
    distance = math.sqrt(math.pow(bulletX - enemyBomberX, 2)) + (math.pow(bulletY - enemyBomberY, 2))
    if distance < 27:
        return True

def isCollisionFighter(enemyFighterX, enemyFighterY, bulletX, bulletY):
    distance = math.sqrt(math.pow(bulletX - enemyFighterX, 2)) + (math.pow(bulletY - enemyFighterY, 2))
    if distance < 27:
        return True

def showScore(x,y):
    score = font.render('Score: ' + str(scoreValue),True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text(x,y):
    gameOver = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(gameOver, (x, y))
    return True

def isCrashFighter(enemyFighterX, enemyFighterY, X, Y):
    distance = math.sqrt(math.pow(playerX - enemyFighterX, 2)) + (math.pow(playerY - enemyFighterY, 2))
    if distance < 64:
        return True

def isCrashBomber(enemyBomberX, enemyBomberY, X, Y):
    distance = math.sqrt(math.pow(enemyBomberX - playerX, 2)) + (math.pow(enemyBomberY - playerY, 2))
    if distance < 150:
        return True

def bombCollision():
    distance = math.sqrt(math.pow(bombX - playerX, 2)) + (math.pow(bombY - playerY, 2))
    if distance < 27:
        return True

# Game loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background,(0,0))

    # Lets player exit/quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        # If keystroke is pressed, check whether its right or left
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change -= .5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change += .5
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                playerY_change -= .5
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                playerY_change += .5
            if event.key == pygame.K_r and gameOv:
                pass
            if event.key == pygame.K_SPACE:
            # Adjusting for bullet_state
                if bullet_state != 'fire':
                    bullet_Sound = mixer.Sound('blaster-firing.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fireBullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                playerY_change = 0

    # Checking boundaries of spaceship so it doesnt go out of bounds
    playerX += playerX_change
    playerY += playerY_change
    if playerX >= -10 and playerX <= 0:
        playerX = 0
    if playerX >= 736 and playerX <= 740:
        playerX = 736
    if playerY >= 390 and playerY <= 400:
        playerY = 400
    if playerY >= 540 and playerY <= 550:
        playerY = 540
    if playerX <= -50 and playerY <= -50:
        playerX = -100
        playerY = -100

    deathStar()

    #Bullet Movement
    if bullet_state == 'fire':
        fireBullet(bulletX,bulletY)
        bulletY -= bulletY_change
    if bulletY < 0:
        bullet_state = 'ready'
        bulletY = playerY

    # Bomb Movement
    for i in range(numBombers):
        if bomb_state == 'fire':
            enemyBomb(bombX,bombY,i)
            bombY += bombY_change
        if bombY > 500:
            bomb_state = 'ready'
            bombY = enemyBomberY[i]

    # Score
    showScore(textX,textY)

    # Fighter movement/collision
    for i in range(numFighters):
        enemyFighterY[i] += enemyFighterY_change[i]
        if enemyFighterY[i] >= 600 and enemyFighterY[i] < 1000:
            enemyFighterY[i] = 0
            enemyFighterX[i] = random.randint(0,736)
        collision = isCollisionFighter(enemyFighterX[i], enemyFighterY[i], bulletX, bulletY)
        if collision and bullet_state == 'fire':
            enemyExplode_Sound = mixer.Sound('Explosion7.wav')
            enemyExplode_Sound.play()
            enemyDeath_Sound = mixer.Sound('WilhelmScream.wav')
            random_Scream = random.randint(0, 10)
            if random_Scream == 5:
                enemyDeath_Sound.play()
            bulletY = playerY
            bullet_state = 'ready'
            scoreValue += 1
            enemyFighterX[i] = random.randint(0, 736)
            enemyFighterY[i] = (-150)
        enemyFighter(enemyFighterX[i], enemyFighterY[i], i)
        fighterCrash = isCrashFighter(enemyFighterX[i], enemyFighterY[i], playerX, playerY)
        if fighterCrash:
            for j in range(numFighters):
                enemyFighterY[j] = 2000
            for j in range(numBombers):
                enemyBomberY[j] = 2000
            enemyExplode_Sound = mixer.Sound('Explosion7.wav')
            enemyExplode_Sound.play()
            scream_Sound = mixer.Sound('R2D2 scream.wav')
            scream_Sound.play()
            playerX, playerY = (-100,-100)
            gameOv = game_over_text(gameOverX, gameOverY)
            break

    # Bomber movement/collision
    for i in range(numBombers):
        enemyBomberX[i] += enemyBomberX_change[i]
        if enemyBomberX[i] <= 0:
            enemyBomberY[i] += enemyBomberY_change[i]
            enemyBomberX_change[i] = 0.3
        elif enemyBomberX[i] >= 736:
            enemyBomberY[i] += enemyBomberY_change[i]
            enemyBomberX_change[i] = -0.3
        elif enemyBomberY[i] >= 600 and enemyFighterY[i] < 1000:
            enemyBomberY[i] = 0
        collision = isCollisionBomber(enemyBomberX[i], enemyBomberY[i], bulletX, bulletY)
        if collision and bullet_state == 'fire':
            enemyExplode_Sound = mixer.Sound('Explosion7.wav')
            enemyExplode_Sound.play()
            enemyDeath_Sound = mixer.Sound('WilhelmScream.wav')
            random_Scream = random.randint(0,10)
            if random_Scream == 5:
                enemyDeath_Sound.play()
            bulletY = playerY
            bullet_state = 'ready'
            scoreValue += 1
            enemyBomberX[i] = random.randint(0, 736)
            enemyBomberY[i] = (-64)
        enemyBomber(enemyBomberX[i], enemyBomberY[i], i)
        bomberCrash = isCrashBomber(enemyBomberX[i], enemyBomberY[i], playerX, playerY)
        if bomberCrash:
            gameOv = True
            for j in range(numFighters):
                enemyFighterY[j] = 2000
            for j in range(numBombers):
                enemyBomberY[j] = 2000
            enemyExplode_Sound = mixer.Sound('Explosion7.wav')
            enemyExplode_Sound.play()
            scream_Sound = mixer.Sound('R2D2 scream.wav')
            scream_Sound.play()
            playerX, playerY = (-100, -100)
            break

    player(playerX, playerY)



    if gameOv:
        gameOver = over_font.render('GAME OVER', True, (255, 255, 255))
        screen.blit(gameOver, (gameOverX,gameOverY))
        bulletY = -100
        bullet_state = 'fire'
        restart = restart_font.render('Press \'R\' to Restart', True, (255, 255, 255))
        #screen.blit(restart, (250, 330))

    pygame.display.update()



