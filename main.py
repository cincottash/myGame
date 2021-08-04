from setup import *
from player import *

def main():
	screen, backgroundImages, clock = pygameSetup()
	
	done = False

	all_sprites = pygame.sprite.Group()
	player = Player()
	all_sprites.add(player)
	
	while(not done):

		for event in pygame.event.get():
			#Enter will exit the test
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				done = True
			elif event.type == pygame.QUIT:
				done = False
			else:
			
				all_sprites.update(event)

				for image in backgroundImages:
					screen.blit(image, (0,0))
				all_sprites.draw(screen)

				clock.tick(60)
				pygame.display.update()

if __name__ == '__main__':
    main()

