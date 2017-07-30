# THIS IS EXACTLY WHAT I WANT
# BASIC ROTATION AND CORNERING MECHANICS
# TRY AND UNDERSTAND THIS JOSH

import pygame, math, sys, random
from pygame.locals import *
#
display_width = 1280
display_height = 800

HALF_WIDTH = int(display_width / 2)
HALF_HEIGHT = int(display_height / 2)
# Sets size of screen
screen = pygame.display.set_mode((display_width, display_height))

FLAGS = 0
CAMERA_SLACK = 30

# Initialises clock
clock = pygame.time.Clock()

# Colours
white = (255,255,255)
black = (0,0,0)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

class VehicleSprite(Entity):
	# Creates a vehicle class
	MAX_FORWARD_SPEED = 10
	MAX_REVERSE_SPEED = 2
	ACCELERATION = 0.05
	TURN_SPEED = 0.000000000001
	
	def __init__(self, image, position, x, y):
		Entity.__init__(self)

		# Creates object instance off
		pygame.sprite.Sprite.__init__(self)
		self.src_image = pygame.image.load(image)
		self.position = position
		self.speed = self.direction = 0
		self.k_left = self.k_right = self.k_down = self.k_up = 0
		self.rect = Rect(x, y, 32, 32)

		
	def update(self, time):
		# SIMULATION
		self.speed += (self.k_up +self.k_down)
		if self.speed > self.MAX_FORWARD_SPEED:
			self.speed = self.MAX_FORWARD_SPEED
		if self.speed < -self.MAX_REVERSE_SPEED:
			self.speed = -self.MAX_REVERSE_SPEED
			
		# Degrees sprite is facing (direction)
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
		
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

	
# CREATE A CAR AND TUN
rect = screen.get_rect()

# Background
BackGround = Background('/home/pi/gametuts/images/backgrounds/I.png', [0, 0])
#bkg_group = pygame.sprite.RenderPlain(BackGround)

# Car image load
#car = VehicleSprite('/home/pi/gametuts/images/blueBike2.png', rect.center)
#car_group = pygame.sprite.RenderPlain(car)

# Bike image load
bike = VehicleSprite('/home/pi/gametuts/images/BikePixelBig.png', rect.center, 32, 16)
bike_group = pygame.sprite.RenderPlain(bike)

# Ball image load
ball = Projectile('/home/pi/gametuts/images/ironball.png', rect.center)
ball_group = pygame.sprite.RenderPlain(ball)

# Main game loop
def game_loop():
	
	# Defining obstacle start parameters
	global cameraX, cameraY

	camera = Camera(simple_camera, display_width, display_height)

	
	while 1:
		#USER INPUT
		# Sets frame rate
		time = clock.tick(60)
		for event in pygame.event.get():
			if not hasattr(event, 'key'): continue
			down = event.type == KEYDOWN
			# Car Input (Player 1)
			#if event.key == K_RIGHT: BackGround.k_right = down * 5
			#elif event.key == K_LEFT: BackGround.k_left = down * -5
			#elif event.key == K_UP: BackGround.k_up = down * -2
			#elif event.key == K_DOWN: BackGround.k_down = down * 2
			
			# Bike Input (Player 2)
			if event.key == K_d: bike.k_right = down * -5
			elif event.key == K_a: bike.k_left = down * 5
			elif event.key == K_w: bike.k_up = down * 2
			elif event.key == K_s: bike.k_down = down * -2
			
			
			# Reset
			if event.key == K_r: 
				bike.position 	= ((display_width/2), (display_height/2))
				bike.speed = 0		
				
			if event.key == K_SPACE: 
				# Projectile test
				ball.k_up = 10
				
			# Could make a mine? Set up collision detection if bike runs over it
			if event.key == K_q:
				ball.position = (bike.position)
				ball.speed = 0	
				ball.k_up = 0
				print(ball.position)
		
			
			# Quit
			elif event.key == K_ESCAPE: sys.exit(0)
			
		#RENDERING
		
		# Game background
		screen.fill([255, 255, 255])
		# screen.blit(BackGround.image, BackGround.rect)
			
		# Camera guess
		camera.update(bike)
		
		# update player, draw everything else
        bike_group.update(time)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

		# Bike render
		#bike_group.update(time)
		#bike_group.draw(screen)
		
		# Projectile
		#ball_group.update(time)
		#ball_group.draw(screen)
		
		pygame.display.flip()

		
game_loop()
pygame.quit()
quit()
			
	
	
