# 2 Displaying Images

# Imports the pygame module
import pygame

pygame.init()

# Frame dimensions definitions
display_width = 800
display_height = 600

# Colour definitions RGB values
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Race Game')
clock = pygame.time.Clock()

# Assigning sprite
carImg = pygame.image.load('/home/pi/gametuts/images/car_01.png')

def car (x, y):
	# Putting carImg to game display
	gameDisplay.blit(carImg, (x,y))
	
# Images are referenced by their upper left corner, this offsets
x = (display_width * 0.45)
y = (display_height * 0.8)


crashed = False

while not crashed:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			crashed = True
	
	# Covers display with white
	gameDisplay.fill(white)
	# Displaying car
	car(x,y)
	pygame.display.update()
	clock.tick(60)
	
pygame.quit()
quit()
		
		
