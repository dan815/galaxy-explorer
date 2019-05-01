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
emptyInventoryImg=pygame.image.load('emptyInventory3.png')
emptyInventoryImg=pygame.transform.scale(emptyInventoryImg,(200,200))
testItem1Img=pygame.transform.scale(meteorImg,(40,40))
testItem2Img=pygame.transform.scale(fireMeteorImg,(40,40))
testItem3Img=pygame.transform.scale(bossImg,(40,40))
itemLine=pygame.transform.scale(bg4,(50,50))

#Item Dictionary Data
itemDict={'testItem1':[testItem1Img],'testItem2':[testItem2Img],'testItem3':[testItem3Img]}
itemLocationDict={'testItem1':[(650,480),True],'testItem2':[(650,550),True]}
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
        
class Inventory():
    def __init__(self):
       self.img=emptyInventoryImg
       self.itemList=[]
       self.itemSlot=0
       #self.slotXY=[(12,10),(60,10),(106,10),(162,10)]
       self.slotXY=[(12,10),(60,10),(106,10),(153,10),(12,58),(60,58),(106,58),(153,58),(12,104),(60,104),(106,104),(153,104),(12,152),(60,152),(106,152),(153,152)]
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

class Rocket(Inventory):
    def __init__(self,rocketImg):
        Inventory.__init__(self)
        self.Img=pygame.image.load(rocketImg)
        self.xScale=60
        self.yScale=80
        self.Img=pygame.transform.scale(self.Img,(60,80))
        self.x = 250
        self.y = 490
        self.itemList=['testItem1','testItem2','testItem3','testItem3']
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
        scaleSize=38
        self.Img=pygame.image.load(img)
        self.Img=pygame.transform.scale(self.Img,(scaleSize,scaleSize))
        self.xScale=scaleSize
        self.yScale=scaleSize
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
#Bullet Type Ideas
        #single fire
        #multiple fire
        #Timed Detonators
        #heat seeking missles
        #...
class Bullet():
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

        return ((self.x+self.width/2)-(rocket.getX()+rocket.getXScale()/2))**2 +((self.y+self.width/2)-(rocket.getY()+rocket.getYScale()/2))**2<(self.width/2+rocket.getXScale()/2)**2

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
#stageDict={stageNumber:[stageImg,(stageWidth,stageHeight), stageDictFileName, stageItemLocations,[rocketX,rocketY],[mapX,MapY]]}
            
