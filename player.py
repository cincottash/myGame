import pygame
import os
from globals import *
class Player(pygame.sprite.Sprite):


    def __init__(self):
        super(Player, self).__init__()

        self.animationFrame = 0

        self.idleAnimationList = []

        heroPath = '/home/cincottash/Documents/codingProjects/myGame/assets/hero/'

        idleFileNames = os.listdir(os.path.join(heroPath, 'idle'))

        idleFileNames = idleFileNames[::-1]

        for fileName in idleFileNames:
            self.idleAnimationList.append(pygame.image.load(os.path.join(heroPath,'idle', fileName)))

        self.image = self.idleAnimationList[0]

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH/2
        self.rect.centery = SCREEN_HEIGHT/2

    #def checkScreenCollision(self, keysPressed, HERO_HEIGHT, HERO_WIDTH):

    def update(self, keysPressed):

        HERO_HEIGHT = self.rect.height
        HERO_WIDTH = self.rect.width

        for key in keysPressed:
            if key == 'w':
                #CHECK IF WE GO OFF THE SCREEN
                if self.rect.centery - MOVE_SPEED - HERO_HEIGHT/2 < 0:
                    self.rect.centery =  0 + HERO_HEIGHT/2
                else:
                    self.rect = self.rect.move(0, -MOVE_SPEED)
            if key == 'a':
                if self.rect.centerx - HERO_WIDTH/2 - MOVE_SPEED < 0:
                    self.rect.centerx = 0 + HERO_WIDTH/2
                else:
                    self.rect = self.rect.move(-MOVE_SPEED, 0)
            if key == 's':
                if self.rect.centery + MOVE_SPEED + HERO_HEIGHT/2 > SCREEN_HEIGHT:
                    self.rect.centery =  SCREEN_HEIGHT - HERO_HEIGHT/2
                else:
                    self.rect = self.rect.move(0, MOVE_SPEED)
            if key == 'd':
                if self.rect.centerx + HERO_WIDTH/2 + MOVE_SPEED > SCREEN_WIDTH:
                    self.rect.centerx = SCREEN_WIDTH - HERO_WIDTH/2
                else:
                    self.rect = self.rect.move(MOVE_SPEED, 0)

        
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

