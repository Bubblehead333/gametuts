# 3 Moving Images

import pygame

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Race Game')
clock = pygame.time.Clock()

carImg = pygame.image.load('/home/pi/gametuts/images/car_01.png')

def car (x, y):
	gameDisplay.blit(carImg, (x,y))
	
x = (display_width * 0.45)
y = (display_height * 0.8)

# Defining movement values
x_change = 0

y_change = 0

crashed = False

while not crashed:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			crashed = True
			
		# Event listener for keyboard input	
		if event.type == pygame.KEYDOWN:
			# Defining Left arrow input
			if event.key == pygame.K_LEFT:
				x_change = -5
			# Defining Right arrow input
			elif event.key == pygame.K_RIGHT:
				x_change = 5
		
		# Makes sure movement is halted when key press has stopped
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				x_change = 0
		
	x += x_change
		
	
	gameDisplay.fill(white)
	car(x,y)
	pygame.display.update()
	clock.tick(60)
	
pygame.quit()
quit()
		
		
