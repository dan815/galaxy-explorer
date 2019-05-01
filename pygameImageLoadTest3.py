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
spriteImg = pygame.image.load('redEffect.png')
x1 = 205
x2 = 242
y1 = 65
yWidth = 85
320,385,460,540
#change x and y
xList = [[0, 61], [61, 118], [118, 184], [184, 246], [246, 320], [320, 385], [385, 460], [460, 540]]
yList = [0]
startNum = 0
for v in yList:
    for u in xList:
        croppedStr = "croppedRed" + str(startNum) + ".png"
        crop_rect = (u[0], v, u[1] - u[0], yWidth)
        cropped = spriteImg.subsurface(crop_rect)
        pygame.image.save(cropped, croppedStr)
        startNum += 1
yNum = 0
for i in range(len(xList)):
    croppedStr = "croppedRed" + str(i) + ".png"
    spriteImg = pygame.image.load(croppedStr)
    gameDisplay2.blit(spriteImg, (70 * i % (70 * 7), yNum))
    if (i == 7):
        yNum = 100
# pygame.image.save()
pygame.display.update()
