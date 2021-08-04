import pygame
import os

class Player(pygame.sprite.Sprite):

    

    def __init__(self):
        super(Player, self).__init__()

        self.animationTypes = ['idle_transition', 'run']

        self.currentAnimationType = self.animationTypes[0]

        self.animationFrame = 0

        self.idleAnimationList = []

        heroPath = '/home/cincottash/Documents/codingProjects/myGame/assets/hero/'

        idleFileNames = os.listdir(os.path.join(heroPath, 'idle_transition'))

        idleFileNames = idleFileNames[::-1]

        for fileName in idleFileNames:
            self.idleAnimationList.append(pygame.image.load(os.path.join(heroPath,'idle_transition', fileName)))

        self.image = self.idleAnimationList[0]

        self.rect = self.image.get_rect()

    def update(self, event):
        #self.rect.y += 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                print('pressed s')
                self.rect.y += 5
        
        if self.animationFrame == len(self.idleAnimationList) - 1:
            self.animationFrame = 0
        else:
            self.animationFrame += 1
        
        self.image = self.idleAnimationList[self.animationFrame]
         