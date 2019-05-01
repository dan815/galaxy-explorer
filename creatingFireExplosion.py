import pygame
import time
import random
import numpy as np
import argparse
import cv2
import pickle

pygame.init()
display_width = 700
display_height = 700
# Initiliaizing Game Window
gameDisplay2 = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Galaxy Explorers')
clock = pygame.time.Clock()
spriteImg = pygame.image.load('slimeMonster.png')
x1 = 205
x2 = 242
y1 = 65
yWidth = 850/4
#change x and y
xList = [[i*1700/8,(i+1)*1700/8] for i in range(8)]
yList = [k*850/4 for k in range(4)]
startNum = 0
for v in yList:
    for u in xList:
        croppedStr = "croppedSlimeMonster" + str(startNum) + ".png"
        crop_rect = (u[0], v, u[1] - u[0], yWidth)
        cropped = spriteImg.subsurface(crop_rect)
        pygame.image.save(cropped, croppedStr)
        startNum += 1

# count=0
# for u in xList:
#     yInd=int(count/5)
#     croppedStr = "croppedHado" + str(startNum) + ".png"
#     crop_rect = (u[0], yList[yInd], u[1] - u[0], yWidth)
#     cropped = spriteImg.subsurface(crop_rect)
#     pygame.image.save(cropped, croppedStr)
#     startNum += 1
showPics=True
while(showPics):
    yNum = 0
    for i in range(len(xList)*len(yList)):
        croppedStr = "croppedSlimeMonster" + str(i) + ".png"
        spriteImg = pygame.image.load(croppedStr)
        gameDisplay2.blit(spriteImg, (180 * i % (180 * 3), yNum))
        if (i == 3):
            yNum = 250
    # for i in range(len(xList)):
    #     croppedStr = "croppedHado" + str(i) + ".png"
    #     spriteImg = pygame.image.load(croppedStr)
    #     gameDisplay2.blit(spriteImg, (180 * i % (180 * 3), yNum))
    #     if (i == 3):
    #         yNum = 250
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # save_obj(rocket,'myRocket')
            # np.save('my_rocket.npy', rocket)
            showPics = False

pygame.display.update()
pygame.quit()
