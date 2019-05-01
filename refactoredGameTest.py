import pygame
import time
import random
import numpy as np
import argparse
import cv2
import pickle
import math


#----------------------DECLARING GLOBAL VARIABLES AND OBJECTS----------------------
score=0
display_width=700
display_height=700
#Color Library
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
pink=(255,105,180)
#Loading Images
rocketImgStr='rocketsam.png'
RocketImg=pygame.image.load('rocketsam.png')
carImg=pygame.transform.scale(RocketImg,(60,80))
backgroundImg=pygame.image.load('backgroundoj.png')
bg1=pygame.image.load('bg1.png')
bg2=pygame.image.load('bg2.png')
bg3=pygame.image.load('bg3.png')
bg4=pygame.image.load('bg4.png')
bg=[bg1,bg2,bg3]
meteorImg=pygame.image.load('meteor.png')
fireMeteorImg=pygame.image.load('fireMeteor.png')
bossImg=pygame.image.load('ship3.png')
townImg=pygame.image.load('questTownPic.jpg')
townShopsImg=pygame.image.load('townShops.png')
shopInside1=pygame.image.load('shopInsideRescale.png')
library=pygame.image.load('library.png')
#imgs for INVENTORY
emptyInventoryImg=pygame.image.load('emptyInventory3.png')
emptyInventoryImg=pygame.transform.scale(emptyInventoryImg,(200,200))
testItem1Img=pygame.transform.scale(meteorImg,(40,40))
testItem2Img=pygame.transform.scale(fireMeteorImg,(40,40))
testItem3Img=pygame.transform.scale(bossImg,(40,40))
skillBarTestImg1=pygame.image.load('croppedRed3.png')
skillTestImg1=pygame.transform.scale(skillBarTestImg1,(40,40))
skillBarTestImg1=pygame.transform.scale(skillBarTestImg1,(25,25))
skillBarTestItem1=pygame.transform.scale(skillBarTestImg1,(25,25))
skillBarTestItem2=pygame.transform.scale(testItem2Img,(25,25))
skillBarTestItem3=pygame.transform.scale(testItem3Img,(25,25))

itemLine=pygame.transform.scale(bg4,(50,50))#'animation' below the item
#img for SKILL LIST
skillListImg=pygame.image.load('emptyInventory3.png')
skillListImg=pygame.transform.scale(skillListImg,(200,200))
skillBarImg=pygame.image.load('emptySkillBarImg1.png')
skillBarImg=pygame.transform.scale(skillBarImg,(283,43))

#Item Dictionary Data
itemDict={'testItem1':[testItem1Img],'testItem2':[testItem2Img],'testItem3':[testItem3Img]}
itemLocationDict={'testItem1':[(650,480),True],'testItem2':[(650,550),True]}
#respawnTimer for item respawns
respawnTimer=25
#Skill Dictionary Data
skillDict={'testItem1':[skillTestImg1],'testItem2':[testItem2Img],'testItem3':[testItem3Img]}
skillBarDict={'testItem1':[skillBarTestItem1],'testItem2':[skillBarTestItem2],'testItem3':[skillBarTestItem3]}
#SKILL ANIMATION TEST
skillAni0=pygame.image.load('croppedRed0.png')
skillAni0=pygame.transform.scale(skillAni0,(60,85))
skillAni1=pygame.image.load('croppedRed1.png')
skillAni1=pygame.transform.scale(skillAni1,(60,85))
skillAni2=pygame.image.load('croppedRed2.png')
skillAni2=pygame.transform.scale(skillAni2,(60,85))
skillAni3=pygame.image.load('croppedRed3.png')
skillAni3=pygame.transform.scale(skillAni3,(60,85))
skillAni4=pygame.image.load('croppedRed4.png')
skillAni4=pygame.transform.scale(skillAni4,(60,85))
skillAni5=pygame.image.load('croppedRed5.png')
skillAni5=pygame.transform.scale(skillAni5,(60,85))
skillAni6=pygame.image.load('croppedRed6.png')
skillAni6=pygame.transform.scale(skillAni6,(60,85))
skillAni7=pygame.image.load('croppedRed7.png')
skillAni7=pygame.transform.scale(skillAni7,(60,85))
#To store the picture scale and the command for pygame surface width and height
skillAniWidth = skillAni7.get_width()
skillAniHeight = skillAni7.get_height()
#skillUseDict={key:[frameIndex,[framePygameSurface List],[x and y dimension of image list],[coolDown]]}
skillCoolDown1=0# 3 sec cool down
skillCoolDown2=1
skillUseDict={1:[0,[skillAni0,skillAni1,skillAni2,skillAni3,skillAni4,skillAni5,skillAni6,skillAni7],
                 [(skillAniWidth,skillAniHeight),(60,85),(60,85),(60,85),(60,85),(60,85),(60,85),(60,85)],
                 [skillCoolDown1]],2:[0,[],[],[skillCoolDown1]],3:[0,[],[],[skillCoolDown1]]}
skillProjUseDict={1:[0,[],[],[skillCoolDown2]],2:[0,[],[],[skillCoolDown1]],3:[0,[],[],[skillCoolDown2]]}


#-------adding skill animation----------------
for i in range(12):
    j=i%6
    width=int(100/1.3*(i/12+1))
    height=int(120/1.3*(i/12+1))
    skillUseDict[2][1].append(pygame.transform.scale(pygame.image.load('croppedFireExplosion'+str(j)+'.png'),(width,height)))
    skillUseDict[2][2].append((width,height))

for i in range(16):
    j=i%8
    width=int((201-43)/2.5)
    height=int((283-97)/2.5)
    skillProjUseDict[1][1].append(pygame.transform.scale(pygame.image.load('croppedHado'+str(j)+'.png'),(width,height)))
    skillProjUseDict[1][2].append((width,height))

for i in range(32):
    j=i%32
    width=75
    height=75
    skillProjUseDict[2][1].append(pygame.transform.scale(pygame.image.load('croppedSlimeMonster'+str(j)+'.png'),(width,height)))
    skillProjUseDict[2][2].append((width,height))
#------end of adding skill animations-----------
#Monster Animation Dictionary
monsterHP=5
monsterAnimationDict={1:[0,[],[],[monsterHP]]}

#--------adding monster animations-----------
for i in range(32):
    j=i%32
    width=75
    height=75
    monsterAnimationDict[1][1].append(pygame.transform.scale(pygame.image.load('croppedSlimeMonster'+str(j)+'.png'),(width,height)))
    monsterAnimationDict[1][2].append((width,height))
