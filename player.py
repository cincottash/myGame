import pygame
import os
from globals import *

class Player(pygame.sprite.Sprite):

    heroPath = '/home/cincottash/Documents/codingProjects/myGame/assets/hero/'

    def __init__(self):
        super(Player, self).__init__()

        self.horizontalFlip = False

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

    
    def loadAnimationFiles(heroPath, animationFolder):
        animationFilesNamesList = [int(num[0]) for num in os.listdir(os.path.join(heroPath, animationFolder))]
        animationFilesNamesList.sort()

        animationFilesList = []

        #TODO: ADD CONVERT_ALPHA
        for animationFilesName in animationFilesNamesList:
            animationFilesList.append(pygame.image.load(os.path.join(heroPath, animationFolder, str(animationFilesName) + '.png')))


        return animationFilesList
        

    #has a list of all the files used for each animaitons
    animations = {
        'idle': loadAnimationFiles(heroPath, 'idle'),
        'run': loadAnimationFiles(heroPath, 'run')
    }


    #keeps -MAX_ACCELERATION < ax, ay < MAX_ACCELERATION
    def normalizeAcceleration(self):
        if self.ax < -MAX_ACCELERATION:
            self.ax = -MAX_ACCELERATION
        elif self.ax > MAX_ACCELERATION:
            self.ax = MAX_ACCELERATION
        
        if self.ay < -MAX_ACCELERATION:
            self.ay = -MAX_ACCELERATION
        elif self.ay > MAX_ACCELERATION:
            self.ay = MAX_ACCELERATION

    #keeps -MAX_VELOCITY < vx, vy < MAX_VELOCITY
    def normalizeVelocity(self):
        if self.vx < -MAX_VELOCITY:
            self.vx = -MAX_VELOCITY
        elif self.vx > MAX_VELOCITY:
            self.vx = MAX_VELOCITY
        
        if self.vy < -MAX_VELOCITY:
            self.vy = -MAX_VELOCITY
        elif self.vy > MAX_VELOCITY:
            self.vy = MAX_VELOCITY

    #simulate friction by reducing/increasing ax by a damping constant
    def dampenAcceleration(self, keysPressed):
        if not(keysPressed[pygame.K_a] or keysPressed[pygame.K_d]):
            
            if self.ax < 0:
                if(self.ax + DAMPING_CONSTANT_A >= 0):
                    self.ax = 0
                else:
                    self.ax += DAMPING_CONSTANT_A
            elif self.ax > 0:
                if(self.ax - DAMPING_CONSTANT_A <= 0):
                    self.ax = 0
                else:
                    self.ax -= DAMPING_CONSTANT_A

    #simulate friction by reducing/increasing vx by a damping constant
    def dampenVelocity(self, keysPressed):
        #only dampen if we aren't pressing a move key
        if not(keysPressed[pygame.K_a] or keysPressed[pygame.K_d]):
            if self.vx < 0:
                if(self.vx + DAMPING_CONSTANT_V >= 0):
                    self.vx = 0
                else:
                    self.vx += DAMPING_CONSTANT_V
            elif self.vx > 0:
                if(self.vx - DAMPING_CONSTANT_V <= 0):
                    self.vx = 0
                else:
                    self.vx -= DAMPING_CONSTANT_V

    def handleKeyPress(self, keysPressed):
        HERO_HEIGHT = self.rect.height

        if keysPressed[pygame.K_SPACE]:
            #check if we are on the ground, no mid air jumps
            if(self.rect.centery == SCREEN_HEIGHT - HERO_HEIGHT/2):
                self.ay = 0 
                self.vy = -MAX_ACCELERATION

        if keysPressed[pygame.K_a]:
            self.ax -= 0.2 * MAX_ACCELERATION
            self.horizontalFlip = True

        if keysPressed[pygame.K_d]:
            self.ax += 0.2 * MAX_ACCELERATION
            self.horizontalFlip = False

    def moveHero(self, keysPressed):
        
        self.handleKeyPress(keysPressed)

        self.ay -= GRAVITY

        self.normalizeAcceleration()
        self.dampenAcceleration(keysPressed)
        
        self.vx += self.ax
        self.vy += self.ay

        self.normalizeVelocity()
        self.dampenVelocity(keysPressed)

        
        #updates the rects coords
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

        

        print('ax:{}\nvx:{}\nay:{}\nvy:{}\ncenterx:{}\ncentery:{}\n:heroWidth:{}\n'.
            format(self.ax, self.vx, self.ay, self.vy, self.rect.centerx, self.rect.centery, self.rect.width))

    def createImageRect(self):
        #keep track of old centerx and centery
        centerx = self.rect.centerx
        centery = self.rect.centery
        
        #the new image we just assigned might have a different size than the previous image, better update the rect
        self.rect = self.image.get_rect()
        self.rect.centery = centery
        self.rect.centerx = centerx

    #go to the next animation frame or reset if at the last frame
    def incrementAnimationFrame(self):
        #check if we are at end of animation 
        if self.animationFrame == len(self.animations[self.currentAnmiation]) - 1:
            self.animationFrame = 0
        else:
            self.animationFrame += 1

    #check if this is a transition to a new animation
    def checkAndSetNewAnimation(self, newAnimation):
        
        if newAnimation != self.currentAnmiation:
            self.currentAnmiation = newAnimation
            self.animationFrame = 0

        self.image = self.animations[self.currentAnmiation][self.animationFrame]

    #flip image if we are running left
    def handleHorizontalFlip(self):
        if self.horizontalFlip:
            self.image = pygame.transform.flip(self.image, True, False)

    #checks if we should change the animation for the player
    def handleAnimationChange(self):
        self.image = self.animations[self.currentAnmiation][self.animationFrame]

        #run animation
        if self.vx != 0:
            self.checkAndSetNewAnimation('run')
            self.handleHorizontalFlip()
                
        else:
            self.checkAndSetNewAnimation('idle')

            self.handleHorizontalFlip()

    def updatePlayerAnimation(self):

        self.incrementAnimationFrame()

        self.handleAnimationChange()

        self.createImageRect()

    def update(self, keysPressed):

        self.moveHero(keysPressed)

        self.updatePlayerAnimation()

        self.keepHeroOnScreen()
        


        

