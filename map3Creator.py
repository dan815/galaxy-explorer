import pickle
import pygame
import time
import random
import numpy as np
import argparse
import cv2

def mapInitializer(imgStr):
    mapDict={}
    def passage(x1,x2,y1,y2):
        for i in range(x1,x2):
            for j in range(y1,y2):
                mapDict[(i,j)][0]=True       
    def blockage(x1,x2,y1,y2):
        for i in range(x1,x2):
            for j in range(y1,y2):
                mapDict[(i,j)][0]=False
    def itemSetter(x1,x2,y1,y2,itemStr):
        for i in range(x1,x2):
            for j in range(y1,y2):
                mapDict[(i,j)][1]=True
                mapDict[(i,j)][2]=itemStr
    def stageConnector(x1,x2,y1,y2,newStageNum):
        for i in range(x1,x2):
            for j in range(y1,y2):
                mapDict[(i,j)][3]=True
                mapDict[(i,j)][4]=newStageNum
        
                          
    def block(x,y):
        mapDict[(x,y)][0]=False
    def open(x,y):
        mapDict[(x,y)][0]=True

    def mapGenerator(imgStr):
        image = cv2.imread(imgStr)
        boundaries=[([17,15,220],[50,56,240])]
        # loop over the boundaries
        #initializing dict
        for i in range(len(image[0])):
            for j in range(len(image)):
            #every position has an extra 3 properties
                mapDict.setdefault((i,j),[True,0,0,0,0,0,0,0,0])


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
                    #switch j and i depending on where you save(paint or lunapic)
                    mapInfo[j][i]=1
                    mapDict[(i,j)][0]=False
##
##        for i in range(len(mapInfo)):
##            for j in range(len(mapInfo[0])):
##                if mapInfo[i][j]==1:
##                    mapDict[(i,j)][0]=False
##
##  


    mapGenerator(imgStr)
##    itemSetter(626,698,481,550,'testItem1')
##    itemSetter(626,698,551,600,'testItem2')
    stageConnector(496,530,650,683,1)
    #Obstable Creation Example:
    #House 1
    #blockage(x1,x2,y1,y2)
    #blockage(320,530,220,400)#(x1,x2,y1,y2)
    #passage(x1,x2,y1,y2)
    #passage(400,440,370,400)

    return mapDict


#IMPORTANT MAPDICT FORMAT
#mapDict={(x,y):[collisionBool,itemBool,itemName,stageConnectBool,stageConnectNumber]}
#map1=mapInitializer('townShopRed.jpg')
map3=mapInitializer('libraryRed.png')

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

#save_obj(map1,'map1')
save_obj(map3,'map3')

# Save
##dictionary = {'hello':'world'}
##np.save('my_file.npy', map1) 

### Load
##read_dictionary = np.load('my_file.npy').item()
## # displays "world"
