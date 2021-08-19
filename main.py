from setup import *
from player import *
from block import *

def main():
	screen, backgroundImages, clock, heroAnimations, blockImages = pygameSetup()
	
	done = False

	playerSpriteGroup = pygame.sprite.Group()
	player = Player(heroAnimations)
	playerSpriteGroup.add(player)

	blocksSpriteGroup = pygame.sprite.Group()
	grassBlock = Block(blockImages['grass'])
	blocksSpriteGroup.add(grassBlock)


	while(not done):

		
		for event in pygame.event.get():
			#Enter will exit the test
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				pygame.quit()
				done = True
			elif event.type == pygame.QUIT:
				pygame.quit()
				done = True

		keysPressed = pygame.key.get_pressed()

		blocksSpriteGroup.update()
		playerSpriteGroup.update(keysPressed)
		

		for image in backgroundImages:
			screen.blit(image, (0,0))
		
		blocksSpriteGroup.draw(screen)
		playerSpriteGroup.draw(screen)
		

		clock.tick(60)
		pygame.display.update()

if __name__ == '__main__':
    main()

