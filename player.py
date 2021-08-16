import pygame
import os
from globals import *

class Player(pygame.sprite.Sprite):

    def __init__(self, animations):
        super(Player, self).__init__()

        self.horizontalFlip = False

        self.vx = 0

        self.vy = 0
        
        self.ax = 0

        self.ay = 0

        self.currentAnmiation = 'idle'

        self.animationFrame = 0

        self.animations = animations

        self.image = self.animations[self.currentAnmiation][0]

        self.rect = self.image.get_rect()

        self.rect.centerx = SCREEN_WIDTH/2
        self.rect.centery = SCREEN_HEIGHT/2


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

    #TODO: DAMPEN AY,VY SO WE CAN PROPERLY HANDLE JUMPS

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

        if keysPressed[pygame.K_w]:
            #check if we are on the ground, no mid air jumps
            if(self.rect.centery == SCREEN_HEIGHT - HERO_HEIGHT/2):
                self.ay = 0 
                self.vy = -MAX_VELOCITY

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

        #top
        if self.rect.centery - HERO_HEIGHT/2 < 0:
            self.rect.centery =  0 + HERO_HEIGHT/2
        
        #Left
        if self.rect.centerx - HERO_WIDTH/2 < 0:
            self.rect.centerx = 0 + HERO_WIDTH/2
        
        #Bottom
        if self.rect.centery + HERO_HEIGHT/2 > SCREEN_HEIGHT:
            self.rect.centery = SCREEN_HEIGHT - HERO_HEIGHT/2
        
        #Right
        if self.rect.centerx + HERO_WIDTH/2 > SCREEN_WIDTH:
            self.rect.centerx = SCREEN_WIDTH - HERO_WIDTH/2

        
    def createImageRect(self):
        #keep track of old botomleft

        #THE NEW RECTS SHOULD HAVE THE SAME BOTTOMLEFT COORDS
        bottomLeft = self.rect.bottomleft

        #the new image we just assigned might have a different size than the previous image, better update the rect
        self.rect = self.image.get_rect()

        self.rect.bottomleft = bottomLeft

        print('ax:{}\nvx:{}\nay:{}\nvy:{}\ncenterx:{}\ncentery:{}\n:heroWidth:{}\n'.
            format(self.ax, self.vx, self.ay, self.vy, self.rect.centerx, self.rect.centery, self.rect.width))

    #go to the next animation frame or reset if at the last frame
    def incrementAnimationFrame(self):
        #check if we are at end of animation 
        if self.animationFrame == len(self.animations[self.currentAnmiation]) - 1:
            self.animationFrame = 0
        else:
            self.animationFrame += 1

    def checkAnimation(self, animation):
        return animation == self.currentAnmiation

    def setAnimation(self, animation):
            
        self.currentAnmiation = animation
        self.animationFrame = 0

        self.image = self.animations[self.currentAnmiation][self.animationFrame]

    #flip image if we are running left
    def handleHorizontalFlip(self):
        if self.horizontalFlip:
            self.image = pygame.transform.flip(self.image, True, False)

    def standingOnObject(self):
        HERO_HEIGHT = self.rect.height

        #is he on the floor?
        if self.rect.centery == int(SCREEN_HEIGHT - HERO_HEIGHT/2):
            return True
        return False

    #checks if we should change the animation for the player
    def handleAnimationChange(self, keysPressed):
        self.image = self.animations[self.currentAnmiation][self.animationFrame]

        #check if hero is standing on something or if he is falling

        
        '''
    
        check what animation we should be showing
        check if we are showing that animation
        if not, update self.currentAnimation, reset self.animationFrame, and update self.image

        '''
        if not (keysPressed[pygame.K_d] or keysPressed[pygame.K_a]):
            animation = 'idle'
            
            if not self.checkAnimation(animation):
                self.setAnimation(animation)

        
        if keysPressed[pygame.K_d] or keysPressed[pygame.K_a]:
            animation = 'run'
            
            if not self.checkAnimation(animation):
                self.setAnimation(animation)
        
        #handle jumping condition
        if self.vy < 0:
            animation = 'jump_rise'
            if not self.checkAnimation(animation):
                self.setAnimation(animation)

        #IF HE IS NOT STANDING ON SOMETHING AND VY > 0
        if not self.standingOnObject() and self.vy > 0:
            animation = 'jump_fall'
            if not self.checkAnimation(animation):
                self.setAnimation(animation)

        
        self.handleHorizontalFlip()

        

    def updatePlayerAnimation(self, keysPressed):

        self.incrementAnimationFrame()

        self.handleAnimationChange(keysPressed)

        self.createImageRect()

    def update(self, keysPressed):

        self.moveHero(keysPressed)

        self.keepHeroOnScreen()

        self.updatePlayerAnimation(keysPressed)

        
        


        