#------end of adding monster animations-----------
class Monster():
    def __init__(self, pos,monsterType):#monsterType is just an Integer for now
        self.x = pos[0]
        self.y = pos[1]
        self.monsterType=monsterType
        self.animationCounter=random.randint(0,31)
        self.img = monsterAnimationDict[monsterType][1][self.animationCounter]#initialized to 1st frame of animation
        self.animationFrameRepeat=1
        self.repeatCount=4
        #gameDisplay.blit(self.img, (self.x, self.y))
    def update(self,mapPos):
        if(self.x>=-mapPos[0] and self.x<=-mapPos[0]+display_width and self.y>=-mapPos[1] and self.y<=-mapPos[1]+display_height):
            if(self.animationFrameRepeat%self.repeatCount==0):
                self.animationCounter=(self.animationCounter+1)%32
            self.img = monsterAnimationDict[self.monsterType][1][self.animationCounter]
            self.animationFrameRepeat = (self.animationFrameRepeat + 1) % self.repeatCount
            gameDisplay.blit(self.img, (self.x+mapPos[0], self.y+mapPos[1]))
    def getPos(self):
        return (self.x,self.y)


#include monster Type, monster Location
monsterPlacesDict={1:[Monster((350,400),1),1],2:[Monster((150,50),1),1],3:[Monster((800,490),1),1],4:[Monster((1000,500),1),1],5:[Monster((540,540),1),1]}



#stageDict={stageNumber:[stageImg,(stageWidth,stageHeight), stageDictFileName, stageItemLocations,[rocketX,rocketY],[mapX,MapY]]}
stageDict={1:[townShopsImg,(2000,2000),'map1',itemLocationDict,[410,350],[0,0]],
           2:[shopInside1,(700,700),'map2',{},[350,650],[0,0]],
           3:[library,(1087,734),'map3',{},[510,657],[0,0]]}#do item locations same as stageDictFileName later

#-------------------------------END OF DECLARING GLOBAL VARIABLES AND OBJECTS--------------------------------------

def monsterUpdater(monsterPlacesDict,mapPos):#draws moster relative to players location
    for k in monsterPlacesDict.keys():
        monsterPlacesDict[k][0].update(mapPos)

class ItemData():
    #itemDict={'itemName':[itemImg,itemStats,...]}
    def img(self,item):
        return itemDict[item][0]
class skillData():
    def img(self,item):
        return skillDict[item][0]#returns the img associated to skill string
class skillBarData():
    def img(self,item):
        return skillBarDict[item][0]#returns the img associated to skill string
class Skills():
    def __init__(self):
        self.skillListImg=skillListImg
        self.skillBarImg=skillBarImg
        self.skillList=[]#if this is left empty, it still takes the skillList of parent or subclass I think...
        self.skillBarList=[]
        self.skillBarLocationX=200
        self.skillBarLocationY=657
        self.offsetX=display_width-200
        self.offsetY=display_height-200
        self.skillSlotXY = [(12, 10), (60, 10), (106, 10), (153, 10), (12, 58), (60, 58), (106, 58), (153, 58), (12, 104),
                       (60, 104), (106, 104), (153, 104), (12, 152), (60, 152), (106, 152), (153, 152)]
        self.skillBarSlotXY=[(10,10),(40,10),(70,10),(100,10),(130,10),(160,10),(190,10),(220,10),(250,10)]
        self.skillBarSlotXY=[(u[0]+self.skillBarLocationX,u[1]+self.skillBarLocationY) for u in self.skillBarSlotXY]
        self.skillSlotXY=[(u[0],u[1]+self.offsetY) for u in self.skillSlotXY]
        self.skillSlot=0
        self.skillFrameRepeat=5
        self.skillFrameInit=0
        self.inputSkillNumber=0
        self.inputProjSkillNumber = 0
        self.coolDownTimer=0
        self.useProjSkillEndBool=False
        self.projFrame=0
        self.projGlobalPosXY={1:[]}
    def displaySkills(self):
        gameDisplay.blit(self.skillListImg,(0,self.offsetY))
        slotInd=0
        for skillStr in self.skillList:
            #displays skill at specified slot ind
           gameDisplay.blit(skillData().img(skillStr),(self.skillSlotXY[slotInd][0],self.skillSlotXY[slotInd][1]))
           slotInd+=1
    def displaySkillBar(self):
        gameDisplay.blit(self.skillBarImg,(self.skillBarLocationX,self.skillBarLocationY))
        #find a new solution to this, the image with the skills should be stored
        #as it could be inefficient to recall blit function so many times
        slotInd=0
        for skillStr in self.skillBarList:
            gameDisplay.blit(skillBarData().img(skillStr), (self.skillBarSlotXY[slotInd][0],
                                                            self.skillBarSlotXY[slotInd][1]))
            slotInd += 1
    def useSkill(self,input):
        #show skill animation
        #determine # of frames skill is effective for
        #skillUseDict[input]=[image1,image2,image3,...,frame]
        #1:[currentFrame,[image1,image2,image3,..]]
        self.inputSkillNumber=input
        frameVal = skillUseDict[input][0]
        # blits the image in the dictionary corresponding to the currentFrame and centers the image around rocket
        gameDisplay.blit(skillUseDict[input][1][frameVal],(self.getX()-int(skillUseDict[input][2][frameVal][0]/2),
                                                           self.getY()-int(skillUseDict[input][2][frameVal][1]/2)))
        #moves to next frame
        self.skillFrameInit=(self.skillFrameInit+1)%self.skillFrameRepeat
        #Updates to next frame count after enough repettion of that frame
        if self.skillFrameInit%self.skillFrameRepeat==0:
            skillUseDict[input][0]=(skillUseDict[input][0]+1)%len(skillUseDict[input][1])
            # skillUseDict={key:[frameIndex,[framePygameSurface List],[x and y dimension of image list]]}

    def useSkillEnd(self):
        #u can figure out a way to make this a global check for all the skill animations firing atm
        if((self.skillFrameInit+1) * (skillUseDict[self.inputSkillNumber][0]+1)
                ==self.skillFrameRepeat*len(skillUseDict[self.inputSkillNumber][1])):
            return True
        else:
            return False
    def setProjectileMotionDict(self,startMapXY,startXYPixel,endMousePos):
        mapX=startMapXY[0]

        mapY=startMapXY[1]
        startPixelX=startXYPixel[0]
        startPixelY = startXYPixel[1]
        endPixelX=endMousePos[0]
        endPixelY = endMousePos[1]
        n=150#number of frames
        self.projGlobalPosXY[1]=[[0],[[-mapX+startPixelX+(endPixelX-startPixelX)*k/n,-mapY+startPixelY+(endPixelY-startPixelY)*k/n] for k in range(n+1)]]

    def useProjectileSkill(self,input,currentMapXY,rotDeg):
        #print(self.Gxy[1])
        xPos=self.projGlobalPosXY[1][1][self.projGlobalPosXY[1][0][0]][0]+currentMapXY[0]
        yPos = self.projGlobalPosXY[1][1][self.projGlobalPosXY[1][0][0]][1] + currentMapXY[1]
        #print(xPos,yPos)
       # print(xPos+currentMapXY[0])
        n=150
        self.projFrame=(self.projFrame+1)%n
        if(self.projFrame==n-1):
            self.useProjSkillEndBool=True

        frameVal = skillProjUseDict[input][0]
        #BAD WAY YOU NEED TO GENERATE A COMPLETE LIST FOR THE PROJECTILE TO FOLLOW
        gameDisplay.blit(pygame.transform.rotate(skillProjUseDict[input][1][frameVal],rotDeg),(xPos-int(skillProjUseDict[input][2][frameVal][0]/2),yPos-int(skillProjUseDict[input][2][frameVal][1]/2)))
        self.projGlobalPosXY[1][0][0]=self.projGlobalPosXY[1][0][0]+1#updating to next global pos of projectile
        #moves to next frame
        self.skillFrameInit=(self.skillFrameInit+1)%self.skillFrameRepeat
        #Updates to next frame count after enough repettion of that frame
        if self.skillFrameInit%self.skillFrameRepeat==0:
            skillProjUseDict[input][0]=(skillProjUseDict[input][0]+1)%len(skillProjUseDict[input][1])
            # skillUseDict={key:[frameIndex,[framePygameSurface List],[x and y dimension of image list]]}
        # if(((self.Gxy[1][1][-1][0]-xPos)**2 +(self.Gxy[1][1][-1][1]-yPos)**2)**0.5<50 or xPos<-200 or xPos>900 or yPos<-200 or yPos>900):
        #     self.useProjSkillEndBool=True
        #     self.totalChangeX=0
        #     self.totalChangeY = 0

    def useProjSkillEnd(self):
        #u can figure out a way to make this a global check for all the skill animations firing atm
        if(self.useProjSkillEndBool):
            self.useProjSkillEndBool=False
            return True
        else:
            return self.useProjSkillEndBool

    def getCoolDownTimer(self):
        return self.coolDownTimer
    def setCoolDownTimer(self,currentTime):
        self.coolDownTimer=currentTime
    def addSkill(self):
        pass
    def delSkill(self):
        pass
    def updateSkill(self):
        pass
