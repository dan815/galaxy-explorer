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
rocketImgStr='rocketsam.png'
#rocketImgStr='invis_upMove.png'
#rocketImgStr='ship3.png'
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
#Skill Dictionary Data
skillDict={'testItem1':[testItem1Img],'testItem2':[testItem2Img],'testItem3':[testItem3Img]}
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
skillCoolDown1=2# 3 sec cool down
skillUseDict={1:[0,[skillAni0,skillAni1,skillAni2,skillAni3,skillAni4,skillAni5,skillAni6,skillAni7],
                 [(skillAniWidth,skillAniHeight),(60,85),(60,85),(60,85),(60,85),(60,85),(60,85),(60,85)],
                 [skillCoolDown1]]}

#stageDict={stageNumber:[stageImg,(stageWidth,stageHeight), stageDictFileName, stageItemLocations,[rocketX,rocketY],[mapX,MapY]]}
stageDict={1:[townShopsImg,(2000,2000),'map1',itemLocationDict,[410,350],[0,0]],
           2:[shopInside1,(700,700),'map2',{},[350,650],[0,0]],
           3:[library,(1087,734),'map3',{},[510,657],[0,0]]}#do item locations same as stageDictFileName later
#pickle loading for mapDict
def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
class ItemData():
    #itemDict={'itemName':[itemImg,itemStats,...]}
    def img(self,item):
        return itemDict[item][0]
class skillData():
    #itemDict={'itemName':[itemImg,itemStats,...]}
    def img(self,item):
        return skillDict[item][0]#returns the img associated to skill string
class skillBarData():
    #itemDict={'itemName':[itemImg,itemStats,...]}
    def img(self,item):
        return skillBarDict[item][0]#returns the img associated to skill string
class Skills():
    def __init__(self):
        self.skillListImg=skillListImg
        self.skillBarImg=skillBarImg
        self.skillList=[]#if this is left empty, it still takes the skillList of parent or subclass I think...
        self.skillBarList=[]
        self.skillBarLocationX=200
        self.skillBarLocationY=650
        self.offsetX=display_width-200
        self.offsetY=display_height-200
        self.skillSlotXY = [(12, 10), (60, 10), (106, 10), (153, 10), (12, 58), (60, 58), (106, 58), (153, 58),
                            (12, 104),(60, 104), (106, 104), (153, 104), (12, 152), (60, 152), (106, 152), (153, 152)]
        self.skillBarSlotXY=[(10,10),(40,10),(70,10),(100,10),(130,10),(160,10),(190,10),(220,10),(250,10)]
        self.skillBarSlotXY=[(u[0]+self.skillBarLocationX,u[1]+self.skillBarLocationY) for u in self.skillBarSlotXY]
        self.skillSlotXY=[(u[0],u[1]+self.offsetY) for u in self.skillSlotXY]
        self.skillSlot=0
        self.skillFrameRepeat=4
        self.skillFrameInit=0
        self.inputSkillNumber=0
        self.coolDownTimer=0
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
        self.skillBarList = ['testItem1', 'testItem2', 'testItem2', 'testItem1']
        #ammo uesd for bullet class object
        self.ammo=1
        self.ammoTypes=2
        self.stage=1
    def setStage(self,stageNum):
        self.stage=stageNum
    def getStage(self):
        return self.stage
    def display(self,x,y):
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
        #takes in a rocket class
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
            text_display('I'*int(self.hp/10),self.x+self.width/2,self.y,20-int((100-self.hp)/10))
        if self.hp<1:
            self.x=-100
            self.y=-500
            self.isDefeated=True
    def getIsDefeated(self):
        return self.isDefeated

def text_display(text,xCenter,yCenter,hpFont):
    largeText=pygame.font.Font('freesansbold.ttf',hpFont)
    TextSurf, TextRect = text_objects(text,largeText)
    TextRect.center = (xCenter,yCenter)
    gameDisplay.blit(TextSurf, TextRect)
#For Middle text
def message_display(text):
    largeText=pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text,largeText)
    TextRect.center = (display_width/2,display_height/2)
    gameDisplay.blit(TextSurf, TextRect)
#for Top bar text
def score_display(text):
    largeText=pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text,largeText)
    TextRect.center = (display_width/2,10)
    gameDisplay.blit(TextSurf, TextRect)
