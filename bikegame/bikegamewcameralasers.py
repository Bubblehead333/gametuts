import sys
import math
import random
import pygame


pygame.init()
screen = pygame.display.set_mode((1280, 800))
rect = screen.get_rect()
clock = pygame.time.Clock()
pygame.display.set_caption('Sci-fi Bike Racing Combat Game....Thing')

WHITE = pygame.Color('white')
road = (60,60,60)
TURN_SPEED = 2
ACCELERATION = 0.1
BRAKING = 0.5

# Load images globally and reuse them in your program.
# Also use the `.convert()` or `.convert_alpha()` methods after
# loading the images to improve the performance.
OBSTACLE = pygame.Surface((30, 30), pygame.SRCALPHA)
OBSTACLE.fill((200, 120, 20))
BACKGROUND = pygame.Surface((1280, 800))
BACKGROUND.fill((30, 30, 30))
bike_img = pygame.image.load('/home/pi/gametuts/images/BikePixelw.bmp').convert_alpha()
laser_img = pygame.image.load('/home/pi/gametuts/images/laser.bmp').convert_alpha()
bkg_img = pygame.image.load('/home/pi/gametuts/images/backgrounds/circ1.png').convert_alpha()



class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class VehicleSprite(Entity):
    MAX_FORWARD_SPEED = 15
    MAX_REVERSE_SPEED = 0

    def __init__(self, image, position):
        Entity.__init__(self)
        self.src_image = image
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0

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


class Background(pygame.sprite.Sprite):

    def __init__(self, image, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(topleft=location)
        
def speedometer(count):
	font = pygame.font.SysFont(None, 25)
	text = font.render("Speed: "+ str(count), True, WHITE)
	screen.blit(text, (10, 10))
	
def game_loop():
	
    background = Background(bkg_img, [0, 0])
    bike = VehicleSprite(bike_img, rect.center)
    obstacle1 = VehicleSprite(OBSTACLE, [500, 500])
    obstacle2 = VehicleSprite(OBSTACLE, [1500, 300])
    obstacle3 = VehicleSprite(OBSTACLE, [1000, 800])
    obstacle4 = VehicleSprite(OBSTACLE, [200, 400])
    obstacle5 = VehicleSprite(OBSTACLE, [500, 0])

    # Laser image load
    laser = Projectile('/home/pi/gametuts/images/laser.bmp', bike.position)

    bkg_group = pygame.sprite.Group(background)
    bike_group = pygame.sprite.Group(bike)
    obstacle_group = pygame.sprite.Group(obstacle1, obstacle2, obstacle3, obstacle4, obstacle5)
    laser_group = pygame.sprite.Group(laser)
    

    all_sprites = pygame.sprite.Group(bike_group, obstacle_group, laser_group, bkg_group)

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
                    #print (laser.direction)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    bike.k_right = 0
                elif event.key == pygame.K_a:
                    bike.k_left = 0
                elif event.key == pygame.K_w:
                    bike.k_up = 0
                elif event.key == pygame.K_s:
                    bike.k_down = 0
                    
        print(bike.speed)           
        
        screen.fill(road)
        camera -= bike.velocity
        all_sprites.update(time)
        speedometer(bike.speed)

        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect.topleft+camera)
        
        pygame.display.flip()


game_loop()
pygame.quit()
sys.exit()