class Inventory():
    def __init__(self):
       self.img=emptyInventoryImg
       self.itemList=[]
       self.itemSlot=0
       #self.slotXY= location of top left corner of every slot space
       self.slotXY=[(12,10),(60,10),(106,10),(153,10),(12,58),(60,58),(106,58),(153,58),
                    (12,104),(60,104),(106,104),(153,104),(12,152),(60,152),(106,152),(153,152)]
    def displayInventory(self):
        gameDisplay.blit(self.img,(0,0))
        slotInd=0
        for i in self.itemList:
           gameDisplay.blit(ItemData().img(i),(self.slotXY[slotInd][0],self.slotXY[slotInd][1]))
           slotInd+=1
    def addItem(self,item):
        if(len(self.itemList)<16):
            self.itemList.append(item)
            self.itemSlot+=1
    def delItem(self,index):
        if(len(self.itemList)>0):
            self.itemList.pop(index)
            self.itemSlot-=1
    def popItem(self):
        if(len(self.itemList)>0):
            self.itemList.pop()
            self.itemSlot-=1
class stage():
    #currently for every time a stage is being initialized its reloading the stage
    #possible alternatives include having preloaded stage map objs to work with
    def __init__(self,rocket):
        self.stageNum=rocket.getStage()
        self.stageImg=stageDict[self.stageNum][0]
        self.stageWidth=stageDict[self.stageNum][1][0]
        self.stageHeight=stageDict[self.stageNum][1][1]
        self.stageMapDict=load_obj(stageDict[self.stageNum][2])
        self.stageItemLocationsDict=stageDict[self.stageNum][3]

    def getStageNum(self):
        return self.stageNum
    def getStageImg(self):
        return self.stageImg
    def getStageWidth(self):
        return self.stageWidth
    def getStageHeight(self):
        return self.stageHeight
    def getStageMapDict(self):
        return self.stageMapDict
    def getStageItemLocationsDict(self):
        return self.stageItemLocationsDict
class Rocket(Inventory,Skills):
    def __init__(self,rocketImg):
        Inventory.__init__(self)
        Skills.__init__(self)
        self.Img=pygame.image.load(rocketImg)
        self.xScale=60
        self.yScale=80
        self.Img=pygame.transform.scale(self.Img,(60,80))
        self.x = 250
        self.y = 490
        self.itemList=['testItem1','testItem2','testItem3','testItem3']
        self.skillList = ['testItem1', 'testItem2', 'testItem2', 'testItem1']
        self.skillBarList = ['testItem1', 'testItem2', 'testItem2', 'testItem1','testItem2','testItem2','testItem2','testItem2','testItem2']
        #ammo uesd for bullet class object
        self.ammo=1
        self.ammoTypes=2
        self.stage=1
    def setStage(self,stageNum):
        self.stage=stageNum
    def getStage(self):
        return self.stage
    def display(self):
        x=int(self.x - self.xScale/2)
        y=int(self.y - self.yScale*0.8)
        gameDisplay.blit(self.Img,(x,y))
    def setImg(self,img):
        scaleSize=33
        self.Img=pygame.image.load(img)
        self.Img=pygame.transform.scale(self.Img,(scaleSize,int(1.6*scaleSize)))
        self.xScale=scaleSize
        self.yScale=1.5*scaleSize
    def setAmmo(self,i):
        self.ammo=i
    def swapAmmo(self):
        self.ammo=(self.ammo+i)%self.ammoTypes
    def swapAmmo(self):
        self.ammo=(self.ammo+1)%self.ammoTypes
    def getAmmo(self):
        return self.ammo
    def setX(self,x):
        self.x=x
    def setY(self,y):
        self.y=y
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
        self.x=random.randrange(0,display_width)
        self.y=-600
        self.speed=random.randrange(3,15)
        self.width=50
        self.height=50
        self.color=(0,0,0)#black
        meteorStrings=['meteor.png','fireMeteor.png']
        self.Img1=pygame.image.load(meteorStrings[random.randrange(0,2)])
        self.Img=self.Img1
        self.xScale=50
        self.yScale=50
        self.Img=pygame.transform.scale(self.Img,(50,50))
    def update(self,score):
        self.x=self.x
        self.y=self.y + self.speed
        self.width=50*(1+score/100)
        self.Img=pygame.transform.scale(self.Img1,(int(self.width),int(self.width)))
        #pygame.draw.rect(gameDisplay,self.color,[self.x,self.y,self.width,self.width])
        gameDisplay.blit(self.Img,(self.x,self.y))
        if self.y > display_height:
            self.y=0
            self.x=random.randrange(0,display_width)
            self.speed=random.randrange(3,5)
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getWidth(self):
        return self.width
    #takes in a rocket class
    def ifCrash(self,rocket):
        return ((self.x+self.width/2)-(rocket.getX()+rocket.getXScale()/2))**2 +((self.y+self.width/2)-(rocket.getY()+rocket.getYScale()/2))**2<(self.width/2+rocket.getXScale()/2)**2
    def setX(self,x):
        self.x=x
    def setY(self,y):
        self.y=y
