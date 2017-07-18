# 1 Intro to game development for Python 

# Imports the pygame module
import pygame

# Initialises pygame
pygame.init()

# Sets resolution of the main game frame
gameDisplay = pygame.display.set_mode((800,600))

# Window title
pygame.display.set_caption('Race Game')

# Sets game clock
clock = pygame.time.Clock()

crashed = False

# Game loop
while not crashed:
	# Gets events within game loop
	for event in pygame.event.get():
		# Event listener
		if event.type == pygame.QUIT:
			crashed = True
			
		print(event)
		
	# Displays compiled data/processes
	pygame.display.update()
	# FPS
	clock.tick(60)
	
pygame.quit()
quit()
		
		
