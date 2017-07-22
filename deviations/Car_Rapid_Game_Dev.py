# THIS IS EXACTLY WHAT I WANT
# BASIC ROTATION AND CORNERING MECHANICS
# TRY AND UNDERSTAND THIS JOSH

import pygame, math, sys, random
from pygame.locals import *
#
display_height = 800
display_width = 1280
# Sets size of screen
gameDisplay = pygame.display.set_mode((display_width, display_height))

# Initialises clock
clock = pygame.time.Clock()

# Colours
white = (255,255,255)
black = (0,0,0)



class VehicleSprite(pygame.sprite.Sprite):
	# Creates a vehicle class
	MAX_FORWARD_SPEED = 15
	MAX_REVERSE_SPEED = 5
	ACCELERATION = 20
	TURN_SPEED = 50
	
	def __init__(self, image, position):
		# Creates object instance off
		pygame.sprite.Sprite.__init__(self)
		self.src_image = pygame.image.load(image)
		self.position = position
		self.speed = self.direction = 0
		self.k_left = self.k_right = self.k_down = self.k_up = 0
		
	def update(self, time):
		# SIMULATION
		self.speed += (self.k_up +self.k_down)
		if self.speed > self.MAX_FORWARD_SPEED:
			self.speed = self.MAX_FORWARD_SPEED
		if self.speed < -self.MAX_REVERSE_SPEED:
			self.speed = -self.MAX_REVERSE_SPEED
			
		# Degrees sprite is facing
		self.direction += (self.k_right + self.k_left)
		x, y = self.position
		rad = self.direction * math.pi / 180
		x += -self.speed*math.sin(rad)
		y += -self.speed*math.cos(rad)
		self.position = (x, y)
		self.image = pygame.transform.rotate(self.src_image, self.direction)
		self.rect = self.image.get_rect()
		self.rect.center = self.position
		
class Projectile(pygame.sprite.Sprite):
	MAX_FORWARD_SPEED = 20
	
	def __init__(self, image, position):
		# Creates object instance off
		pygame.sprite.Sprite.__init__(self)
		self.src_image = pygame.image.load(image)
		self.position = position
		self.speed = self.direction = 0
		self.k_left = self.k_right = self.k_down = self.k_up = 0
		
	def update(self, time):
		# SIMULATION
		self.speed += (self.k_up +self.k_down)
		if self.speed > self.MAX_FORWARD_SPEED:
			self.speed = self.MAX_FORWARD_SPEED
		self.direction += (self.k_right + self.k_left)
		x, y = self.position
		rad = self.direction * math.pi / 180
		x += -self.speed*math.sin(rad)
		y += -self.speed*math.cos(rad)
		self.position = (x, y)
		self.image = pygame.transform.rotate(self.src_image, self.direction)
		self.rect = self.image.get_rect()
		self.rect.center = self.position


	
# CREATE A CAR AND TUN
rect = gameDisplay.get_rect()

# Car image load
car = VehicleSprite('/home/pi/gametuts/images/car_01.png', rect.center)
car_group = pygame.sprite.RenderPlain(car)

# Bike image load
bike = VehicleSprite('/home/pi/gametuts/images/blueBike2.png', rect.center)
bike_group = pygame.sprite.RenderPlain(bike)

# Ball image load
ball = Projectile('/home/pi/gametuts/images/ironball.png', rect.center)
ball_group = pygame.sprite.RenderPlain(ball)

# Main game loop
def game_loop():
	
	# Defining obstacle start parameters
	ob_startx = random.randrange(0, display_width)
	ob_starty = -600
	ob_speed = 10
	ob_width = random.randrange(30, 100)
	ob_height = random.randrange(30, 100)
	
	while 1:
		#USER INPUT
		# Sets frame rate
		time = clock.tick(30)
		for event in pygame.event.get():
			if not hasattr(event, 'key'): continue
			down = event.type == KEYDOWN
			# Car Input (Player 1)
			if event.key == K_RIGHT: car.k_right = down * -5
			elif event.key == K_LEFT: car.k_left = down * 5
			elif event.key == K_UP: car.k_up = down * 2
			elif event.key == K_DOWN: car.k_down = down * -2
			
			# Bike Input (Player 2)
			elif event.key == K_d: bike.k_right = down * -5
			elif event.key == K_a: bike.k_left = down * 5
			elif event.key == K_w: bike.k_up = down * 2
			elif event.key == K_s: bike.k_down = down * -2
			
			print(bike.rad)
			
			# Reset
			if event.key == K_r: 
				bike.position 	= ((display_width/2), (display_height/2))
				bike.speed = 0		
				
			if event.key == K_SPACE: 
				# Projectile test
				ball.k_up = 10
				
			if event.key == K_q:
				ball.position = (bike.position)
				ball.speed = 0	
				ball.k_up = 0
	

				
		
				
				
			# Car render
				car_group.update(time)
				car_group.draw(gameDisplay)
				
			
			# Quit
			elif event.key == K_ESCAPE: sys.exit(0)
			
		#RENDERING
		
		# Game background
		gameDisplay.fill((white))
		
		
		# Bike render
		bike_group.update(time)
		bike_group.draw(gameDisplay)
		
		# Projectile
		ball_group.update(time)
		ball_group.draw(gameDisplay)

		
		
		pygame.display.flip()

		
game_loop()
pygame.quit()
quit()
			
	
	