class Bullet():
    # Bullet Type Ideas#single fire#multiple fire#Timed Detonators#heat seeking missles
    def __init__(self,rocket):
        self.x=rocket.getX()+rocket.getXScale()/2
        self.x1=rocket.getX()+rocket.getXScale()/2
        self.x2=rocket.getX()+rocket.getXScale()/2
        self.x3=rocket.getX()+rocket.getXScale()/2
        self.y=rocket.getY()
        self.y1=rocket.getY()+rocket.getYScale()/2
        self.y2=self.y1
        self.y3=self.y1
        self.speed=8
        self.width=5
        self.height=5
        self.color=(200,0,200)#black
        self.ammo=rocket.getAmmo()
        self.noCollision = True
        self.startWidth=rocket.getXScale()
        self.startHeight=rocket.getYScale()
    def update(self):
        if self.ammo==0:
            if self.y>0 and self.noCollision:
                self.y=self.y-self.speed
                pygame.draw.rect(gameDisplay,self.color,[self.x,self.y,self.width,self.height])
        if self.ammo==1:
            if self.y>0 and self.noCollision:
                self.y=self.y-self.speed
                self.x1=self.x1-self.speed/2
                self.x2=self.x2+self.speed/2
                pygame.draw.rect(gameDisplay,self.color,[self.x,self.y,self.width,self.height])
                pygame.draw.rect(gameDisplay,self.color,[self.x1,self.y,self.width,self.height])
                pygame.draw.rect(gameDisplay,self.color,[self.x2,self.y,self.width,self.height])
        if self.ammo==2:
            #bullet with in width and height and no collision
            if (self.y>0 and self.y<display_height and self.x>0 and self.x<display_width) and self.noCollision:
                self.y=self.y-self.speed
                self.y1=self.y1+self.speed
                self.x1=self.x1
                self.x2=self.x2-self.speed
                self.x3=self.x3+self.speed
                pygame.draw.rect(gameDisplay,self.color,[self.x,self.y,self.width,self.height])
                pygame.draw.rect(gameDisplay,self.color,[self.x1,self.y1,self.width,self.height])
                pygame.draw.rect(gameDisplay,self.color,[self.x2,self.y2,self.width,self.height])
                pygame.draw.rect(gameDisplay,self.color,[self.x3,self.y3,self.width,self.height])
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getWidth(self):
        return self.width
    def ifHit(self,meteor,rocket):
        meteorX=meteor.getX()
        meteorY=meteor.getY()
        meteorWidth=meteor.getWidth()
        if self.ammo==0:
            if (self.x-meteorX-meteorWidth/2)**2+(self.y-meteorY-meteorWidth/2)**2<(meteorWidth/1.7)**2:
                self.noCollision=False
                return True
        if self.ammo==1:
            if ((self.x-meteorX-meteorWidth/2)**2+(self.y-meteorY-meteorWidth/2)**2<(meteorWidth/1.7)**2
                    or(self.x1-meteorX-meteorWidth/2)**2+(self.y-meteorY-meteorWidth/2)**2<(meteorWidth/1.7)**2
                    or(self.x2-meteorX-meteorWidth/2)**2+(self.y-meteorY-meteorWidth/2)**2<(meteorWidth/1.7)**2):
                self.noCollision=False
                return True
        if self.ammo==2:
            if ((self.x-meteorX-meteorWidth/2)**2+(self.y-meteorY-meteorWidth/2)**2<(meteorWidth/1.7)**2
                    or(self.x1-meteorX-meteorWidth/2)**2+(self.y1-meteorY-meteorWidth/2)**2<(meteorWidth/1.7)**2 or(self.x2-meteorX-meteorWidth/2)**2+(self.y2-meteorY-meteorWidth/2)**2<(meteorWidth/1.7)**2
                    or(self.x3-meteorX-meteorWidth/2)**2+(self.y3-meteorY-meteorWidth/2)**2<(meteorWidth/1.7)**2):
                return True
    def getNoCollision(self):
        return self.noCollision
class BossBullet():
    def __init__(self,rocket):
        self.x=rocket.getX()+rocket.getXScale()/2
        self.x1=rocket.getX()+rocket.getXScale()/2
        self.x2=rocket.getX()+rocket.getXScale()/2
        self.y=rocket.getY()
        self.speed=8
        self.width=5
        self.height=5
        self.color=(200,0,200)#black
        self.ammo=rocket.getAmmo()
        self.noCollision = True
    def update(self):
        if self.ammo==0:
            if self.y>0 and self.noCollision:
                self.y=self.y-self.speed
                pygame.draw.rect(gameDisplay,self.color,[self.x,self.y,self.width,self.height])
        if self.ammo==1:
            if self.y>0 and self.noCollision:
                self.y=self.y-self.speed
                self.x1=self.x1-self.speed/2
                self.x2=self.x2+self.speed/2
                pygame.draw.rect(gameDisplay,self.color,[self.x,self.y,self.width,self.height])
                pygame.draw.rect(gameDisplay,self.color,[self.x1,self.y,self.width,self.height])
                pygame.draw.rect(gameDisplay,self.color,[self.x2,self.y,self.width,self.height])
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getWidth(self):
        return self.width
    #meteor -> rocket, rocket -> boss; switch
    def ifHit(self,meteor,rocket):
        meteorX=meteor.getX()
        meteorY=meteor.getY()
        meteorWidth=meteor.getWidth()
        if rocket.ammo==0:
            if (self.x-meteorX-meteorWidth/2)**2+(self.y-meteorY-meteorWidth/2)**2<(meteorWidth/1.7)**2:
                self.noCollision=False
                return True
        if rocket.ammo==1:
            if ((self.x-meteorX-meteorWidth/2)**2+(self.y-meteorY-meteorWidth/2)**2<(meteorWidth/1.7)**2
                    or(self.x1-meteorX-meteorWidth/2)**2+(self.y-meteorY-meteorWidth/2)**2<(meteorWidth/1.7)**2
                    or(self.x2-meteorX-meteorWidth/2)**2+(self.y-meteorY-meteorWidth/2)**2<(meteorWidth/1.7)**2):
                self.noCollision=False
                return True
    def getNoCollision(self):
        return self.noCollision
