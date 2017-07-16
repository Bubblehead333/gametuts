# 6 Drawing Objects

import pygame
from time import sleep
import random

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

def roadlines(roady):
	pygame.draw.rect(gameDisplay, white, [(display_width/2 - 5), roady, 10, 100])
	
def roadlines2(roady):
	pygame.draw.rect(gameDisplay, white, [(display_width/2 - 5), roady, 10, 100])
	
# Define obstacle object
def obstacle(obx, oby, obw, obh, colour):
	pygame.draw.rect(gameDisplay, colour, [obx, oby, obw, obh])

def car (x, y):
	gameDisplay.blit(carImg, (x,y))
	
def crash():
	message_display('You crashed')
	
def message_display(text):
	largeText = pygame.font.Font('freesansbold.ttf', 90)
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = ((display_width/2), (display_height/2))
	gameDisplay.blit(TextSurf, TextRect)

	pygame.display.update()
	time.sleep(3)
	
	game_loop()
	
def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()
	
		
def game_loop():
	x = (display_width * 0.45)
	y = (display_height * 0.8)

	x_change = 0
	
	# Defining obstacle start parameters
	ob_startx = random.randrange(0, display_width)
	ob_starty = -600
	ob_speed = 10
	ob_width = random.randrange(30, 100)
	ob_height = random.randrange(30, 100)
	
	# Roadlines
	roadline_startx = (display_width/2) - 5
	roadline_starty = 0
	roadline_speed = 30
	roadline2_starty = -300



	gameExit = False

	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -5
				elif event.key == pygame.K_RIGHT:
					x_change = 5
			
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change = 0
					
		x += x_change
			
		gameDisplay.fill(road)
		
		roadlines(roadline_starty)
		roadline_starty += roadline_speed
		
		roadlines2(roadline2_starty)
		roadline2_starty += roadline_speed
		
		
		# Creates new object for obstacle
		obstacle(ob_startx, ob_starty, ob_width, ob_height, black)
		ob_starty += ob_speed
		car(x,y)
		
		# Frame boundaries
		if x > display_width - car_width or x < 0:
			crash()
			
		# Whenever the obstacle is off screen, re-define variables
		if ob_starty > display_height:
			ob_starty= 0 - ob_height
			ob_startx = random.randrange(0, display_width)
			ob_width = random.randrange(30, 100)
			ob_height = random.randrange(30, 100)
			
		if roadline_starty > display_height:
			roadline_starty = 0 
		
		if roadline2_starty > display_height:
			roadline2_starty = 0 
			
			
		
		pygame.display.update()
		clock.tick(60)

game_loop()
pygame.quit()
quit()
		
		
