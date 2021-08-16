import pygame
import os
from globals import *

def loadAnimationFiles(screen, entityAssetsPath, animationFolder):
        animationFilesNamesList = [int(num[0]) for num in os.listdir(os.path.join(entityAssetsPath, animationFolder))]
        animationFilesNamesList.sort()

        animationFilesList = []

        #TODO: ADD CONVERT_ALPHA
        for animationFilesName in animationFilesNamesList:
            animationFilesList.append(pygame.image.load(os.path.join(entityAssetsPath, animationFolder, str(animationFilesName) + '.png')).convert_alpha())


        return animationFilesList

def pygameSetup():

	heroAssetsPath = '/home/cincottash/Documents/codingProjects/myGame/assets/hero/'

	pygame.init()

	clock = pygame.time.Clock()

	backgroundImages = []

	backgroundAssetsDir = '/home/cincottash/Documents/codingProjects/myGame/assets/background/'

	backgroundFileNames = os.listdir(backgroundAssetsDir)

	for filename in backgroundFileNames:
		#print(filename)
		backgroundImages.append(pygame.image.load(backgroundAssetsDir + filename))


	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	#has a list of all the files used for each animaitons	
	heroAnimations = {
        'idle': loadAnimationFiles(screen, heroAssetsPath, 'idle'),
        'run': loadAnimationFiles(screen, heroAssetsPath, 'run'),
        'jump_rise': loadAnimationFiles(screen, heroAssetsPath, 'jump_rise'),
        'jump_mid': loadAnimationFiles(screen, heroAssetsPath, 'jump_mid'),
        'jump_fall': loadAnimationFiles(screen, heroAssetsPath, 'jump_fall')
    }

	return screen, backgroundImages, clock, heroAnimations