class Boss():
    def __init__(self,bossImg):
        self.Img=pygame.image.load(bossImg)
        self.xScale=150
        self.width=self.xScale
        self.yScale=150
        self.Img1=pygame.transform.scale(self.Img,(self.xScale,self.yScale))
        self.Img=self.Img1
        self.x = 230
        self.y =300
        self.hp= 100
        self.speed=3
        self.isDefeated=False
        self.bulletList=[]
        self.ammo=2
    def gotHit(self):
        self.hp=self.hp-1
        self.xScale=0.99*self.xScale
        self.width=self.xScale
        self.yScale=0.99*self.xScale
        self.Img=pygame.transform.scale(self.Img1,(int(self.xScale),int(self.yScale)))
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
        self.x=self.x
        self.y=self.y
        #self.x=(self.x+self.speed-2)%display_width
        #self.y=(self.y+self.speed-2)%display_height
    def getAmmo(self):
        return self.ammo
    def fire(self):
        if(len(self.bulletList)<10):
            self.bulletList.append(Bullet(self))
        for i in range(0,len(self.bulletList)):
            self.bulletList[i].update()
            if self.bulletList[i].getY()<0.1 or not self.bulletList[i].getNoCollision():
                self.bulletList.pop(i)
                break
    def ifCrash(self,rocket):
        for j in range(0,len(self.bulletList)):
                #If bullet hits, restart meteor
            if self.bulletList[j].ifHit(rocket,self):
                return True
        return ((self.x+self.width/2)-(rocket.getX()+rocket.getXScale()/2))**2 +\
               ((self.y+self.width/2)-(rocket.getY()+rocket.getYScale()/2))**2<(self.width/2+rocket.getXScale()/2)**2
    def update(self):
        #Boss Movement and Display
        #Boss HP display
        #Boss Fire
        if self.hp>0:
            self.move()
            self.fire()
            gameDisplay.blit(self.Img,(self.x,self.y))
            textDisplay().text_display('I'*int(self.hp/10),self.x+self.width/2,self.y,20-int((100-self.hp)/10))
        if self.hp<1:
            self.x=-100
            self.y=-500
            self.isDefeated=True
    def getIsDefeated(self):
        return self.isDefeated
class textDisplay():
    def text_display(self,text, xCenter, yCenter, hpFont):
        largeText = pygame.font.Font('freesansbold.ttf', hpFont)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = (xCenter, yCenter)
        gameDisplay.blit(TextSurf, TextRect)
    # For Middle text
    def message_display(self,text):
        largeText = pygame.font.Font('freesansbold.ttf', 20)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = (display_width / 2, display_height / 2)
        gameDisplay.blit(TextSurf, TextRect)
    # for Top bar text
    def score_display(self,text):
        largeText = pygame.font.Font('freesansbold.ttf', 20)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = (display_width / 2, 10)
        gameDisplay.blit(TextSurf, TextRect)
    def text_objects(self,text, font):
        textSurface = font.render(text, True, pink)
        return textSurface, textSurface.get_rect()
    def crash(self,text):
        self.message_display(text)
        pygame.display.update()
        time.sleep(2)
        game_loop()


def areaEnterLoopInitializing(rocket,currentStage):
    areaEnterInitializingDict={0:[]}
    x_change = 0
    y_change = 0
    walkSpeed=2
    itemLocationDict=currentStage.getStageItemLocationsDict()
    currentStageNum=rocket.getStage()
    mapX=stageDict[rocket.getStage()][5][0]
    mapY=stageDict[rocket.getStage()][5][1]
    rocket.setX(stageDict[rocket.getStage()][4][0])
    rocket.setY(stageDict[rocket.getStage()][4][1])
    townShopsImg=currentStage.getStageImg()
    #Stage Dimensions
    stageWidth=currentStage.getStageWidth()
    stageHeight=currentStage.getStageHeight()
    townShopsImg=pygame.transform.scale(townShopsImg, (stageWidth, stageHeight))
    mapDict=currentStage.getStageMapDict()
    itemLocationDictNames={}
    townExit = False
    showInventory=False
    showSkills=False
    useSkillBool=False
    skillsTrueFalseCount=0
    trueFalse=[True,False]
    trueFalseCount=0
    aniCount=0
    #CroppedDict for sprite animation
    CD={}
    #more efficient to have a dict with preloade images instead of directory to pngs
    for i in range(16):
        CD[i+1]="cropped"+str(i+1)+".png"
    frames=6
    #set 2 aminations
    downAnimation1=[CD[1]]*frames+[CD[2]]*frames+[CD[3]]*frames+[CD[4]]*frames
    leftAnimation1=[CD[5]]*frames+[CD[6]]*frames+[CD[7]]*frames+[CD[8]]*frames
    rightAnimation1=[CD[9]]*frames+[CD[10]]*frames+[CD[11]]*frames+[CD[12]]*frames
    upAnimation1=[CD[13]]*frames+[CD[14]]*frames+[CD[15]]*frames+[CD[16]]*frames
    result=(x_change,y_change,walkSpeed,itemLocationDict,currentStageNum,mapX,mapY,townShopsImg,stageWidth,stageHeight,
            mapDict,townExit,showInventory,showSkills,useSkillBool,skillsTrueFalseCount,trueFalse,trueFalseCount,aniCount,
            downAnimation1,leftAnimation1,rightAnimation1,upAnimation1)
    return result
