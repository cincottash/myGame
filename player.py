import pygame
import os
from globals import *
import math
class Player(pygame.sprite.Sprite):
    heroPath = '/home/cincottash/Documents/codingProjects/myGame/assets/hero/'

    def loadAnimationFiles(heroPath, animationFolder):
        animationFilesNamesList = [int(num[0]) for num in os.listdir(os.path.join(heroPath, animationFolder))]
        animationFilesNamesList.sort()

        animationFilesList = []

        for animationFilesName in animationFilesNamesList:
            animationFilesList.append(pygame.image.load(os.path.join(heroPath, animationFolder, str(animationFilesName) + '.png')))


        return animationFilesList
        

    #has a list of all the files used for each animaitons
    animations = {
        'idle': loadAnimationFiles(heroPath, 'idle'),
        'run': loadAnimationFiles(heroPath, 'run')
    }

    def __init__(self):
        super(Player, self).__init__()

        self.vx = 0

        self.vy = 0
        
        self.ax = 0

        self.ay = 0

        self.currentAnmiation = 'idle'

        self.animationFrame = 0

        self.image = self.animations[self.currentAnmiation][0]

        self.rect = self.image.get_rect()

        self.rect.centerx = SCREEN_WIDTH/2
        self.rect.centery = SCREEN_HEIGHT/2

    def handleHeroMovement(self, keysPressed):
        if keysPressed[pygame.K_SPACE]:
            self.ay = 0
            self.ay -= 10
            print('pressed space')

        if keysPressed[pygame.K_a]:
            self.ax -= 5
            print('pressed a')

        if keysPressed[pygame.K_s]:
            self.ay += 5
            print('pressed s')

        if keysPressed[pygame.K_d]:
            self.ax += 5
            print('pressed d')

        self.ay -= GRAVITY

        if self.ax < 0 and abs(self.ax) > MAX_ACCELERATION:
            self.ax = -MAX_ACCELERATION
        if self.ax > 0 and abs(self.ax) > MAX_ACCELERATION:
            self.ax = MAX_ACCELERATION
        if self.ay < 0 and abs(self.ay) > MAX_ACCELERATION:
            self.ay = -MAX_ACCELERATION
        if self.ay > 0 and abs(self.ay) > MAX_ACCELERATION:
            self.ay = MAX_ACCELERATION

        self.vx += self.ax
        self.vy += self.ay
        
        if self.vx < 0 and abs(self.vx) > MAX_VELOCITY:
            self.vx = -MAX_VELOCITY
        if self.vx > 0 and abs(self.vx) > MAX_VELOCITY:
            self.vx = MAX_VELOCITY
        if self.vy < 0 and abs(self.vy) > MAX_VELOCITY:
            self.vy = -MAX_VELOCITY
        if self.vy > 0 and abs(self.vy) > MAX_VELOCITY:
            self.vy = MAX_VELOCITY
        
        print('ax:{}\nvx:{}\nay:{}\nvy:{}\ncenterx:{}\ncentery:{}\n:heroWidth:{}\n'.
            format(self.ax, self.vx, self.ay, self.vy, self.rect.centerx, self.rect.centery, self.rect.width))
        self.rect = self.rect.move(self.vx, self.vy)

    def keepHeroOnScreen(self):
        HERO_HEIGHT = self.rect.height
        HERO_WIDTH = self.rect.width

        if self.rect.centery - HERO_HEIGHT/2 < 0:
            self.rect.centery =  0 + HERO_HEIGHT/2
        
        if self.rect.centerx - HERO_WIDTH/2 < 0:
            self.rect.centerx = 0 + HERO_WIDTH/2
        
        if self.rect.centery + HERO_HEIGHT/2 > SCREEN_HEIGHT:
            self.rect.centery = SCREEN_HEIGHT - HERO_HEIGHT/2
        
        if self.rect.centerx + HERO_WIDTH/2 > SCREEN_WIDTH:
            self.rect.centerx = SCREEN_WIDTH - HERO_WIDTH/2

    def updateAnimation(self):

        #check if we are at end of animation 
        if self.animationFrame == len(self.animations[self.currentAnmiation]) - 1:
            self.animationFrame = 0
        else:
            self.animationFrame += 1

        self.image = self.animations[self.currentAnmiation][self.animationFrame]

        #keep track of old centerx and centery
        centerx = self.rect.centerx
        centery = self.rect.centery
        
        #the new image we just assigned might have a different size than the previous image, better update the rect
        self.rect = self.image.get_rect()
        self.rect.centery = centery
        self.rect.centerx = centerx

        #dummy value for initialization
        newAnimation = self.currentAnmiation

        #run animation
        if self.vx != 0 or self.vy != 0:
            newAnimation = 'run'
            
            #check if this is a transition to a new animation
            if newAnimation != self.currentAnmiation:
                self.currentAnmiation = newAnimation
                self.animationFrame = 0
            
            self.image = self.animations[self.currentAnmiation][self.animationFrame]
            
            #flip image if we are running left
            if self.ax < 0:
                self.image = pygame.transform.flip(self.image, True, False)
                
        else:
            newAnimation = 'idle'
            if newAnimation != self.currentAnmiation:
                self.currentAnmiation = newAnimation
                self.animationFrame = 0

    def update(self, keysPressed):

        self.handleHeroMovement(keysPressed)

        self.updateAnimation()

        self.keepHeroOnScreen()
        


        

