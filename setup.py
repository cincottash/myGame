import pygame
import os

def pygameSetup():

	pygame.init()

	SCREEN_WIDTH = 928
	SCREEN_HEIGHT = 793

	clock = pygame.time.Clock()

	backgroundImages = []

	backgroundAssetsDir = '/home/cincottash/Documents/codingProjects/myGame/assets/background/'

	backgroundFileNames = os.listdir(backgroundAssetsDir)


	for filename in backgroundFileNames:
		print(filename)
		backgroundImages.append(pygame.image.load(backgroundAssetsDir + filename))


	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	return screen, backgroundImages, clock
