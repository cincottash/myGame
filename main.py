from setup import *
from player import *

def main():
	screen, backgroundImages, clock = pygameSetup()
	
	done = False

	all_sprites = pygame.sprite.Group()
	player = Player()
	all_sprites.add(player)
	
	while(not done):

		keysPressed = []
		for event in pygame.event.get():
			#Enter will exit the test
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				done = True
			elif event.type == pygame.QUIT:
				done = False
			else:

				if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
					keysPressed.append('w')
				if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
					keysPressed.append('a')
				if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
					keysPressed.append('s')
				if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
					keysPressed.append('d')
			
		all_sprites.update(keysPressed)

		for image in backgroundImages:
			screen.blit(image, (0,0))
		
		all_sprites.draw(screen)

		clock.tick(60)
		pygame.display.update()

if __name__ == '__main__':
    main()

