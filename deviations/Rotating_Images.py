# Rotating a sprite

# Not going so well, trying to use a special triangle solving function
# but slowly thinking it may not be the best idea!

import pygame
import time
import random
import math
from trianglesolver import solve, degree


pygame.init()

display_width = 800
display_height = 600
car_width = 80

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
road = (160, 160, 160)


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Race Game')
clock = pygame.time.Clock()

carImg = pygame.image.load('/home/pi/gametuts/images/car_01.png')

def car (x, y, angle):
	
	rotateCar = pygame.transform.rotate(carImg, angle)
	gameDisplay.blit(rotateCar, (x,y))
	
def trajectory(acc, angle):
	
	acc = abs(acc)
	angle = abs(acc)
	a,b,c,A,B,C = solve (b = acc, c = acc, A = angle*degree)
	foundLength = a 
	otherAngle = (180 - angle)/2

	a,b,c,A,B,C = solve (a = foundLength, B = otherAngle*degree, A = 90*degree)

	#working out y movement
	y = acc - c

	#working out x movement
	x = b

	return(x, y)
	
def crash():
	message_display('You crashed')
	
		
def game_loop():
	x = (display_width/2)
	y = (display_height/2)

	acc = 0.1
	angle = 0.1

	gameExit = False

	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					acc += -5
				elif event.key == pygame.K_DOWN:
					acc += 5
				if event.key == pygame.K_LEFT:
					angle += 10
				elif event.key == pygame.K_RIGHT:
					angle -= 10
			
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					acc = 0.1
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					acc = 0.1
					

		cords = trajectory(acc, angle)
		
		print(angle)	

		x += cords[0]
		y += cords[1]
		

		# Background colour
		gameDisplay.fill(road)
		
		car(x, y, angle)
					
		
		pygame.display.update()
		clock.tick(10)

game_loop()
pygame.quit()
quit()
		
		
