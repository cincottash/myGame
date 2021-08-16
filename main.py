from setup import *
from player import *

def main():
	screen, backgroundImages, clock, heroAnimations = pygameSetup()
	
	done = False

	playerSpriteGroup = pygame.sprite.Group()
	player = Player(heroAnimations)
	playerSpriteGroup.add(player)
	
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

		playerSpriteGroup.update(keysPressed)

		for image in backgroundImages:
			screen.blit(image, (0,0))
		
		playerSpriteGroup.draw(screen)

		clock.tick(120)
		pygame.display.update()

if __name__ == '__main__':
    main()