def text_objects(text, font):
    textSurface=font.render(text,True, pink)
    return textSurface, textSurface.get_rect()
#for rocket crashes
def crash(text):
    message_display(text)
    pygame.display.update()
    time.sleep(2)
    game_loop()

def bossBattleLoop(rocket):
    x_change=0
    y_change=0
    bgCount=0
    bulletList=[]
##    bossList=[]
##    bossList.append(Boss())
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
        rocket.display(rocket.getX(),rocket.getY())
        #Bullet update
        for i in range(0,len(bulletList)):
            bulletList[i].update()
            #bullet is popped if bullet is offscreen or collides into an object
            if bulletList[i].getY()<0.1 or not bulletList[i].getNoCollision():
                bulletList.pop(i)
                break
        boss.update()
        if boss.ifCrash(rocket):
            crash('GameOver, Final Score: '+str(score))
        for j in range(0,len(bulletList)):
            if bulletList[j].ifHit(boss,rocket):
                boss.gotHit()
                boss.update()
        #Car collion on side wall
        if rocket.getX()>display_width-rocket.getXScale() or rocket.getX() < 0:
            crash('GameOver, Final Score: '+str(score))
        score_display('Boss Score: '+str(score))
        pygame.display.update()
        clock.tick(60)
        if boss.getIsDefeated():
            bossExit=True

#currentStage=stage(rocket)


