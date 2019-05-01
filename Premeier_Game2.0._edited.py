import pygame
import time
import random

pygame.init()

# GLOBAL VARIABLE SCORE
score = 0

# Game WINDOW Dimension
display_width = 500
display_height = 700

# Color Library
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
pink = (255, 105, 180)

# Initiliaizing Game Window
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Galaxy Explorers')
clock = pygame.time.Clock()

# Loading Images
rocketImgStr = 'rocketsam.png'
# rocketImgStr='ship3.png'
RocketImg = pygame.image.load('rocketsam.png')
carImg = pygame.transform.scale(RocketImg, (60, 80))
backgroundImg = pygame.image.load('backgroundoj.png')
bg1 = pygame.image.load('bg1.png')
bg2 = pygame.image.load('bg2.png')
bg3 = pygame.image.load('bg3.png')
bg = [bg1, bg2, bg3]
meteorImg = pygame.image.load('meteor.png')
bossImg = pygame.image.load('ship3.png')
townImg = pygame.image.load('questTownPic.jpg')
townShopsImg = pygame.image.load('townShops.png')


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


class Rocket():
    def __init__(self, rocketImg):
        self.Img = pygame.image.load(rocketImg)
        self.xScale = 60
        self.yScale = 80
        self.Img = pygame.transform.scale(self.Img, (60, 80))
        self.x = 230
        self.y = 581
        # ammo uesd for bullet class object
        self.ammo = 1
        self.ammoTypes = 2

    def display(self, x, y):
        gameDisplay.blit(self.Img, (x, y))

    def setImg(self, img):
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (50, 50))

    def setAmmo(self, i):
        self.ammo = i

    def swapAmmo(self):
        self.ammo = (self.ammo + i) % self.ammoTypes

    def swapAmmo(self):
        self.ammo = (self.ammo + 1) % self.ammoTypes

    def getAmmo(self):
        return self.ammo

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getXScale(self):
        return self.xScale

    def getYScale(self):
        return self.yScale

    def getWidth(self):
        return self.xScale


class Meteor():
    def __init__(self):
        self.x = random.randrange(0, display_width)
        self.y = -600
        self.speed = random.randrange(3, 15)
        self.width = 50
        self.height = 50
        self.color = (0, 0, 0)  # black
        meteorStrings = ['meteor.png', 'fireMeteor.png']
        self.Img1 = pygame.image.load(meteorStrings[random.randrange(0, 2)])
        self.Img = self.Img1
        self.xScale = 50
        self.yScale = 50
        self.Img = pygame.transform.scale(self.Img, (50, 50))

    def update(self, score):
        self.x = self.x
        self.y = self.y + self.speed
        self.width = 50 * (1 + score / 100)
        self.Img = pygame.transform.scale(self.Img1, (int(self.width), int(self.width)))
        # pygame.draw.rect(gameDisplay,self.color,[self.x,self.y,self.width,self.width])
        gameDisplay.blit(self.Img, (self.x, self.y))
        if self.y > display_height:
            self.y = 0
            self.x = random.randrange(0, display_width)
            self.speed = random.randrange(3, 5)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

    # takes in a rocket class
    def ifCrash(self, rocket):
        return ((self.x + self.width / 2) - (rocket.getX() + rocket.getXScale() / 2)) ** 2 + (
                    (self.y + self.width / 2) - (rocket.getY() + rocket.getYScale() / 2)) ** 2 < (
                           self.width / 2 + rocket.getXScale() / 2) ** 2

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y


