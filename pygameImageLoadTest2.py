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
gameDisplay2 = pygame.display.set_mode((display_width,display_height))

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
#spriteImg = pygame.image.load('testSprite.png').convert_alpha()
spriteImg = pygame.image.load('testSprite.png')
spriteImg2=pygame.image.load('redEffect.png')
x1=205
x2=242
y1=65
yWidth=63
xList=[[14,52],[81,116],[141,181],[205,244]]
yList=[130,193]
crop_rect=(x1,y1,x2-x1,yWidth)
cropped=spriteImg.subsurface(crop_rect)
croppedStr="cropped"+str(8)+".png"
crop_rect=(205,65,244-205,yWidth)
cropped=spriteImg.subsurface(crop_rect)

pygame.image.save(cropped,croppedStr)
startNum=9
for v in yList:
    for u in xList:
        croppedStr="cropped"+str(startNum)+".png"
        crop_rect=(u[0],v,u[1]-u[0],yWidth)
        cropped=spriteImg.subsurface(crop_rect)
        
        pygame.image.save(cropped,croppedStr)
        startNum+=1

yNum=0
holdImgDict={1:[]}
for i in range(16):
    croppedStr="cropped"+str(i+1)+".png"
    spriteImg = pygame.image.load(croppedStr)
    holdImgDict[1].append(spriteImg)
    #gameDisplay2.blit(spriteImg,(65*i%(65*8),yNum))
    if(i==7):
        yNum=100
#pygame.image.save()
yNum=0
loopRun=True
while(loopRun):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            loopRun=False
    for i in range(16):
        gameDisplay.blit(holdImgDict[1][i],(65*i%(65*8),yNum))
        #gameDisplay2.blit(holdImgDict[1][i],(65*i%(65*8),yNum))

        if(i==7):
            yNum=100
    pygame.display.update()
pygame.quit()
