import pygame
import time
import random
import numpy as np
import argparse
import cv2
import pickle

pygame.init()



#GLOBAL VARIABLE SCORE
score=0

#Game WINDOW Dimension
display_width=700
display_height=700

#Color Library
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
pink=(255,105,180)

#Initiliaizing Game Window
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Galaxy Explorers')
clock=pygame.time.Clock()

#Loading Images
##rocketImgStr='testSprite.png'
###rocketImgStr='invis_upMove.png'
###rocketImgStr='ship3.png'
##RocketImg=pygame.image.load('rocketsam.png')
##gameDisplay.blit(RocketImg,(0,0))
##pygame.display.update()
##image = cv2.imread(rocketImgStr)
##cv2.imwrite('spriteWriteTest.png',image[0:65,0:65])
##testSprite2 = cv2.imread('testSprite.png', cv2.IMREAD_UNCHANGED)
##testSprite=cv2.imread('spriteWriteTest.png')
###cv2.imshow('',testSprite)
##cv2.imshow('',testSprite2)
##cv2.imwrite('spriteWriteTest1.png',image[0:65,0:65])
spriteImg = pygame.image.load('testSprite.png')
#spriteImg = pygame.image.load('testSprite.png')

gameDisplay.blit(spriteImg,(0,0),(65,65,65,65))
#pygame.image.save()
pygame.display.update()