# Bullet Type Ideas
# single fire
# multiple fire
# Timed Detonators
# heat seeking missles
# ...
class Bullet():
    def __init__(self, rocket):
        self.x = rocket.getX() + rocket.getXScale() / 2
        self.x1 = rocket.getX() + rocket.getXScale() / 2
        self.x2 = rocket.getX() + rocket.getXScale() / 2
        self.x3 = rocket.getX() + rocket.getXScale() / 2

        self.y = rocket.getY()
        self.y1 = rocket.getY() + rocket.getYScale() / 2
        self.y2 = self.y1
        self.y3 = self.y1

        self.speed = 8
        self.width = 5
        self.height = 5
        self.color = (200, 0, 200)  # black
        self.ammo = rocket.getAmmo()
        self.noCollision = True
        self.startWidth = rocket.getXScale()
        self.startHeight = rocket.getYScale()

    def update(self):
        if self.ammo == 0:
            if self.y > 0 and self.noCollision:
                self.y = self.y - self.speed
                pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.width, self.height])
        if self.ammo == 1:
            if self.y > 0 and self.noCollision:
                self.y = self.y - self.speed
                self.x1 = self.x1 - self.speed / 2
                self.x2 = self.x2 + self.speed / 2

                pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.width, self.height])
                pygame.draw.rect(gameDisplay, self.color, [self.x1, self.y, self.width, self.height])
                pygame.draw.rect(gameDisplay, self.color, [self.x2, self.y, self.width, self.height])

        if self.ammo == 2:
            # bullet with in width and height and no collision
            if (self.y > 0 and self.y < display_height and self.x > 0 and self.x < display_width) and self.noCollision:
                self.y = self.y - self.speed
                self.y1 = self.y1 + self.speed
                self.x1 = self.x1
                self.x2 = self.x2 - self.speed
                self.x3 = self.x3 + self.speed

                pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.width, self.height])
                pygame.draw.rect(gameDisplay, self.color, [self.x1, self.y1, self.width, self.height])
                pygame.draw.rect(gameDisplay, self.color, [self.x2, self.y2, self.width, self.height])
                pygame.draw.rect(gameDisplay, self.color, [self.x3, self.y3, self.width, self.height])

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

    def ifHit(self, meteor, rocket):
        meteorX = meteor.getX()
        meteorY = meteor.getY()
        meteorWidth = meteor.getWidth()
        if self.ammo == 0:
            if (self.x - meteorX - meteorWidth / 2) ** 2 + (self.y - meteorY - meteorWidth / 2) ** 2 < (
                    meteorWidth / 1.7) ** 2:
                self.noCollision = False
                return True
        if self.ammo == 1:
            if ((self.x - meteorX - meteorWidth / 2) ** 2 + (self.y - meteorY - meteorWidth / 2) ** 2 < (
                    meteorWidth / 1.7) ** 2
                    or (self.x1 - meteorX - meteorWidth / 2) ** 2 + (self.y - meteorY - meteorWidth / 2) ** 2 < (
                            meteorWidth / 1.7) ** 2
                    or (self.x2 - meteorX - meteorWidth / 2) ** 2 + (self.y - meteorY - meteorWidth / 2) ** 2 < (
                            meteorWidth / 1.7) ** 2):
                self.noCollision = False
                return True
        if self.ammo == 2:
            if ((self.x - meteorX - meteorWidth / 2) ** 2 + (self.y - meteorY - meteorWidth / 2) ** 2 < (
                    meteorWidth / 1.7) ** 2
                    or (self.x1 - meteorX - meteorWidth / 2) ** 2 + (self.y1 - meteorY - meteorWidth / 2) ** 2 < (
                            meteorWidth / 1.7) ** 2 or (self.x2 - meteorX - meteorWidth / 2) ** 2 + (
                            self.y2 - meteorY - meteorWidth / 2) ** 2 < (meteorWidth / 1.7) ** 2
                    or (self.x3 - meteorX - meteorWidth / 2) ** 2 + (self.y3 - meteorY - meteorWidth / 2) ** 2 < (
                            meteorWidth / 1.7) ** 2):
                return True

    def getNoCollision(self):
        return self.noCollision