def areaEnterLoop(rocket,currentStage):#currentStage=stage(rocket)
    # Is there another way to initiliaze these??
    result=areaEnterLoopInitializing(rocket, currentStage)
    x_change=result[0]
    y_change=result[1]
    walkSpeed=result[2]
    itemLocationDict=result[3]
    currentStageNum=result[4]
    mapX=result[5]
    mapY=result[6]
    townShopsImg=result[7]
    stageWidth=result[8]
    stageHeight=result[9]
    mapDict=result[10]
    townExit=result[11]
    showInventoryBool=result[12]
    showSkillsBool=result[13]
    useSkillBool=result[14]
    skillsTrueFalseCount=result[15]
    trueFalse=result[16]
    trueFalseCount=result[17]
    aniCount=result[18]
    downAnimation1=result[19]
    leftAnimation1=result[20]
    rightAnimation1=result[21]
    upAnimation1=result[22]

    iconImg=skillDict['testItem1'][0]
    iconStr='testItem1'
    iconDragBool = False
    useProjSkillBool=False
    rPush = False
    startXYPixel=(0,0)
    rotDeg=0

    while not townExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #save_obj(rocket,'myRocket')
                #np.save('my_rocket.npy', rocket)
                gameExit = True
                pygame.quit()
            #For KEY DOWN type
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_change = -walkSpeed
                elif event.key == pygame.K_d:
                    x_change = walkSpeed
                elif event.key == pygame.K_w:
                    y_change = -walkSpeed
                elif event.key == pygame.K_s:
                    y_change = walkSpeed
                elif event.key == pygame.K_SPACE:
                    pass
                elif event.key == pygame.K_i:
                    showInventoryBool=trueFalse[trueFalseCount]
                    trueFalseCount=(trueFalseCount+1)%2
                elif event.key == pygame.K_k:
                    showSkillsBool=trueFalse[skillsTrueFalseCount]
                    skillsTrueFalseCount=(skillsTrueFalseCount+1)%2
                elif event.key == pygame.K_z:
                    itemEventHandle(rocket,(mapX,mapY),mapDict,itemLocationDict)
                elif event.key == pygame.K_o:
                    itemDropHandle(rocket)
                elif event.key == pygame.K_TAB:
                    #rocket.swapAmmo()
                    pass
                elif event.key == pygame.K_q:
                    inputSkill = 1
                    currentTime=pygame.time.get_ticks()
                    #by multiplying before dividing you can increase the sensitivity of cooldown control
                    if(int((currentTime-rocket.getCoolDownTimer())/1000)>skillUseDict[inputSkill][3][0]):
                        useSkillBool=True
                        rocket.setCoolDownTimer(currentTime)
                    else:
                        useSkillBool=False
                elif event.key == pygame.K_e:
                    inputSkill = 2
                    currentTime=pygame.time.get_ticks()
                    #by multiplying before dividing you can increase the sensitivity of cooldown control
                    if(int((currentTime-rocket.getCoolDownTimer())/1000)>skillUseDict[inputSkill][3][0]):
                        useSkillBool=True
                        rocket.setCoolDownTimer(currentTime)
                elif event.key == pygame.K_r:
                    inputSkill = 1
                    currentTime=pygame.time.get_ticks()
                    if (int((currentTime - rocket.getCoolDownTimer()) / 1000) > skillProjUseDict[inputSkill][3][0]):
                        rPush=True
                        useProjSkillBool=True
                        startXYPixel=(rocket.getX(),rocket.getY())
                        startMapXY=(mapX,mapY)
                        endMousePos=pygame.mouse.get_pos()
                        rocket.setProjectileMotionDict(startMapXY, startXYPixel, endMousePos)
                        try:
                            rotDeg=-(180/math.pi*math.atan((endMousePos[1]-startXYPixel[1])/(endMousePos[0]-startXYPixel[0])))
                        except:
                            pass
                        rocket.setCoolDownTimer(currentTime)
                elif event.key == pygame.K_f:
                    inputSkill = 2
                    currentTime=pygame.time.get_ticks()
                    if (int((currentTime - rocket.getCoolDownTimer()) / 1000) > skillProjUseDict[inputSkill][3][0]):
                        rPush=True
                        useProjSkillBool=True
                        startXYPixel=(rocket.getX(),rocket.getY())
                        startMapXY=(mapX,mapY)
                        endMousePos=pygame.mouse.get_pos()
                        rocket.setProjectileMotionDict(startMapXY, startXYPixel, endMousePos)
                        try:
                            rotDeg=-(180/math.pi*math.atan((endMousePos[1]-startXYPixel[1])/(endMousePos[0]-startXYPixel[0])))
                        except:
                            pass
                        rocket.setCoolDownTimer(currentTime)

            #For KEY UP type
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x_change = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    y_change = 0
                elif event.key == pygame.K_q:
                    #useSkillBool=False
                    pass
            if event.type==pygame.MOUSEBUTTONDOWN:
                mousePos=pygame.mouse.get_pos()
                iconPlaceCheck(iconDragBool,iconStr,mousePos,rocket)
                iconDragBool,iconStr, iconImg=iconDragCheck(showSkillsBool,showInventoryBool, mousePos,rocket)
        if x_change==-walkSpeed:
            rocket.setImg(leftAnimation1[aniCount])
            aniCount=(aniCount+1)%len(leftAnimation1)#remove this len function for speed later
        if x_change==walkSpeed:
            rocket.setImg(rightAnimation1[aniCount])
            aniCount=(aniCount+1)%len(rightAnimation1)
        if y_change==-walkSpeed:
            rocket.setImg(upAnimation1[aniCount])
            aniCount=(aniCount+1)%len(upAnimation1)
        if y_change==walkSpeed:
            rocket.setImg(downAnimation1[aniCount])
            aniCount=(aniCount+1)%len(downAnimation1)
        #Processes the if statements required for blitting map on corners or moving till character is centered
        mapX,mapY=refactorIfStatements(mapX,mapY,x_change,y_change,stageWidth,stageHeight,rocket,mapDict)
        # Draw map background
        gameDisplay.blit(townShopsImg, (mapX, mapY))
        #Displays items on map, respawns items wrt respawnTimer
        itemDisplay(itemLocationDict,mapX,mapY)
        monsterUpdater(monsterPlacesDict,(mapX,mapY))
        rocket.display()#note** hitbox at feet
        rocket.displaySkillBar()
        if showInventoryBool:
            rocket.displayInventory()
        if showSkillsBool:
            rocket.displaySkills()
        if useSkillBool:
            rocket.useSkill(inputSkill)#input skill is based on what key was pressed
            if rocket.useSkillEnd():
                useSkillBool=False
        if (rPush):#sets up the complete motions of projectile to refer to
            useProjSkillBool = True
            startXYPixel = (rocket.getX(), rocket.getY())
            startMapXY = (mapX, mapY)
            endMousePos = pygame.mouse.get_pos()
            rocket.setProjectileMotionDict(startMapXY, startXYPixel, endMousePos)
            try:
                rotDeg = -(180 / math.pi * math.atan(
                    (endMousePos[1] - startXYPixel[1]) / (endMousePos[0] - startXYPixel[0])))
                if (endMousePos[0] - startXYPixel[0] < 0):
                    rotDeg = rotDeg + 180
            except:
                pass

            print(rotDeg)
            rPush=False
        if useProjSkillBool:#updates projectiles pos wrt to map and player
            rocket.useProjectileSkill(inputSkill, (mapX,mapY), rotDeg)
            if rocket.useProjSkillEnd():
                useProjSkillBool=False
        if iconDragBool:
            gameDisplay.blit(iconImg,(pygame.mouse.get_pos()))
        if rocket.getStage()!=currentStageNum:
            stageChangeSequence(currentStageNum,rocket,mapX,mapY)
            townExit=True
        pygame.display.update()
        clock.tick(60)