def areaEnterLoop(rocket,currentStage):
    itemLocationDict=currentStage.getStageItemLocationsDict()
    currentStageNum=rocket.getStage()
    x_change = 0
    y_change = 0
    bgCount = 0
    walkSpeed=2
    bulletList = []
    mapX=stageDict[rocket.getStage()][5][0]
    mapY=stageDict[rocket.getStage()][5][1]
    rocket.setX(stageDict[rocket.getStage()][4][0])
    rocket.setY(stageDict[rocket.getStage()][4][1])
    #charImg=''
    #rocket.setImg(charImg)
    ##    bossList=[]
    ##    bossList.append(Boss())
    #rename variable appropriately
    townShopsImg=currentStage.getStageImg()
    boss = Boss('ship3.png')
    #Stage Dimensions
    stageWidth=currentStage.getStageWidth()
    stageHeight=currentStage.getStageHeight()
    townShopsImg=pygame.transform.scale(townShopsImg, (stageWidth, stageHeight))
    #mapDict=mapInitializer() #mapCreator.py script and pickled as map1.pkl to save load time
    mapDict=currentStage.getStageMapDict()
    #itemLocationDict implemented as Global Variable with itemDict
    #itemLocationDict={'testItem1':[(650,480),True],'testItem2':[(650,550),True]}
    itemLocationDictNames={}
    townExit = False
    #mapDict=np.load('my_file.npy').item()
    showInventory=False
    showSkills=False
    useSkillBool=False
    skillsTrueFalseCount=0
    trueFalse=[True,False]
    trueFalseCount=0
    aniCount=0
    LS='invis_leftStationary.png'
    LM='invis_leftMove.png'
    RS='invis_rightStationary.png'
    RM='invis_rightMove.png'
    US='invis_upStationary.png'
    UM='invis_upMove.png'
    DS='invis_downStationary.png'
    DM='invis_downMove.png'
    #CroppedDict for sprite animation
    CD={}
    #more efficient to have a dict with preloade images instead of directory to pngs
    for i in range(16):
        CD[i+1]="cropped"+str(i+1)+".png"
    frames=6
    #SELF NOTE: LOOK INTO SPRITE SHEETS AND LOADING FROM SPRITE SHEETS
    leftAnimation=[LS]*frames+[LM]*frames
    rightAnimation=[RS]*frames+[RM]*frames#['invis_rightStationary.png','invis_rightStationary.png','invis_rightStationary.png','invis_rightStationary.png','invis_rightMove.png','invis_rightMove.png','invis_rightMove.png','invis_rightMove.png']
    upAnimation=[US]*frames+[UM]*frames#['invis_upStationary.png','invis_upStationary.png','invis_upStationary.png','invis_upStationary.png','invis_upMove.png','invis_upMove.png','invis_upMove.png','invis_upMove.png']
    downAnimation=[DS]*frames+[DM]*frames#['invis_downStationary.png','invis_downStationary.png','invis_downStationary.png','invis_downStationary.png','invis_downMove.png','invis_downMove.png','invis_downMove.png','invis_downMove.png']
    #set 2 aminations
    downAnimation1=[CD[1]]*frames+[CD[2]]*frames+[CD[3]]*frames+[CD[4]]*frames
    leftAnimation1=[CD[5]]*frames+[CD[6]]*frames+[CD[7]]*frames+[CD[8]]*frames
    rightAnimation1=[CD[9]]*frames+[CD[10]]*frames+[CD[11]]*frames+[CD[12]]*frames
    upAnimation1=[CD[13]]*frames+[CD[14]]*frames+[CD[15]]*frames+[CD[16]]*frames
    #skillsTrueFalseCount = {0: 0}
    #trueFalseCount = {0: 0}
    while not townExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #save_obj(rocket,'myRocket')
                #np.save('my_rocket.npy', rocket)
                gameExit = True
                pygame.quit()
            #For KEY DOWN type
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -walkSpeed
                elif event.key == pygame.K_RIGHT:
                    x_change = walkSpeed
                elif event.key == pygame.K_UP:
                    y_change = -walkSpeed
                elif event.key == pygame.K_DOWN:
                    y_change = walkSpeed
                elif event.key == pygame.K_SPACE:
                    pass
                elif event.key == pygame.K_i:
                    showInventory=trueFalse[trueFalseCount]
                    trueFalseCount=(trueFalseCount+1)%2
                elif event.key == pygame.K_s:
                    showSkills=trueFalse[skillsTrueFalseCount]
                    skillsTrueFalseCount=(skillsTrueFalseCount+1)%2
                elif event.key == pygame.K_a:
                    #
                    itemEventHandle(rocket,(mapX,mapY),mapDict,itemLocationDict)
                elif event.key == pygame.K_o:
                    itemDropHandle(rocket)
                elif event.key == pygame.K_TAB:
                    #rocket.swapAmmo()
                    pass
                elif event.key == pygame.K_q:
                    inputSkill = 1
                    currentTime=pygame.time.get_ticks()
                    #by diving by multiplying before dividing you can increase the sensitivity of cooldown control
                    if(int((currentTime-rocket.getCoolDownTimer())/1000)>skillUseDict[inputSkill][3][0]):#instead of '2' use the actual CD skillTime
                        useSkillBool=True
                        rocket.setCoolDownTimer(currentTime)
            #For KEY UP type
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
                elif event.key == pygame.K_q:
                    #useSkillBool=False
                    pass

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
  #map poistion updates if it is in bounds, and player moves until centered
        #X component changes

    #
    #     if mapX-x_change>=-stageWidth+display_width \
    #             and mapX-x_change<0 \
    #             and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()][0]:##DONE
    #         mapX=mapX-x_change
    #         if (rocket.getX()-display_width/2)**2+(rocket.getY()-display_height/2)**2>20**2:
    #             if((rocket.getX()-display_width/2)**2>30**2):
    #                 if(rocket.getX()+x_change>20
    #                         and rocket.getX()+x_change<display_width-20
    #                         and mapDict[-(mapX-x_change)+rocket.getX()+x_change,-(mapY-y_change)+rocket.getY()][0]):##
    #                     rocket.setX(rocket.getX()+x_change)
    #             if((rocket.getY()-display_height/2)**2>30**2):
    #                 if(rocket.getY()+y_change>20
    #                         and rocket.getY()+y_change<display_height-20
    #                         and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()+y_change][0]):##
    #                     rocket.setY(rocket.getY()+y_change)
    #     #Y component changes
    #     if mapY-y_change>=-stageHeight+display_height \
    #             and mapY-y_change<=0 \
    #             and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()][0]:##DONE
    #         mapY=mapY-y_change
    #         if (rocket.getX()-display_width/2)**2+(rocket.getY()-display_height/2)**2>20**2:
    #             if((rocket.getX()-display_width/2)**2>30**2):
    #                 if(rocket.getX()+x_change>20
    #                         and rocket.getX()+x_change<display_width-20
    #                         and mapDict[-(mapX-x_change)+rocket.getX()+x_change,-(mapY-y_change)+rocket.getY()][0]):##
    #                     rocket.setX(rocket.getX()+x_change)
    #             if((rocket.getY()-display_height/2)**2>30**2):
    #                 if(rocket.getY()+y_change>20
    #                         and rocket.getY()+y_change<display_height-20
    #                         and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()+y_change][0]):##
    #                     rocket.setY(rocket.getY()+y_change)
    # #map position does not update and only player moves
    #     #X component changes
    #     if mapX-x_change<=-stageWidth+display_width or mapX-x_change >=0:
    #         if(rocket.getX()+x_change>20
    #                 and rocket.getX()+x_change<display_width-20
    #                 and mapDict[-(mapX)+rocket.getX()+x_change,-(mapY)+rocket.getY()][0]):##
    #             rocket.setX(rocket.getX()+x_change)
    #     #YComponent changes
    #     if mapY-y_change<=-stageHeight+display_height or mapY-y_change >=0:
    #         if(rocket.getY()+y_change>20
    #                 and rocket.getY()+y_change<display_height-20
    #                 and mapDict[-(mapX)+rocket.getX(),-(mapY)+rocket.getY()+y_change][0]):##
    #             rocket.setY(rocket.getY()+y_change)
        #Draw map background

        mapX,mapY=refactorIfStatements(mapX,mapY,x_change,y_change,stageWidth,stageHeight,display_width,display_height,rocket,mapDict)
        gameDisplay.blit(townShopsImg, (mapX, mapY))
        #Displays items on map, respawns items wrt respawnTimer
        for k,v in itemLocationDict.items():
            #if item has respawned and itemLocation is in map bounds
            if v[1] and v[0][0]>-mapX \
                    and v[0][0]<-mapX+display_width \
                    and v[0][1] > -mapY \
                    and v[0][1] <-mapY+display_height:
                gameDisplay.blit(itemDict[k][0],(v[0][0]-(-mapX),v[0][1]-(-mapY)))
                gameDisplay.blit(itemLine,(v[0][0]-(-mapX),v[0][1]-(-mapY)))
            #item respawner
            if int(pygame.time.get_ticks()/1000)%respawnTimer==0:
                v[1]=True
        # printing the character as x and y(near feet) as its center instead of the top corner
        rocket.display(rocket.getX() - rocket.getXScale() / 2, rocket.getY() - int(rocket.getYScale() * 0.8))
        rocket.displaySkillBar()
        if showInventory:
            rocket.displayInventory()
        if showSkills:
            rocket.displaySkills()
        if useSkillBool:
            rocket.useSkill(inputSkill)#inputSkill from keyboard event
            if rocket.useSkillEnd():
                useSkillBool=False
        if rocket.getStage()!=currentStageNum:#if stage is about to change
            #store the rockets position on screen and the last blitted map position
            stageDict[currentStageNum][4][0]=rocket.getX()
            stageDict[currentStageNum][4][1]=rocket.getY()
            stageDict[currentStageNum][5][0]=mapX
            stageDict[currentStageNum][5][1]=mapY
            townExit=True
        pygame.display.update()
        clock.tick(60)