stageDict={1:[townShopsImg,(2000,2000),'map1',itemLocationDict,[410,350],[0,0]],2:[shopInside1,(700,700),'map2',{},[350,650],[0,0]]}#do item locations same as stageDictFileName later
class stage():
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
    trueFalse=[True,False]
    trueFalseCount=0
    aniCount=0
    leftAnimation=['invis_leftStationary.png','invis_leftStationary.png','invis_leftStationary.png','invis_leftStationary.png','invis_leftMove.png','invis_leftMove.png','invis_leftMove.png','invis_leftMove.png']
    rightAnimation=['invis_rightStationary.png','invis_rightStationary.png','invis_rightStationary.png','invis_rightStationary.png','invis_rightMove.png','invis_rightMove.png','invis_rightMove.png','invis_rightMove.png']
    upAnimation=['invis_upStationary.png','invis_upStationary.png','invis_upStationary.png','invis_upStationary.png','invis_upMove.png','invis_upMove.png','invis_upMove.png','invis_upMove.png']
    downAnimation=['invis_downStationary.png','invis_downStationary.png','invis_downStationary.png','invis_downStationary.png','invis_downMove.png','invis_downMove.png','invis_downMove.png','invis_downMove.png']
    while not townExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #save_obj(rocket,'myRocket')
                #np.save('my_rocket.npy', rocket)
                gameExit = True
                pygame.quit()
                
            if x_change==-walkSpeed:
                rocket.setImg(leftAnimation[aniCount])
                aniCount=(aniCount+1)%len(leftAnimation)#remove this len function for speed later
            if x_change==walkSpeed:
                rocket.setImg(rightAnimation[aniCount])
                aniCount=(aniCount+1)%len(rightAnimation)
            if y_change==-walkSpeed:
                rocket.setImg(upAnimation[aniCount])
                aniCount=(aniCount+1)%len(upAnimation)
            if y_change==walkSpeed:
                rocket.setImg(downAnimation[aniCount])
                aniCount=(aniCount+1)%len(downAnimation)         

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
                    showInventory=trueFalse[trueFalseCount%2]
                    trueFalseCount+=1
                elif event.key == pygame.K_a:
                    #
                    itemEventHandle(rocket,(mapX,mapY),mapDict,itemLocationDict)
                elif event.key == pygame.K_o:
                    itemDropHandle(rocket)
                elif event.key == pygame.K_TAB:
                    #rocket.swapAmmo()
                    pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
        if x_change==-walkSpeed:
            rocket.setImg(leftAnimation[aniCount])
            aniCount=(aniCount+1)%len(leftAnimation)#remove this len function for speed later
        if x_change==walkSpeed:
            rocket.setImg(rightAnimation[aniCount])
            aniCount=(aniCount+1)%len(rightAnimation)
        if y_change==-walkSpeed:
            rocket.setImg(upAnimation[aniCount])
            aniCount=(aniCount+1)%len(upAnimation)
        if y_change==walkSpeed:
            rocket.setImg(downAnimation[aniCount])
            aniCount=(aniCount+1)%len(downAnimation)

  #map poistion updates if it is in bounds, and player moves until centered        
        if mapX-x_change>=-stageWidth+display_width and mapX-x_change<0 and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()][0]:##DONE
            mapX=mapX-x_change
            if (rocket.getX()-display_width/2)**2+(rocket.getY()-display_height/2)**2>20**2:
                if((rocket.getX()-display_width/2)**2>30**2):
                    if(rocket.getX()+x_change>20 and rocket.getX()+x_change<display_width-20  and mapDict[-(mapX-x_change)+rocket.getX()+x_change,-(mapY-y_change)+rocket.getY()][0]):##
                        rocket.setX(rocket.getX()+x_change)
                if((rocket.getY()-display_height/2)**2>30**2):
                    if(rocket.getY()+y_change>20 and rocket.getY()+y_change<display_height-20  and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()+y_change][0]):##
                        rocket.setY(rocket.getY()+y_change)
                
        if mapY-y_change>=-stageHeight+display_height and mapY-y_change<=0 and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()][0]:##DONE
            mapY=mapY-y_change
            if (rocket.getX()-display_width/2)**2+(rocket.getY()-display_height/2)**2>20**2:
                if((rocket.getX()-display_width/2)**2>30**2):
                    if(rocket.getX()+x_change>20 and rocket.getX()+x_change<display_width-20 and mapDict[-(mapX-x_change)+rocket.getX()+x_change,-(mapY-y_change)+rocket.getY()][0]):##
                        rocket.setX(rocket.getX()+x_change)
                if((rocket.getY()-display_height/2)**2>30**2):
                    if(rocket.getY()+y_change>20 and rocket.getY()+y_change<display_height-20 and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()+y_change][0]):##
                        rocket.setY(rocket.getY()+y_change)


    #map position does not update and only player moves
        if mapX-x_change<=-stageWidth+display_width or mapX-x_change >=0:
            if(rocket.getX()+x_change>20 and rocket.getX()+x_change<display_width-20 and mapDict[-(mapX)+rocket.getX()+x_change,-(mapY)+rocket.getY()][0]):##
                rocket.setX(rocket.getX()+x_change)
        if mapY-y_change<=-stageHeight+display_height or mapY-y_change >=0:
            if(rocket.getY()+y_change>20 and rocket.getY()+y_change<display_height-20 and mapDict[-(mapX)+rocket.getX(),-(mapY)+rocket.getY()+y_change][0]):##
                rocket.setY(rocket.getY()+y_change)


    #Draw map background
        gameDisplay.blit(townShopsImg, (mapX, mapY))
    #printing the character as x and y as its center instead of the top corner
        rocket.display(rocket.getX()-rocket.getXScale()/2, rocket.getY()-rocket.getYScale()/2)
        

