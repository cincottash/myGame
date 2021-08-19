import pygame
import os
from globals import *

def loadEntityAnimationFiles(screen, entityAssetsPath, animationFolder):
        animationFilesNamesList = [int(num[0]) for num in os.listdir(os.path.join(entityAssetsPath, animationFolder))]
        animationFilesNamesList.sort()

        animationFilesList = []

        for animationFilesName in animationFilesNamesList:
            animationFilesList.append(pygame.image.load(os.path.join(entityAssetsPath, animationFolder, str(animationFilesName) + '.png')).convert_alpha())

        return animationFilesList

def pygameSetup():

	heroAssetsPath = '/home/cincottash/Documents/codingProjects/myGame/assets/hero/'
	blockAssetsPath = '/home/cincottash/Documents/codingProjects/myGame/assets/blocks/'
	backgroundAssetsPath = '/home/cincottash/Documents/codingProjects/myGame/assets/background/'
	pygame.init()

	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	clock = pygame.time.Clock()

	blockImages = {
		'grass': pygame.image.load(os.path.join(blockAssetsPath, 'grass.png')).convert_alpha()

	}

	#TODO: ADD THESE TO DICT LIKE BLOCK IMAGES MAYBE? MAYBE NOT IDK LOL GOODLUCK
	backgroundImages = []

	

	for filename in os.listdir(backgroundAssetsPath):
		#print(filename)
		backgroundImages.append(pygame.image.load(os.path.join(backgroundAssetsPath, filename)))


	#has a list of all the files used for each animaitons	
	heroAnimations = {
        'idle': loadEntityAnimationFiles(screen, heroAssetsPath, 'idle'),
        'run': loadEntityAnimationFiles(screen, heroAssetsPath, 'run'),
        'jump_rise': loadEntityAnimationFiles(screen, heroAssetsPath, 'jump_rise'),
        'jump_fall': loadEntityAnimationFiles(screen, heroAssetsPath, 'jump_fall')
    }

	return screen, backgroundImages, clock, heroAnimations, blockImages