class BossBullet():
    def __init__(self, rocket):
        self.x = rocket.getX() + rocket.getXScale() / 2
        self.x1 = rocket.getX() + rocket.getXScale() / 2
        self.x2 = rocket.getX() + rocket.getXScale() / 2
        self.y = rocket.getY()
        self.speed = 8
        self.width = 5
        self.height = 5
        self.color = (200, 0, 200)  # black
        self.ammo = rocket.getAmmo()
        self.noCollision = True

    def update(self):
        if self.ammo == 0:
            if self.y > 0 and self.noCollision:
                self.y = self.y - self.speed
                pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.width, self.height])
        if self.ammo == 1:
            if self.y > 0 and self.noCollision:
                self.y = self.y - self.speed
                self.x1 = self.x1 - self.speed / 2
                self.x2 = self.x2 + self.speed / 2

                pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.width, self.height])
                pygame.draw.rect(gameDisplay, self.color, [self.x1, self.y, self.width, self.height])
                pygame.draw.rect(gameDisplay, self.color, [self.x2, self.y, self.width, self.height])

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

    # meteor -> rocket, rocket -> boss; switch
    def ifHit(self, meteor, rocket):
        meteorX = meteor.getX()
        meteorY = meteor.getY()
        meteorWidth = meteor.getWidth()
        if rocket.ammo == 0:
            if (self.x - meteorX - meteorWidth / 2) ** 2 + (self.y - meteorY - meteorWidth / 2) ** 2 < (
                    meteorWidth / 1.7) ** 2:
                self.noCollision = False
                return True
        if rocket.ammo == 1:
            if ((self.x - meteorX - meteorWidth / 2) ** 2 + (self.y - meteorY - meteorWidth / 2) ** 2 < (
                    meteorWidth / 1.7) ** 2
                    or (self.x1 - meteorX - meteorWidth / 2) ** 2 + (self.y - meteorY - meteorWidth / 2) ** 2 < (
                            meteorWidth / 1.7) ** 2
                    or (self.x2 - meteorX - meteorWidth / 2) ** 2 + (self.y - meteorY - meteorWidth / 2) ** 2 < (
                            meteorWidth / 1.7) ** 2):
                self.noCollision = False
                return True

    def getNoCollision(self):
        return self.noCollision


class Boss():
    def __init__(self, bossImg):
        self.Img = pygame.image.load(bossImg)
        self.xScale = 150
        self.width = self.xScale
        self.yScale = 150
        self.Img1 = pygame.transform.scale(self.Img, (self.xScale, self.yScale))
        self.Img = self.Img1
        self.x = 230
        self.y = 300
        self.hp = 100
        self.speed = 3
        self.isDefeated = False
        self.bulletList = []
        self.ammo = 2

    def gotHit(self):
        self.hp = self.hp - 1
        self.xScale = 0.99 * self.xScale
        self.width = self.xScale
        self.yScale = 0.99 * self.xScale
        self.Img = pygame.transform.scale(self.Img1, (int(self.xScale), int(self.yScale)))

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWidth(self):
        return self.xScale

    def getXScale(self):
        return self.xScale

    def getYScale(self):
        return self.yScale

    def move(self):
        self.x = self.x
        self.y = self.y
        # self.x=(self.x+self.speed-2)%display_width
        # self.y=(self.y+self.speed-2)%display_height

    def getAmmo(self):
        return self.ammo

    def fire(self):
        if (len(self.bulletList) < 10):
            self.bulletList.append(Bullet(self))
        for i in range(0, len(self.bulletList)):
            self.bulletList[i].update()
            if self.bulletList[i].getY() < 0.1 or not self.bulletList[i].getNoCollision():
                self.bulletList.pop(i)
                break

        # takes in a rocket class

    def ifCrash(self, rocket):
        for j in range(0, len(self.bulletList)):
            # If bullet hits, restart meteor
            if self.bulletList[j].ifHit(rocket, self):
                return True

        return ((self.x + self.width / 2) - (rocket.getX() + rocket.getXScale() / 2)) ** 2 + (
                    (self.y + self.width / 2) - (rocket.getY() + rocket.getYScale() / 2)) ** 2 < (
                           self.width / 2 + rocket.getXScale() / 2) ** 2

    def update(self):
        # Boss Movement and Display
        # Boss HP display
        # Boss Fire
        if self.hp > 0:
            self.move()
            self.fire()
            gameDisplay.blit(self.Img, (self.x, self.y))
            text_display('I' * int(self.hp / 10), self.x + self.width / 2, self.y, 20 - int((100 - self.hp) / 10))
        if self.hp < 1:
            self.x = -100
            self.y = -500
            self.isDefeated = True

    def getIsDefeated(self):
        return self.isDefeated


