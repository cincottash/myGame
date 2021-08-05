import pygame
import os
from globals import *
class Player(pygame.sprite.Sprite):


    def __init__(self):
        super(Player, self).__init__()

        self.animationFrame = 0

        self.idleAnimationList = []

        heroPath = '/home/cincottash/Documents/codingProjects/myGame/assets/hero/'

        #TODO: THIS SHIT ISNT SORTED
        idleFileNames = os.listdir(os.path.join(heroPath, 'idle'))

        print(idleFileNames)

        #exit(0)

        for fileName in idleFileNames:
            self.idleAnimationList.append(pygame.image.load(os.path.join(heroPath,'idle', fileName)))

        self.image = self.idleAnimationList[0]

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH/2
        self.rect.centery = SCREEN_HEIGHT/2

    def handleKeyPress(self, keysPressed):
        for key in keysPressed:
            if key == 'w':
                self.rect = self.rect.move(0, -MOVE_SPEED)
            if key == 'a':
                self.rect = self.rect.move(-MOVE_SPEED, 0)
            if key == 's':
                self.rect = self.rect.move(0, MOVE_SPEED)
            if key == 'd':
                self.rect = self.rect.move(MOVE_SPEED, 0)

    #Keeps the hero on the screen
    def keepHeroOnScreen(self, HERO_HEIGHT, HERO_WIDTH):
        if self.rect.centery - HERO_HEIGHT/2 < 0:
            self.rect.centery =  0 + HERO_HEIGHT/2
        
        if self.rect.centerx - HERO_WIDTH/2 < 0:
            self.rect.centerx = 0 + HERO_WIDTH/2
        
        if self.rect.centery + HERO_HEIGHT/2 > SCREEN_HEIGHT:
            self.rect.centery = SCREEN_HEIGHT - HERO_HEIGHT/2
        
        if self.rect.centerx + HERO_WIDTH/2 > SCREEN_WIDTH:
            self.rect.centerx = SCREEN_WIDTH - HERO_WIDTH/2

    #create a new rect for our new hero image
    def updateHeroRectImage(self):
        if self.animationFrame == len(self.idleAnimationList) - 1:
            self.animationFrame = 0
        else:
            self.animationFrame += 1
        
        self.image = self.idleAnimationList[self.animationFrame]

        #keep track of old centerx and centery
        centerx = self.rect.centerx
        centery = self.rect.centery
        
        #make new rect for the new animation frame image (each frame has slightly different sizes so we need to update our rect)
        self.rect = self.image.get_rect()
        self.rect.centery = centery
        self.rect.centerx = centerx

    def update(self, keysPressed):

        HERO_HEIGHT = self.rect.height
        HERO_WIDTH = self.rect.width

        self.handleKeyPress(keysPressed)

        self.keepHeroOnScreen(HERO_HEIGHT, HERO_WIDTH)

        self.updateHeroRectImage()
        


        

