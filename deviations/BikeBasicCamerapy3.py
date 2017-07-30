import pygame, math, sys, random
import pygame as pg
from pygame.math import Vector2

from pygame.locals import *

display_width = 1280
display_height = 800

# Sets size of screen
screen = pygame.display.set_mode((display_width, display_height))

# Initialises clock
clock = pygame.time.Clock()
 
# Colours
white = (255,255,255)
road = (60,60,60)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class VehicleSprite(pg.sprite.Sprite):
    # Creates a vehicle class
    MAX_FORWARD_SPEED = 10
    MAX_REVERSE_SPEED = 2
    #ACCELERATION = 0.05
    #TURN_SPEED = 0.000000000001

    def __init__(self, image, position, *groups):
        super().__init__(*groups)
        Entity.__init__(self)
        # Creates object instance off
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0
        self.vel = Vector2(0, 0)
        self.position = Vector2(position)


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
        self.rad = self.direction * math.pi / 180
        x += -self.speed*math.sin(self.rad)
        y += -self.speed*math.cos(self.rad)
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.position += self.vel
        
class Projectile(Entity):
	
	def __init__(self, image, position):
		# Creates object instance off
		pygame.sprite.Sprite.__init__(self)
		self.src_image = pygame.image.load(image)
		self.position = position
		self.direction = 0
		# Laser speed
		self.speed = 30
		self.k_left = self.k_right = self.k_down = self.k_up = self.rad = 0
		
	def update(self, time):
		# SIMULATION
		self.direction += (self.k_right + self.k_left)
		x, y = self.position
		self.rad = self.direction * math.pi / 180
		x += (-self.speed)*math.sin(self.rad)
		y += (-self.speed)*math.cos(self.rad)
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

rect = screen.get_rect()

# Background
#BackGround = Background('/home/pi/gametuts/images/backgrounds/circ1.png', [0, 0])
all_sprites = pg.sprite.Group()

# Bike image load
bike = VehicleSprite('/home/pi/gametuts/images/BikePixelw.bmp', rect.center, all_sprites)
bike_group = pygame.sprite.RenderPlain(bike)

# Ball image load
ball = Projectile('/home/pi/gametuts/images/laser.bmp', rect.center)
ball_group = pygame.sprite.RenderPlain(ball)

ball2 = Projectile('/home/pi/gametuts/images/laser.bmp', rect.center)
ball2_group = pygame.sprite.RenderPlain(ball)

# Main game loop
def game_loop():

# Game background
    camera = Vector2(0, 0)
    
	
    while 1:
        #USER INPUT
        # Sets frame rate
        time = clock.tick(60)
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            down = event.type == KEYDOWN

            # Bike Input (Player 1)
            if event.key == K_d: 
                bike.k_right = down * -3
                bike.vel.x = down * -3
            elif event.key == K_a: 
                bike.k_left = down * 3
                bike.vel.x = down * 3
            elif event.key == K_w: 
                bike.k_up = down * 0.25
                bike.vel.y = down * 0.25
            elif event.key == K_s: 
                bike.k_down = down * -0.25
                bike.vel.y = down * -0.25    

            # Quit
            elif event.key == K_ESCAPE: sys.exit(0)
            
            # Laser
            if event.key == K_SPACE and event.type == KEYDOWN:
                ball.position = bike.position
                ball.direction = bike.direction
                print (ball.direction)
                
        camera -= bike.position
        all_sprites.update(time)

        screen.fill((30, 30, 30))
        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect.topleft+camera)
            

        #RENDERING
        screen.fill(road)
        #screen.blit(BackGround.image, BackGround.rect)


        # Bike render
        bike_group.update(time)
        bike_group.draw(screen)

        ball_group.update(time)
        ball_group.draw(screen)

        pygame.display.flip()


game_loop()
pygame.quit()
quit()
