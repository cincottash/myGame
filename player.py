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

        self.atTopEdge = False
        self.atBottomEdge = False
        self.atLeftEdge = False
        self.atRightEdge = False

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

        if self.ay > MAX_ACCELERATION:
            self.ay = MAX_ACCELERATION
        elif self.ay < -MAX_ACCELERATION:
            self.ay = -MAX_ACCELERATION
        # self.ax = min(abs(self.ax), MAX_ACCELERATION)*self.ax/abs(self.ax)
        # self.ay = min(abs(self.ay), MAX_ACCELERATION)*self.ay/abs(self.ay)


    #keeps -MAX_VELOCITY < vx, vy < MAX_VELOCITY
    def normalizeVelocity(self):
        if self.vx < -MAX_VELOCITY:
            self.vx = -MAX_VELOCITY
        elif self.vx > MAX_VELOCITY: 
            self.vx = MAX_VELOCITY

        if self.vy > MAX_VELOCITY:
            self.vy = MAX_VELOCITY
        elif self.vy < -MAX_VELOCITY:
            self.vy = -MAX_VELOCITY

        # self.vx = min(abs(self.vx), MAX_VELOCITY)*self.vx/abs(self.vx)
        # self.vy = min(abs(self.vy), MAX_VELOCITY)*self.vy/abs(self.vy)


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

    def resetMotionX(self):
        self.ax = self.vx = 0

    def resetMotionY(self):
        self.ay = self.vy = 0

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

    def checkCollision(self, blocksSpriteGroup):

        #CHECK IF WE'RE AT BORDER (L/R) OF SCREEN
        self.atLeftEdge = self.atRightEdge = self.atTopEdge = self.atBottomEdge = False

        #Left
        if self.rect.left <= 0:
            self.rect.left = 0

            #let us instantly turn around if we're at the edge of the map
            self.resetMotionX()

            self.atLeftEdge = True
        #Right
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

            #let us instantly turn around if we're at the edge of the map
            self.resetMotionX()

            self.atRightEdge = True
        
        #bottom
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.atBottomEdge = True
        #top
        elif self.rect.top < 0:
            self.rect.top = 0
            self.atTopEdge = True

        # if self.rect.left == 0:
        #     self.atLeftEdge = True
        # elif self.rect.right == SCREEN_WIDTH:
        #     self.atRightEdge = True
        
            #self.resetMotionY()

        # #TODO: check for collison with blocks
        # for block in blocksSpriteGroup:
        #     if pygame.sprite.collide_rect(block, self):
        #         print('collide\n')
                
        #         #RIGHT EDGE
        #         if self.rect.right >= block.rect.left:
        #             self.rect.right = block.rect.left
        #             self.atRightEdge = True
                    
        #             self.resetMotionX()
                    
    # the new image we just assigned might have a different size than the
    # previous image, better update the rect
    def createImageRect(self):

        if self.atRightEdge:
            print('1\n')
            bottomRight = self.rect.bottomright

            self.rect = self.image.get_rect()

            self.rect.bottomright = bottomRight

        elif self.atLeftEdge:
            print('2\n')
            bottomLeft= self.rect.bottomleft

            self.rect = self.image.get_rect()

            self.rect.bottomleft = bottomLeft

        #else it doesn't matter so just us the left edge
        else:
            print('3\n')
            bottomLeft= self.rect.bottomleft

            self.rect = self.image.get_rect()

            self.rect.bottomleft = bottomLeft




        print(f'ax:{self.ax}\nvx:{self.vx}\nay:{self.ay}\nvy:{self.vy}\natLeftEdge:{self.atLeftEdge}\natRightEdge:{self.atRightEdge}\natTopEdge:{self.atTopEdge}\natBottomEdge:{self.atBottomEdge}\n')

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
        if self.rect.bottom >= SCREEN_HEIGHT:
            return True
        return False

    '''

        check what animation we should be showing
        check if we are showing that animation
        if not, update self.currentAnimation, reset self.animationFrame, and
        update self.image

    '''

    def handleAnimationChange(self, keysPressed):
        self.image = self.animations[self.currentAnmiation][self.animationFrame]

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

    def update(self, keysPressed, blocksSpriteGroup):

        self.moveHero(keysPressed)

        self.checkCollision(blocksSpriteGroup)

        self.updatePlayerAnimation(keysPressed)