def iconDragCheck(showSkillsBool,showInventoryBool, positionTuple,rocket):
    iconDragBool=False
    img=skillDict['testItem1'][0]
    imgStr='testItem1'
    #implement variablity for future
    maxSlotRow,maxSlotCol=4,4
    minX,maxX,minY,maxY=0,200,500,700
    slotMinX, slotMaxX, slotMinY, slotMaxY = 0, 200, 0, 200
    x,y =positionTuple[0], positionTuple[1]
    if(showSkillsBool):
        #method to number skill slots
        slotX=int(x/((maxX-minX)/maxSlotRow))
        slotY = int((y-minY) / ((maxY - minY) / maxSlotCol))
        skillListIndex=(4*slotY+slotX)
        if(x>minX and x<maxX and y >minY and y<maxY and skillListIndex<len(rocket.skillList)):
            iconDragBool=True
            return iconDragBool, rocket.skillList[skillListIndex], skillDict[rocket.skillList[skillListIndex]][0]
        else:
            iconDragBool=False
    if (showInventoryBool):
        # method to number skill slots
        slotX = int(x / ((slotMaxX - slotMinX) / maxSlotRow))
        slotY = int((y - slotMinY) / ((slotMaxY - slotMinY) / maxSlotCol))
        itemListIndex = (4 * slotY + slotX)
        if (x > slotMinX and x < slotMaxX and y > slotMinY and y < slotMaxY and itemListIndex < len(rocket.itemList)):
            iconDragBool = True
            return iconDragBool, rocket.itemList[itemListIndex], itemDict[rocket.itemList[itemListIndex]][0]
        else:
            iconDragBool = False
    return iconDragBool,imgStr, img
def iconPlaceCheck(iconDragBool,iconStr,posTuple,rocket):
    iconPlaceBool=False
    xMin,yMin=rocket.skillBarLocationX+10,rocket.skillBarLocationY
    xMax,yMax=xMin+265,yMin+50
    xWidth=265
    nSlot=9#number of slots in the bar
    x,y=posTuple[0],posTuple[1]
    if(iconDragBool):
        skillBarListIndex=int((x-xMin)/(xWidth/nSlot))
        if(x>xMin and x<xMax and y>yMin and y<yMax and skillBarListIndex<nSlot):
            rocket.skillBarList[skillBarListIndex]=iconStr
def stageChangeSequence(currentStageNum,rocket,mapX,mapY):
    stageDict[currentStageNum][4][0] = rocket.getX()
    stageDict[currentStageNum][4][1] = rocket.getY()
    stageDict[currentStageNum][5][0] = mapX
    stageDict[currentStageNum][5][1] = mapY
def refactorIfStatements(mapX,mapY,x_change,y_change,stageWidth,stageHeight,rocket,mapDict):
    if mapX-x_change>=-stageWidth+display_width \
            and mapX-x_change<0 \
            and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()][0]:##DONE
        mapX=mapX-x_change
        if (rocket.getX()-display_width/2)**2+(rocket.getY()-display_height/2)**2>20**2:
            if((rocket.getX()-display_width/2)**2>30**2):
                if(rocket.getX()+x_change>20
                        and rocket.getX()+x_change<display_width-20
                        and mapDict[-(mapX-x_change)+rocket.getX()+x_change,-(mapY-y_change)+rocket.getY()][0]):##
                    rocket.setX(rocket.getX()+x_change)
            if((rocket.getY()-display_height/2)**2>30**2):
                if(rocket.getY()+y_change>20
                        and rocket.getY()+y_change<display_height-20
                        and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()+y_change][0]):##
                    rocket.setY(rocket.getY()+y_change)
    #Y component changes
    if mapY-y_change>=-stageHeight+display_height \
            and mapY-y_change<=0 \
            and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()][0]:##DONE
        mapY=mapY-y_change
        if (rocket.getX()-display_width/2)**2+(rocket.getY()-display_height/2)**2>20**2:
            if((rocket.getX()-display_width/2)**2>30**2):
                if(rocket.getX()+x_change>20
                        and rocket.getX()+x_change<display_width-20
                        and mapDict[-(mapX-x_change)+rocket.getX()+x_change,-(mapY-y_change)+rocket.getY()][0]):##
                    rocket.setX(rocket.getX()+x_change)
            if((rocket.getY()-display_height/2)**2>30**2):
                if(rocket.getY()+y_change>20
                        and rocket.getY()+y_change<display_height-20
                        and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()+y_change][0]):##
                    rocket.setY(rocket.getY()+y_change)
    #map position does not update and only player moves
    #X component changes
    if mapX-x_change<=-stageWidth+display_width or mapX-x_change >=0:
        if(rocket.getX()+x_change>20
                and rocket.getX()+x_change<display_width-20
                and mapDict[-(mapX)+rocket.getX()+x_change,-(mapY)+rocket.getY()][0]):##
            rocket.setX(rocket.getX()+x_change)
    #YComponent changes
    if mapY-y_change<=-stageHeight+display_height or mapY-y_change >=0:
        if(rocket.getY()+y_change>20
                and rocket.getY()+y_change<display_height-20
                and mapDict[-(mapX)+rocket.getX(),-(mapY)+rocket.getY()+y_change][0]):##
            rocket.setY(rocket.getY()+y_change)
    return(mapX,mapY)
def itemDisplay(itemLocationDict,mapX,mapY):
    # Displays items on map, respawns items wrt respawnTimer
    for k, v in itemLocationDict.items():
        # if item has respawned and itemLocation is in map bounds
        if v[1] and v[0][0] > -mapX \
                and v[0][0] < -mapX + display_width \
                and v[0][1] > -mapY \
                and v[0][1] < -mapY + display_height:
            gameDisplay.blit(itemDict[k][0], (v[0][0] - (-mapX), v[0][1] - (-mapY)))
            gameDisplay.blit(itemLine, (v[0][0] - (-mapX), v[0][1] - (-mapY)))
        # item respawner
        if int(pygame.time.get_ticks() / 1000) % respawnTimer == 0:
            v[1] = True
