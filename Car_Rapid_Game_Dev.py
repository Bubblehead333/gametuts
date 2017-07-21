# THIS IS EXACTLY WHAT I WANT
# BASIC ROTATION AND CORNERING MECHANICS
# TRY AND UNDERSTAND THIS JOSH

import pygame, math, sys
from pygame.locals import *
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()
white = (255,255,255)



class CarSprite(pygame.sprite.Sprite):
	MAX_FORWARD_SPEED = 25
	MAX_REVERSE_SPEED = 5
	ACCELERATION = 5
	TURN_SPEED = 20

	def __init__(self, image, position):
		pygame.sprite.Sprite.__init__(self)
		self.src_image = pygame.image.load(image)
		self.position = position
		self.speed = self.direction = 0
		self.k_left = self.k_right = self.k_down = self.k_up = 0

	def update(self, deltat):
		# SIMULATION
		self.speed += (self.k_up +self.k_down)
		if self.speed > self.MAX_FORWARD_SPEED:
			self.speed = self.MAX_FORWARD_SPEED
		if self.speed < -self.MAX_REVERSE_SPEED:
			self.speed = -self.MAX_REVERSE_SPEED
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
rect = screen.get_rect()
# RPi3
# car = CarSprite('/home/pi/gametuts/images/car_01.png', rect.center)

#EQPC
car = CarSprite('C:/Users/jlyell/PycharmProjects/gametuts/images/blueBike2.png', rect.center)
bike = CarSprite('C:/Users/jlyell/PycharmProjects/gametuts/images/purpleBike2SM.png', rect.center)

car_group = pygame.sprite.RenderPlain(car)
bike_group = pygame.sprite.RenderPlain(bike)

while 1:

	#USER INPUT
	deltat = clock.tick(30)

	for event in pygame.event.get():
		if not hasattr(event, 'key'): continue
		down = event.type == KEYDOWN
		if event.key == K_RIGHT: car.k_right = down * -5
		elif event.key == K_LEFT: car.k_left = down * 5
		elif event.key == K_UP: car.k_up = down * 2
		elif event.key == K_DOWN: car.k_down = down * -2
		elif event.key == K_ESCAPE: sys.exit(0)

		elif event.key == K_d: bike.k_right = down * -5
		elif event.key == K_a: bike.k_left = down * 5
		elif event.key == K_w: bike.k_up = down * 2
		elif event.key == K_s: bike.k_down = down * -2
		
	#RENDERING

	screen.fill(white)
	car_group.update(deltat)
	bike_group.update(deltat)

	car_group.draw(screen)
	bike_group.draw(screen)

	pygame.display.flip()

	
	
