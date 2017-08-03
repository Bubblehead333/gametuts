import sys
import math
import random
import pygame


pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
rect = screen.get_rect()
clock = pygame.time.Clock()
pygame.display.set_caption('Sci-fi Bike Racing Combat Game....Thing')

WHITE = pygame.Color('white')
GREY = (60,60,60)
LIGHT_GREY = (80,80,80)

BLACK = pygame.Color('black')

 
TURN_SPEED = 2
ACCELERATION = 0.1
BRAKING = 0.5


BKG_W = BKG_H = 3600

# Load images globally and reuse them in your program.
# Also use the `.convert()` or `.convert_alpha()` methods after
# loading the images to improve the performance.

PLAYAREA = pygame.Surface((3600, 3600))
PLAYAREA.fill(LIGHT_GREY)

OBSTACLE = pygame.Surface((30, 30), pygame.SRCALPHA)
OBSTACLE.fill((200, 120, 20))

bkg_img = pygame.image.load('/home/pi/gametuts/images/backgrounds/circ3.png').convert_alpha()
bike_img = pygame.image.load('/home/pi/gametuts/images/BikePixelw.bmp').convert_alpha()
laser_img = pygame.image.load('/home/pi/gametuts/images/laser.bmp').convert_alpha()



class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class VehicleSprite(Entity):
    MAX_FORWARD_SPEED = 15
    MAX_REVERSE_SPEED = 1
    

    def __init__(self, image, position, width, height):
        Entity.__init__(self)
        self.src_image = image
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0
        self.width = 32
        self.height = 64

    def update(self, time):
        # SIMULATION
        self.speed += self.k_up + self.k_down
        # To clamp the speed.
        self.speed = max(-self.MAX_REVERSE_SPEED,
                         min(self.speed, self.MAX_FORWARD_SPEED))

        # Degrees sprite is facing (direction)
        self.direction += (self.k_right + self.k_left)
        rad = math.radians(self.direction)
        self.velocity.x = -self.speed*math.sin(rad)
        self.velocity.y = -self.speed*math.cos(rad)
        self.position += self.velocity
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect(center=self.position)
        
class Projectile(Entity):
	
	def __init__(self, image, position):
		# Creates object instance off
		pygame.sprite.Sprite.__init__(self)
		self.src_image = pygame.image.load(image)
		self.position = position
		self.direction = 0
		self.speed = 40
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
		
class Obstacle(Entity):
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.src_image = pygame.image.load(image)
		self.position = position
		self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
		
	def update(self, time):
		self.position = [random.randrange(0, BKG_W), random.randrange(0, BKG_H)]
		
		
        
def speedometer(count):
	font = pygame.font.SysFont(None, 25)
	text = font.render("Speed: "+ str(count), True, WHITE)
	screen.blit(text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 50))
	
def game_loop():
	
    bike = VehicleSprite(bike_img, rect.center, 32, 64)
    obstacle1 = VehicleSprite(OBSTACLE, [random.randrange(0, BKG_W), random.randrange(0, BKG_H)], 30, 30)
    obstacle2 = VehicleSprite(OBSTACLE, [1500, 300], 30, 30)
    obstacle3 = VehicleSprite(OBSTACLE, [1000, 800], 30, 30)
    obstacle4 = VehicleSprite(OBSTACLE, [200, 400], 30, 30)
    obstacle5 = VehicleSprite(OBSTACLE, [500, 0], 30, 30)

    # Laser image load
    laser = Projectile('/home/pi/gametuts/images/laser.bmp', bike.position)

    bike_group = pygame.sprite.Group(bike)
    obstacle_group = pygame.sprite.Group(obstacle1, obstacle2, obstacle3, obstacle4, obstacle5)
    laser_group = pygame.sprite.Group(laser)
    
    all_sprites = pygame.sprite.Group(bike_group, obstacle_group, laser_group)

    camera = pygame.math.Vector2(0, 0)
    done = False

    while not done:
        time = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # Bike Input (Player 1)
                if event.key == pygame.K_d:
                    bike.k_right = -TURN_SPEED
                elif event.key == pygame.K_a:
                    bike.k_left = TURN_SPEED
                elif event.key == pygame.K_w:
                    bike.k_up = ACCELERATION
                elif event.key == pygame.K_s:
                    bike.k_down = -BRAKING
                elif event.key == pygame.K_ESCAPE:
                    done = True
                # Laser
                elif event.key == pygame.K_SPACE and event.type == pygame.KEYDOWN:
                    laser.position = bike.position
                    laser.direction = bike.direction

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    bike.k_right = 0
                elif event.key == pygame.K_a:
                    bike.k_left = 0
                elif event.key == pygame.K_w:
                    bike.k_up = 0
                elif event.key == pygame.K_s:
                    bike.k_down = 0
                    
        print "FPS: ", clock.get_fps()
        print obstacle1.position
          
        # Collision Frame
        if bike.position.x > BKG_W or bike.position.x < 0:
			bike.speed = 0
        if bike.position.y > BKG_H or bike.position.y < 0:
			bike.speed = 0
			
			
        camera -= bike.velocity
        screen.fill(GREY)
        screen.blit(PLAYAREA, [0,0]+camera)

        all_sprites.update(time)

        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect.topleft+camera)
        speedometer(bike.speed)
        pygame.display.flip()


game_loop()
pygame.quit()
sys.exit()