#displays items on map, respawns items wrt respawnTimer
        for k,v in itemLocationDict.items():
            if v[1] and v[0][0]>-mapX and v[0][0]<-mapX+display_width and v[0][1] > -mapY and v[0][1] <-mapY+display_height:
                
                gameDisplay.blit(itemDict[k][0],(v[0][0]-(-mapX),v[0][1]-(-mapY)))
                gameDisplay.blit(itemLine,(v[0][0]-(-mapX),v[0][1]-(-mapY)))
                
            #item respawner
            if int(pygame.time.get_ticks()/1000)%respawnTimer==0:
                v[1]=True
                
                
                
        #EVENT HANDLING IDEA
        #EVENT(rocket,mapDict,mapLocation)
        if showInventory:
            rocket.displayInventory()
        if rocket.getStage()!=currentStageNum:
            stageDict[currentStageNum][4][0]=rocket.getX()
            stageDict[currentStageNum][4][1]=rocket.getY()
            stageDict[currentStageNum][5][0]=mapX
            stageDict[currentStageNum][5][1]=mapY
            
            townExit=True

        pygame.display.update()
        clock.tick(60)
#respawnTimer for item respawns
respawnTimer=25     

##def townEnterLoop(rocket,itemLocationDict): #need an input(rocket)?
##    x_change = 0
##    y_change = 0
##    bgCount = 0
##    walkSpeed=2
##    bulletList = []
##    mapX=0
##    mapY=0
##    #charImg=''
##    #rocket.setImg(charImg)
##    ##    bossList=[]
##    ##    bossList.append(Boss())
##    townShopsImg=pygame.image.load('townShops.png')
##    boss = Boss('ship3.png')
##
##    #Stage Dimensions
##    stageWidth=2000  #stageWidth=Stage.getWidth()
##    stageHeight=2000 #stageHeight=stage.getHeight()
##    townShopsImg=pygame.transform.scale(townShopsImg, (stageWidth, stageHeight))
##
##    #itemLocationDict implemented as Global Variable with itemDict
##    #itemLocationDict={'testItem1':[(650,480),True],'testItem2':[(650,550),True]}
##    itemLocationDictNames={}
##    townExit = False
##    #mapDict=mapInitializer() #mapCreator.py script and pickled as map1.pkl to save load time
##    mapDict=load_obj('map1')
##    #mapDict=np.load('my_file.npy').item()
##    showInventory=False
##    trueFalse=[True,False]
##    trueFalseCount=0
##    aniCount=0
##    leftAnimation=['invis_leftStationary.png','invis_leftStationary.png','invis_leftStationary.png','invis_leftStationary.png','invis_leftMove.png','invis_leftMove.png','invis_leftMove.png','invis_leftMove.png']
##    rightAnimation=['invis_rightStationary.png','invis_rightStationary.png','invis_rightStationary.png','invis_rightStationary.png','invis_rightMove.png','invis_rightMove.png','invis_rightMove.png','invis_rightMove.png']
##    upAnimation=['invis_upStationary.png','invis_upStationary.png','invis_upStationary.png','invis_upStationary.png','invis_upMove.png','invis_upMove.png','invis_upMove.png','invis_upMove.png']
##    downAnimation=['invis_downStationary.png','invis_downStationary.png','invis_downStationary.png','invis_downStationary.png','invis_downMove.png','invis_downMove.png','invis_downMove.png','invis_downMove.png']
##    while not townExit:
##        for event in pygame.event.get():
##            if event.type == pygame.QUIT:
##                #save_obj(rocket,'myRocket')
##                #np.save('my_rocket.npy', rocket)
##                gameExit = True
##                pygame.quit()
##                
##            if x_change==-walkSpeed:
##                rocket.setImg(leftAnimation[aniCount])
##                aniCount=(aniCount+1)%len(leftAnimation)#remove this len function for speed later
##            if x_change==walkSpeed:
##                rocket.setImg(rightAnimation[aniCount])
##                aniCount=(aniCount+1)%len(rightAnimation)
##            if y_change==-walkSpeed:
##                rocket.setImg(upAnimation[aniCount])
##                aniCount=(aniCount+1)%len(upAnimation)
##            if y_change==walkSpeed:
##                rocket.setImg(downAnimation[aniCount])
##                aniCount=(aniCount+1)%len(downAnimation)         
##
##            if event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_LEFT:
##                    x_change = -walkSpeed
##                elif event.key == pygame.K_RIGHT:
##                    x_change = walkSpeed
##                elif event.key == pygame.K_UP:
##                    y_change = -walkSpeed
##                elif event.key == pygame.K_DOWN:
##                    y_change = walkSpeed
##                elif event.key == pygame.K_SPACE:
##                    pass
##                elif event.key == pygame.K_i:
##                    showInventory=trueFalse[trueFalseCount%2]
##                    trueFalseCount+=1
##                elif event.key == pygame.K_a:
##                    #
##                    itemEventHandle(rocket,(mapX,mapY),mapDict,itemLocationDict)
##                elif event.key == pygame.K_o:
##                    itemDropHandle(rocket)
##                elif event.key == pygame.K_TAB:
##                    #rocket.swapAmmo()
##                    pass
##            if event.type == pygame.KEYUP:
##                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
##                    x_change = 0
##                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
##                    y_change = 0
##        if x_change==-walkSpeed:
##            rocket.setImg(leftAnimation[aniCount])
##            aniCount=(aniCount+1)%len(leftAnimation)#remove this len function for speed later
##        if x_change==walkSpeed:
##            rocket.setImg(rightAnimation[aniCount])
##            aniCount=(aniCount+1)%len(rightAnimation)
##        if y_change==-walkSpeed:
##            rocket.setImg(upAnimation[aniCount])
##            aniCount=(aniCount+1)%len(upAnimation)
##        if y_change==walkSpeed:
##            rocket.setImg(downAnimation[aniCount])
##            aniCount=(aniCount+1)%len(downAnimation)
##
##    #Draw map background
##        gameDisplay.blit(townShopsImg, (mapX, mapY))
##        
##  #map poistion updates if it is in bounds, and player moves until centered        
##        if mapX-x_change>=-stageWidth+display_width and mapX-x_change<0 and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()][0]:##DONE
##            mapX=mapX-x_change
##            if (rocket.getX()-display_width/2)**2+(rocket.getY()-display_height/2)**2>20**2:
##                if((rocket.getX()-display_width/2)**2>30**2):
##                    if(rocket.getX()+x_change>20 and rocket.getX()+x_change<display_width-20  and mapDict[-(mapX-x_change)+rocket.getX()+x_change,-(mapY-y_change)+rocket.getY()][0]):##
##                        rocket.setX(rocket.getX()+x_change)
##                if((rocket.getY()-display_height/2)**2>30**2):
##                    if(rocket.getY()+y_change>20 and rocket.getY()+y_change<display_height-20  and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()+y_change][0]):##
##                        rocket.setY(rocket.getY()+y_change)
##                
##        if mapY-y_change>=-stageHeight+display_height and mapY-y_change<=0 and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()][0]:##DONE
##            mapY=mapY-y_change
##            if (rocket.getX()-display_width/2)**2+(rocket.getY()-display_height/2)**2>20**2:
##                if((rocket.getX()-display_width/2)**2>30**2):
##                    if(rocket.getX()+x_change>20 and rocket.getX()+x_change<display_width-20 and mapDict[-(mapX-x_change)+rocket.getX()+x_change,-(mapY-y_change)+rocket.getY()][0]):##
##                        rocket.setX(rocket.getX()+x_change)
##                if((rocket.getY()-display_height/2)**2>30**2):
##                    if(rocket.getY()+y_change>20 and rocket.getY()+y_change<display_height-20 and mapDict[-(mapX-x_change)+rocket.getX(),-(mapY-y_change)+rocket.getY()+y_change][0]):##
##                        rocket.setY(rocket.getY()+y_change)
##
##    #printing the character as x and y as its center instead of the top corner
##        rocket.display(rocket.getX()-rocket.getXScale()/2, rocket.getY()-rocket.getYScale()/2)
##    #map position does not update and only player moves
##        if mapX-x_change<=-stageWidth+display_width or mapX-x_change >=0:
##            if(rocket.getX()+x_change>20 and rocket.getX()+x_change<display_width-20 and mapDict[-(mapX)+rocket.getX()+x_change,-(mapY)+rocket.getY()][0]):##
##                rocket.setX(rocket.getX()+x_change)
##        if mapY-y_change<=-stageHeight+display_height or mapY-y_change >=0:
##            if(rocket.getY()+y_change>20 and rocket.getY()+y_change<display_height-20 and mapDict[-(mapX)+rocket.getX(),-(mapY)+rocket.getY()+y_change][0]):##
##                rocket.setY(rocket.getY()+y_change)
##
###displays items on map, respawns items wrt respawnTimer
##        for k,v in itemLocationDict.items():
##            if v[1] and v[0][0]>-mapX and v[0][0]<-mapX+display_width and v[0][1] > -mapY and v[0][1] <-mapY+display_height:
##                
##                gameDisplay.blit(itemDict[k][0],(v[0][0]-(-mapX),v[0][1]-(-mapY)))
##                gameDisplay.blit(itemLine,(v[0][0]-(-mapX),v[0][1]-(-mapY)))
##                
##            #item respawner
##            if int(pygame.time.get_ticks()/1000)%respawnTimer==0:
##                v[1]=True
##                
##                
##                
##        #EVENT HANDLING IDEA
##        #EVENT(rocket,mapDict,mapLocation)
##        if showInventory:
##            rocket.displayInventory()                    
##
##        pygame.display.update()
##        clock.tick(60)
###respawnTimer for item respawns
##respawnTimer=25

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
        
    

