import pygame
from globals import *


class Block(pygame.sprite.Sprite):

    def __init__(self, image):
        super(Block, self).__init__()

        self.image = image

        self.rect = self.image.get_rect()

        self.rect.centerx = SCREEN_WIDTH//2
        self.rect.centery = SCREEN_HEIGHT - self.image.get_height()/2 - 45

    def update(self):
    	pass