def text_display(text, xCenter, yCenter, hpFont):
    largeText = pygame.font.Font('freesansbold.ttf', hpFont)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (xCenter, yCenter)
    gameDisplay.blit(TextSurf, TextRect)
# For Middle text
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (display_width / 2, display_height / 2)
    gameDisplay.blit(TextSurf, TextRect)
# for Top bar text
def score_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (display_width / 2, 10)
    gameDisplay.blit(TextSurf, TextRect)
def text_objects(text, font):
    textSurface = font.render(text, True, pink)
    return textSurface, textSurface.get_rect()
# for rocket crashes
def crash(text):
    message_display(text)
    pygame.display.update()
    time.sleep(2)
    game_loop()
def bossBattleLoop(rocket):
    x_change = 0
    y_change = 0
    bgCount = 0
    bulletList = []
    ##    bossList=[]
    ##    bossList.append(Boss())

    boss = Boss('ship3.png')

    bossExit = False

    while not bossExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -3
                elif event.key == pygame.K_RIGHT:
                    x_change = 3
                elif event.key == pygame.K_UP:
                    y_change = -3
                elif event.key == pygame.K_DOWN:
                    y_change = 3
                elif event.key == pygame.K_SPACE:
                    bulletList.append(Bullet(rocket))
                elif event.key == pygame.K_TAB:
                    rocket.swapAmmo()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
        rocket.setX((rocket.getX() + x_change))  # %display_width)
        rocket.setY((rocket.getY() + y_change) % display_height)

        # Loading Background
        gameDisplay.blit(bg[2], (0, 0))
        # gameDisplay.blit(townImg,(0,0))

        rocket.display(rocket.getX(), rocket.getY())
        # Bullet update
        for i in range(0, len(bulletList)):
            bulletList[i].update()
            # bullet is popped if bullet is offscreen or collides into an object
            if bulletList[i].getY() < 0.1 or not bulletList[i].getNoCollision():
                bulletList.pop(i)
                break
        boss.update()

        if boss.ifCrash(rocket):
            crash('GameOver, Final Score: ' + str(score))
        for j in range(0, len(bulletList)):
            if bulletList[j].ifHit(boss, rocket):
                boss.gotHit()
                boss.update()

                # Car collion on side wall
        if rocket.getX() > display_width - rocket.getXScale() or rocket.getX() < 0:
            crash('GameOver, Final Score: ' + str(score))

        score_display('Boss Score: ' + str(score))
        pygame.display.update()
        clock.tick(60)
        if boss.getIsDefeated():
            bossExit = True
def townEnterLoop(rocket):  # need an input(rocket)?
    x_change = 0
    y_change = 0
    bgCount = 0
    bulletList = []
    charImg = ''
    rocket.setImg(charImg)
    ##    bossList=[]
    ##    bossList.append(Boss())
    townShopsImg = pygame.image.load('townShops.png')
    boss = Boss('ship3.png')
    townShopsImg = pygame.transform.scale(townShopsImg, (display_width, display_height))
    townExit = False

    while not townExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -3
                elif event.key == pygame.K_RIGHT:
                    x_change = 3
                elif event.key == pygame.K_UP:
                    y_change = -3
                elif event.key == pygame.K_DOWN:
                    y_change = 3
                elif event.key == pygame.K_SPACE:
                    bulletList.append(Bullet(rocket))
                elif event.key == pygame.K_TAB:
                    rocket.swapAmmo()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
        rocket.setX((rocket.getX() + x_change))  # %display_width)
        rocket.setY((rocket.getY() + y_change) % display_height)

        # Loading Background
        # gameDisplay.blit(bg[2],(0,0))
        gameDisplay.blit(townShopsImg, (0, 0))

        rocket.display(rocket.getX(), rocket.getY())
        ##    # Bullet update
        ##    for i in range(0, len(bulletList)):
        ##        bulletList[i].update()
        ##        # bullet is popped if bullet is offscreen or collides into an object
        ##        if bulletList[i].getY() < 0.1 or not bulletList[i].getNoCollision():
        ##            bulletList.pop(i)
        ##            break
        ##    #boss.update()
        ##
        ##    if boss.ifCrash(rocket):
        ##        crash('GameOver, Final Score: ' + str(score))
        ##    for j in range(0, len(bulletList)):
        ##        if bulletList[j].ifHit(boss, rocket):
        ##            boss.gotHit()
        ##            boss.update()
        ##
        ##            # Car collion on side wall
        ##    if rocket.getX() > display_width - rocket.getXScale() or rocket.getX() < 0:
        ##        crash('GameOver, Final Score: ' + str(score))
        ##
        ##    score_display('Boss Score: ' + str(score))
        pygame.display.update()
        clock.tick(60)