#Map Generator-sets obstacles and options wrt to position
#To save time preload initialized map from datafile into mapDict
def mapInitializer():
    mapDict={}
    def passage(x1,x2,y1,y2):
        for i in range(x1,x2):
            for j in range(y1,y2):
                mapDict[(i,j)][0]=True       
    def blockage(x1,x2,y1,y2):
        for i in range(x1,x2):
            for j in range(y1,y2):
                mapDict[(i,j)][0]=False
    def block(x,y):
        mapDict[(x,y)][0]=False
    def open(x,y):
        mapDict[(x,y)][0]=True

    def mapGenerator():
        image = cv2.imread('townShopRed.jpg')
        boundaries=[([17,15,220],[50,56,240])]
        # loop over the boundaries

        lower = np.array(boundaries[0][0], dtype = "uint8")
        upper = np.array(boundaries[0][1], dtype = "uint8")
         
                # find the colors within the specified boundaries and apply
                # the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask = mask)

        mapInfo=[[0 for x in range(len(output[0]))] for y in range(len(output))]
#for every row in output...theyre switched because of cv2?
        for i in range(len(output[0])):
            #for every col in output...
            for j in range(len(output)):
                #NOTE***col and row reverse order for output
                if sum(output[j][i])>100:
                    mapInfo[i][j]=1
        for i in range(len(mapInfo)):
            for j in range(len(mapInfo[0])):
                if mapInfo[i][j]==1:
                    mapDict[(i,j)][0]=False

  
    for i in range(2000):
        for j in range(2000):
            #every position has an extra 3 properties
            mapDict.setdefault((i,j),[True,0,0,0])

    mapGenerator()
    #Obstable Creation Example:
    #House 1
    #blockage(x1,x2,y1,y2)
    #blockage(320,530,220,400)#(x1,x2,y1,y2)
    #passage(x1,x2,y1,y2)
    #passage(400,440,370,400)

    return mapDict
    

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
            currentStage=stage(rocket)
            areaEnterLoop(rocket,currentStage)
            print('Trying to Enter Stage 2 Now....')

#new Game Implementation end ---------------

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