#respawnTimer for item respawns
respawnTimer=25

def refactorIfStatements(mapX,mapY,x_change,y_change,stageWidth,stageHeight,display_width,display_height,rocket,mapDict):
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
def itemEventHandle(rocket,mapLocation,mapDict,itemLocationDict):
    xLocation=-mapLocation[0]+rocket.getX()
    yLocation=-mapLocation[1]+rocket.getY()
    if(mapDict[(xLocation,yLocation)][1]==True):
        #mapDict[(xLocation,yLocation)][1]=False
        if(itemLocationDict[mapDict[xLocation,yLocation][2]][1]==True):
            rocket.addItem(mapDict[xLocation,yLocation][2])
            itemLocationDict[mapDict[xLocation,yLocation][2]][1]=False
    if(mapDict[(xLocation,yLocation)][3]==True):
        rocket.setStage(mapDict[(xLocation,yLocation)][4])

def itemDropHandle(rocket):
    rocket.popItem()

#Space Travelling Asteroid Loop
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
        rocket.display(rocket.getX(),rocket.getY())
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
                crash('GameOver, Final Score: '+str(score))
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
            crash('GameOver, Final Score: '+str(score))
        score_display('Score: '+str(score))
        pygame.display.update()
        clock.tick(60)
#loop 1 uncompleto
game_loop()
#loop 2 commencemento

