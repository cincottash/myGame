import pygame
import os
from globals import *

class Player(pygame.sprite.Sprite):

    def __init__(self, animations):
        super(Player, self).__init__()

        self.horizontalFlip = False

        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0

        self.atRightEdgeOfMap = False
        self.atLeftEdgeOfMap = False
        self.atTopEdgeOfMap = False
        self.atBottomEdgeOfMap = False

        self.atLeftEdgeOfBlock = False
        self.atRightEdgeOfBlock = False
        self.atTopEdgeOfBlock = False
        self.atBottomEdgeOfBlock = False

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

    #simulate friction by reducing/increasing ax by a damping constant
    def dampenAcceleration(self, keysPressed):
        if not(keysPressed[pygame.K_a] or keysPressed[pygame.K_d]):

            if self.ax < 0:
                if(self.ax + DAMPING_CONSTANT_A >= 0):
                    self.ax = 0.0
                else:
                    self.ax += DAMPING_CONSTANT_A
            elif self.ax > 0:
                if(self.ax - DAMPING_CONSTANT_A <= 0):
                    self.ax = 0.0
                else:
                    self.ax -= DAMPING_CONSTANT_A

    #simulate friction by reducing/increasing vx by a damping constant
    def dampenVelocity(self, keysPressed):
        #only dampen if we aren't pressing a move key
        if not(keysPressed[pygame.K_a] or keysPressed[pygame.K_d]):
            if self.vx < 0:
                if(self.vx + DAMPING_CONSTANT_V >= 0):
                    self.vx = 0.0
                else:
                    self.vx += DAMPING_CONSTANT_V
            elif self.vx > 0:
                if(self.vx - DAMPING_CONSTANT_V <= 0):
                    self.vx = 0.0
                else:
                    self.vx -= DAMPING_CONSTANT_V

    def resetMotionX(self):
        self.ax = self.vx = 0.0

    def resetMotionY(self):
        self.ay = self.vy = 0.0


    def handleKeyPress(self, keysPressed):
        HERO_HEIGHT = self.rect.height

        if keysPressed[pygame.K_w]:
            #check if we are on the ground, no mid air jumps
            if(self.rect.centery == SCREEN_HEIGHT - HERO_HEIGHT/2):
                self.ay = 0
                self.vy = -MAX_VELOCITY

        if keysPressed[pygame.K_d]:
            self.ax += 0.2 * MAX_ACCELERATION
            self.horizontalFlip = False

        if keysPressed[pygame.K_a]:
            self.ax -= 0.2 * MAX_ACCELERATION
            self.horizontalFlip = True



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

    def handleBorderCollision(self):
        #Left
        if self.rect.left <= 0:
            self.rect.left = 0

            #let us instantly turn around if we're at the edge of the map
            self.resetMotionX()

            self.atLeftEdgeOfMap = True
        #Right
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

            #let us instantly turn around if we're at the edge of the map
            self.resetMotionX()

            self.atRightEdgeOfMap = True

        #bottom
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.atBottomEdgeOfMap = True
        #top
        elif self.rect.top < 0:
            self.rect.top = 0
            self.atTopEdgeOfMap = True

    def handleBlockCollision(self, blocksSpriteGroup):
        #TODO: check for collison with blocks
        for block in blocksSpriteGroup:
            if pygame.Rect.colliderect(self.rect, block.rect):
                
                
                # Collision at top
                if(self.rect.right >= block.rect.left and self.rect.left <= block.rect.right and self.rect.top <= block.rect.top):
                    print('Collide Top\n')

                    self.atTopEdgeOfBlock = True
                    
                    #update the rect
                    self.rect.bottom = block.rect.top

                    self.resetMotionY()

                # Collision at bottom
                elif(self.rect.right >= block.rect.left and self.rect.left <= block.rect.right and self.rect.bottom >= block.rect.bottom):
                    print('Collide Bottom\n')
                    
                    self.atBottomEdgeOfBlock = True
                    self.rect.top = block.rect.bottom
                    self.resetMotionY()
                
                # Collision at right
                elif(self.rect.bottom >= block.rect.top and self.rect.top <=block.rect.bottom and self.rect.right >=block.rect.right):

                    print('Collide Right\n')
                    self.atRightEdgeOfBlock = True
                    self.rect.left = block.rect.right
                    self.resetMotionX()

                #Collision at left
                elif(self.rect.bottom >= block.rect.top and self.rect.top <= block.rect.bottom and self.rect.left <= block.rect.left):
                    print('Collide Left\n')

                    self.atLeftEdgeOfBlock = True
                    self.rect.right = block.rect.left
                    self.resetMotionX()

    def handleCollisions(self, blocksSpriteGroup):


        self.atRightEdgeOfMap = self.atLeftEdgeOfMap = self.atTopEdgeOfMap = self.atBottomEdgeOfMap = self.atLeftEdgeOfBlock = self.atRightEdgeOfBlock = self.atTopEdgeOfBlock = self.atBottomEdgeOfBlock = False

        self.handleBorderCollision()
        self.handleBlockCollision(blocksSpriteGroup)



    # the new image we just assigned might have a different height than the
    # previous image, better update the rect
    def createImageRect(self):

        if(self.atTopEdgeOfMap or self.atBottomEdgeOfMap or self.atLeftEdgeOfMap or self.atRightEdgeOfMap):

            if self.atTopEdgeOfMap:
                top = self.rect.top

                self.rect = self.image.get_rect()

                self.rect.top = top

            elif self.atBottomEdgeOfMap :
                bottomLeft = self.rect.bottomleft

                self.rect = self.image.get_rect()

                self.rect.bottomleft = bottomLeft
        
        elif self.atTopEdgeOfBlock or self.atBottomEdgeOfBlock or self.atLeftEdgeOfBlock or self.atRightEdgeOfBlock:

            if self.atTopEdgeOfBlock:
                bottomleft = self.rect.bottomleft

                self.rect = self.image.get_rect()

                self.rect.bottomleft = bottomleft

            elif self.atBottomEdgeOfBlock:
                topleft = self.rect.topleft

                self.rect = self.image.get_rect()

                self.rect.topleft = topleft



        print(f'ax:{self.ax}\nvx:{self.vx}\nay:{self.ay}\nvy:{self.vy}\natRightEdgeOfMap:{self.atRightEdgeOfMap}\natLeftEdgeOfMap:{self.atLeftEdgeOfMap}\natTopEdgeOfMap:{self.atTopEdgeOfMap}\natBottomEdgeOfMap:{self.atBottomEdgeOfMap}\natLeftEdge:{self.atLeftEdgeOfBlock}\natRightEdge:{self.atRightEdgeOfBlock}\natTopEdge{self.atTopEdgeOfBlock}\natBottomEdge:{self.atBottomEdgeOfBlock}\nImage Width: {self.image.get_width()}\nImage Height: {self.image.get_height()}\n')

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
        return self.atTopEdgeOfBlock or self.atBottomEdgeOfMap

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
        if  self.vy > 0 and not self.standingOnObject():
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

        self.handleCollisions(blocksSpriteGroup)

        self.updatePlayerAnimation(keysPressed)