def itemEventHandle(rocket,mapLocation,mapDict,itemLocationDict):
    xLocation=-mapLocation[0]+rocket.getX()
    yLocation=-mapLocation[1]+rocket.getY()
    if(mapDict[(xLocation,yLocation)][1]==True):#for picking up
        #mapDict[(xLocation,yLocation)][1]=False
        if(itemLocationDict[mapDict[xLocation,yLocation][2]][1]==True):
            rocket.addItem(mapDict[xLocation,yLocation][2])
            itemLocationDict[mapDict[xLocation,yLocation][2]][1]=False
    if(mapDict[(xLocation,yLocation)][3]==True):#for entering stage
        rocket.setStage(mapDict[(xLocation,yLocation)][4])
def itemDropHandle(rocket):
    rocket.popItem()
def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def bossBattleLoop(rocket):
    x_change=0
    y_change=0
    bgCount=0
    bulletList=[]
    boss=Boss('ship3.png')
    bossExit = False
    while not bossExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    x_change=-3
                elif event.key == pygame.K_RIGHT:
                    x_change=3
                elif event.key == pygame.K_UP:
                    y_change=-3
                elif event.key == pygame.K_DOWN:
                    y_change=3
                elif event.key == pygame.K_SPACE:
                    bulletList.append(Bullet(rocket))
                elif event.key == pygame.K_TAB:
                    rocket.swapAmmo()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change =0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
        rocket.setX((rocket.getX()+x_change))#%display_width)
        rocket.setY((rocket.getY()+y_change)%display_height)
        #Loading Background
        gameDisplay.blit(bg[2],(0,0))
        #gameDisplay.blit(townImg,(0,0))
        rocket.display()
        #Bullet update
        for i in range(0,len(bulletList)):
            bulletList[i].update()
            #bullet is popped if bullet is offscreen or collides into an object
            if bulletList[i].getY()<0.1 or not bulletList[i].getNoCollision():
                bulletList.pop(i)
                break
        boss.update()
        if boss.ifCrash(rocket):
            textDisplay().crash('GameOver, Final Score: '+str(score))
        for j in range(0,len(bulletList)):
            if bulletList[j].ifHit(boss,rocket):
                boss.gotHit()
                boss.update()
        #Car collion on side wall
        if rocket.getX()>display_width-rocket.getXScale() or rocket.getX() < 0:
            textDisplay().crash('GameOver, Final Score: '+str(score))
        textDisplay().score_display('Boss Score: '+str(score))
        pygame.display.update()
        clock.tick(60)
        if boss.getIsDefeated():
            bossExit=True
def game_loop():
    x_change=0
    y_change=0
    bgCount=0
    score=0
    bossLVL=1
    meteorList=[]
    bulletList=[]
    gameExit = False
    #Creating Rocket Class
    rocket=Rocket(rocketImgStr)
    #rocket=load_obj('myRocket')
    #initiliazing stage Loops
    bossBattle = False
    townEnter = True
    areaEnterTest=True
    while not gameExit:
        #New Idea to avoid nested while loops for different stage events
        #stage=checkStageEnterLoop(rocket.getCurrentStage())
        #stageEnterLoop(rocket)#Rocket must contain the extra arguments needed for the stage
        #stageEnterLoop(rocket,stage.Map(),stage.MapData())
#New Game Implementation tests------------------
        while areaEnterTest:
            print('Stage Exnter....')
            currentStage=stage(rocket)
            areaEnterLoop(rocket,currentStage)
            #Area exit condition
            if (rocket.getStage()==10):
                areaEnterTest=False
                currentStage=rocket.setStage()
            print('Stage Exit....')
#new Game Implementation end ---------------
#NEW GAME MODE IDEA
            #ROCKET.GETGAMEMODE()
            #Game mode will determine, areaEnterLoop() or bossBattleLoop() or gameLoop() etc....
        if bossBattle:
            bossBattleLoop(rocket)
            bossBattle=False
##        if townEnter:
##            townEnterLoop(rocket,itemLocationDict)
##            townEnter=False
        #no boss battle case
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()
            #customize movements later by defining movement for rocket class
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    x_change=-3
                elif event.key == pygame.K_RIGHT:
                    x_change=3
                elif event.key == pygame.K_UP:
                    y_change=-3
                elif event.key == pygame.K_DOWN:
                    y_change=3
                elif event.key == pygame.K_SPACE:
                    bulletList.append(Bullet(rocket))
                elif event.key == pygame.K_TAB:
                    rocket.swapAmmo()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change =0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
        rocket.setX((rocket.getX()+x_change))#%display_width)
        rocket.setY((rocket.getY()+y_change)%display_height)
        #Loading Background
        #gameDisplay.fill(white)
        bgCount=(bgCount+1)%60
        #gameDisplay.blit(backgroundImg,(0,0))
        #gameDisplay.blit(bg[int(bgCount/20)],(0,0))
        gameDisplay.blit(bg[2],(0,0))
        rocket.display()
        #Bullet update
        for i in range(0,len(bulletList)):
            bulletList[i].update()
            if bulletList[i].getY()<0.1 or not bulletList[i].getNoCollision():
                bulletList.pop(i)
                break
        #New block every 15 max 10 blocks
        if len(meteorList)<=score/15 and len(meteorList)<10:
            meteorList.append(Meteor())
        for i in range(0,len(meteorList)):
            meteorList[i].update(score)
        for i in range(0,len(meteorList)):
            if meteorList[i].getY() == 0:
                score=score+1
        #Collision detection, create a loop for more meteors
        for i in range(0,len(meteorList)):
            if meteorList[i].ifCrash(rocket):
                textDisplay().crash('GameOver, Final Score: '+str(score))
                score=0
            for j in range(0,len(bulletList)):
                #If bullet hits, restart meteor
                if bulletList[j].ifHit(meteorList[i],rocket):
                    meteorList[i]=Meteor()
                    score=score+3
        #How often the boss comes
        if score>(bossLVL+25)**2-25**2:
            bossLVL=bossLVL+1
            bossBattle=True
        #Car collion on side wall
        if rocket.getX()>display_width-rocket.getXScale() or rocket.getX() < 0:
            textDisplay().crash('GameOver, Final Score: '+str(score))
        textDisplay().score_display('Score: '+str(score))
        pygame.display.update()
        clock.tick(60)

#-------------------EXECUTING CODE------------------
pygame.init()

#Initiliaizing Game Window
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Galaxy Explorers')
clock=pygame.time.Clock()

game_loop()

