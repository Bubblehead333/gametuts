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
LIGHT_GREY = (120,120,120)

BLACK = pygame.Color('black')

 
TURN_SPEED = 2
ACCELERATION = 0.18
DEACCELERATION = 0.1
BRAKING = 0.5

BKG_W = BKG_H = 3600

PLAYAREA = pygame.Surface((3600, 3600))
PLAYAREA.fill(LIGHT_GREY)

OBSTACLE = pygame.Surface((30, 30), pygame.SRCALPHA)
OBSTACLE.fill((200, 120, 20))

#bkg_img = pygame.image.load('/home/pi/gametuts/images/backgrounds/circ3.bmp').convert_alpha()
purple_bike_imgs = pygame.image.load('/home/pi/gametuts/images/purple_bike1.bmp').convert_alpha()
bike_img = pygame.image.load('/home/pi/gametuts/images/BikePixelw.bmp').convert_alpha()
purple_bike_img =pygame.image.load('/home/pi/gametuts/images/purple_bike1ss.bmp').convert_alpha()


laser_img = pygame.image.load('/home/pi/gametuts/images/laser.bmp').convert_alpha()
crate_img = pygame.image.load('/home/pi/gametuts/images/crate1.bmp').convert_alpha()

power_img = pygame.image.load('/home/pi/gametuts/images/crate2.bmp').convert_alpha()





class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class VehicleSprite(Entity):
    MAX_FORWARD_SPEED = 18
    MAX_REVERSE_SPEED = 1
    

    def __init__(self, images, position):
        Entity.__init__(self)
        self.src_images = images
        self.images = images
        self.rect = self.images.get_rect(center=position)
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0
        self.width = 28
        self.height = 64
        #self.numImages = 8
        #self.cImage = 0


    def update(self, time):
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
        #if (self.cImage >= self.numImages - 1):
		#	self.cImage = 0
        #else:
		#	self.cImage += 1
        self.images = pygame.transform.rotate(self.src_images, self.direction)
        #self.rect = self.images.get_rect(center=self.position)
        
    def render(self, screen, camera):
		# For animation
        #screen.blit(self.images, (self.rect.topleft+camera), (self.cImage*self.width, 0, self.width, self.height))
        # For static
        screen.blit(self.images, camera)

        
        
        
class Laser(Entity):
	LASER_SPEED = 40
	
	def __init__(self, position, direction):
		pygame.sprite.Sprite.__init__(self)
		self.src_image = laser_img
		self.position = position
		self.direction = direction
		self.speed = 40
		
	def update(self, time):
		# SIMULATION
		x, y = self.position
		self.rad = self.direction * math.pi / 180
		x += (-self.speed)*math.sin(self.rad)
		y += (-self.speed)*math.cos(self.rad)
		self.position = (x, y)
		self.image = pygame.transform.rotate(self.src_image, self.direction)
		self.rect = self.image.get_rect()
		self.rect.center = self.position
		
class Obstacle(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.src_image = crate_img
        self.image = crate_img
        self.x = random.randrange(0, BKG_W)
        self.y = random.randrange(0, BKG_H)
        self.position = [self.x, self.y]
        self.width = self.height = 32
        x, y = self.position
       
    def update(self, time):
        x, y = self.position
        self.image = crate_img
        self.rect = self.image.get_rect(center=self.position)	
		
class Powerup(Entity):
    def __init__(self, image, x, y):
        Entity.__init__(self)
        self.src_image = image
        self.image = image
        self.x = x
        self.y = y
        self.position = (self.x, self.y)
        self.width = self.height = 32
       
    def update(self, time):
        x, y = self.position
        self.image = crate_img
        self.rect = self.image.get_rect(center=self.position)	
		
        
def speedometer(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Speed: "+ str(10*count) + " mph", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50))
	
def game_loop():
	
    #purple_bike = VehicleSprite(purple_bike_img, rect.center)
    red_bike = VehicleSprite(bike_img, rect.center)

    purple_bike = VehicleSprite(purple_bike_imgs, rect.center)

    power = Powerup(power_img, 200, 200)
    
    lasers = []
    crates = []
    num = 100
    while num > 0:
        crates.append(Obstacle())
        num = num - 1
    print(crates[0].position)
        
    #power_group = pygame.sprite.Group(power)
    

    #bike_group = pygame.sprite.Group(purple_bike)
    
    all_sprites = pygame.sprite.Group(purple_bike)

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
                    purple_bike.k_right = -TURN_SPEED
                elif event.key == pygame.K_a:
                    purple_bike.k_left = TURN_SPEED
                elif event.key == pygame.K_w:
                    purple_bike.k_up = ACCELERATION
                elif event.key == pygame.K_s:
                    purple_bike.k_down = -BRAKING
                elif event.key == pygame.K_ESCAPE:
                    done = True
                # Laser
                elif event.key == pygame.K_SPACE and event.type == pygame.KEYDOWN:
                    lasers.append(Laser(purple_bike.position, purple_bike.direction))

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    purple_bike.k_right = 0
                elif event.key == pygame.K_a:
                    purple_bike.k_left = 0
                elif event.key == pygame.K_w:
                    purple_bike.k_up = 0
                elif event.key == pygame.K_s:
                    purple_bike.k_down = 0
                    
        #print "FPS: ", clock.get_fps()
          
        # Collision Frame
        if purple_bike.position.x > BKG_W or purple_bike.position.x < 0:
            purple_bike.speed = 0
        if purple_bike.position.y > BKG_H or purple_bike.position.y < 0:
            purple_bike.speed = 0
		
		
			
		# Deacceleration
        if purple_bike.speed > 0: 
            purple_bike.speed = purple_bike.speed - DEACCELERATION
			
        camera -= purple_bike.velocity
        screen.fill(GREY)
        screen.blit(PLAYAREA, [0,0]+camera)

        all_sprites.update(time)


        for sprite in all_sprites:
            for crate in crates:
                crate.update(time)
            for crate in crates:
                screen.blit(power_img, crate.position+camera)
                # Collision with crate
                if pygame.sprite.collide_rect(purple_bike, crate):
					print("Hit")
					purple_bike.speed = 0

            for laser in lasers:
                laser.update(time)
                if (laser.position[0] >= crate.x and laser.position[0] < crate.x + crate.width or laser.position[0] > crate.x and laser.position[0] < crate.x + crate.width and laser.position[1] > crate.y and laser.position[1] < crate.y + crate.height or laser.position[1]  > crate.y and laser.position[1] < crate.y + crate.height):
                    print('Pew!')
            for laser in lasers:
                screen.blit(laser.image, laser.position+camera)
                
                
            #screen.blit(sprite.image, sprite.rect.topleft+camera)
            purple_bike.render(screen, camera)
            
        

        speedometer(purple_bike.speed)
        

        pygame.display.flip()


game_loop()
pygame.quit()
sys.exit()
