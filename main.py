from setup import *
from player import *

def main():
	screen, backgroundImages, clock = pygameSetup()
	
	done = False

	hero = Player()
	
	while(not done):

		for event in pygame.event.get():
			#Enter will exit the test
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				done = True
			elif event.type == pygame.QUIT:
				done = False
			else:
				for image in backgroundImages:
					screen.blit(image, (0,0))

		clock.tick(30)
		pygame.display.update()

if __name__ == '__main__':
    main()