# Space Travelling Asteroid Loop
def game_loop():
    x_change = 0
    y_change = 0
    bgCount = 0
    score = 0
    bossLVL = 1

    meteorList = []
    bulletList = []

    gameExit = False

    # Creating Rocket Class
    rocket = Rocket(rocketImgStr)

    # initiliazing stage Loops
    bossBattle = False
    townEnter = True
    while not gameExit:

        if bossBattle:
            bossBattleLoop(rocket)
            bossBattle = False

        if townEnter:
            townEnterLoop(rocket)
            townEnter = False

        # no boss battle case
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()

            # customize movements later by defining movement for rocket class
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -3
                elif event.key == pygame.K_RIGHT:
                    x_change = 3
                elif event.key == pygame.K_UP:
                    y_change = -3
                elif event.key == pygame.K_DOWN:
                    y_change = 3
                elif event.key == pygame.K_SPACE:
                    bulletList.append(Bullet(rocket))
                elif event.key == pygame.K_TAB:
                    rocket.swapAmmo()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
        rocket.setX((rocket.getX() + x_change))  # %display_width)
        rocket.setY((rocket.getY() + y_change) % display_height)

        # Loading Background
        # gameDisplay.fill(white)
        bgCount = (bgCount + 1) % 60
        # gameDisplay.blit(backgroundImg,(0,0))
        # gameDisplay.blit(bg[int(bgCount/20)],(0,0))
        gameDisplay.blit(bg[2], (0, 0))

        rocket.display(rocket.getX(), rocket.getY())
        # Bullet update
        for i in range(0, len(bulletList)):
            bulletList[i].update()
            if bulletList[i].getY() < 0.1 or not bulletList[i].getNoCollision():
                bulletList.pop(i)
                break

        # New block every 15 max 10 blocks
        if len(meteorList) <= score / 15 and len(meteorList) < 10:
            meteorList.append(Meteor())
        for i in range(0, len(meteorList)):
            meteorList[i].update(score)

        for i in range(0, len(meteorList)):
            if meteorList[i].getY() == 0:
                score = score + 1

        # Collision detection, create a loop for more meteors
        for i in range(0, len(meteorList)):
            if meteorList[i].ifCrash(rocket):
                crash('GameOver, Final Score: ' + str(score))
                score = 0
            for j in range(0, len(bulletList)):
                # If bullet hits, restart meteor
                if bulletList[j].ifHit(meteorList[i], rocket):
                    meteorList[i] = Meteor()
                    score = score + 3
        # How often the boss comes
        if score > (bossLVL + 25) ** 2 - 25 ** 2:
            bossLVL = bossLVL + 1
            bossBattle = True
        # Car collion on side wall
        if rocket.getX() > display_width - rocket.getXScale() or rocket.getX() < 0:
            crash('GameOver, Final Score: ' + str(score))

        score_display('Score: ' + str(score))
        pygame.display.update()
        clock.tick(60)
# Planetary T
def game_loop2():
    pass


# loop 1 uncompleto
game_loop()
# loop 2 commencemento

