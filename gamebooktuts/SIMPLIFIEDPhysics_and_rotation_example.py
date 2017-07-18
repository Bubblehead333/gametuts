#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
017_turning_and_physic.py
pygame sprites primitive physic (elastic collision)
url: http://thepythongamebook.com/en:part2:pygame:step017
author: horst.jens@spielend-programmieren.at
physic by Leonard Michlmayr
licence: gpl, see http://www.gnu.org/licenses/gpl.html

move the big bird around with the keys w,a,s,d  and q and e
fire with space, toggle gravity with g

works with pyhton3.4 and python2.7
"""
#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division

def game(folder = "data"):
    import pygame
    import os
    import random
    import math 
    
    #------ starting pygame -------------
    pygame.init()
    screen=pygame.display.set_mode((640,480)) # try out larger values and see what happens !

    print("pygame version", pygame.ver)
    # ------- game constants ----------------------
    BIRDSPEEDMAX = 200
    FRAGMENTMAXSPEED = 200
    FRICTION =.991  # between 1 and 0. 1 means no friction at all (deep space)
    GRAD = math.pi / 180 # 2 * pi / 360   # math module needs Radiant instead of Grad
    # ----------- functions -----------
    def write(msg="pygame is cool", color=(0,0,0)):
        """write text into pygame surfaces"""
        myfont = pygame.font.SysFont("None", 32)
        mytext = myfont.render(msg, True, color)
        mytext = mytext.convert_alpha()
        return mytext
    def getclassname(class_instance):
        """this function extract the class name of a class instance.
        For an instance of a XWing class, it will return 'XWing'."""
        text = str(class_instance.__class__) # like "<class '__main__.XWing'>"
        parts = text.split(".") # like ["<class '__main__","XWing'>"]
        return parts[-1][0:-2] # from the last (-1) part, take all but the last 2 chars
    
    def elastic_collision(sprite1, sprite2):
        """elasitc collision between 2 sprites (calculated as disc's).
           The function alters the dx and dy movement vectors of both sprites.
           The sprites need the property .mass, .radius, .pos[0], .pos[1], .dx, dy
           pos[0] is the x postion, pos[1] the y position"""
        # here we do some physics: the elastic
        # collision
        #
        # first we get the direction of the push.
        # Let's assume that the sprites are disk
        # shaped, so the direction of the force is
        # the direction of the distance.
        dirx = sprite1.pos[0] - sprite2.pos[0]
        diry = sprite1.pos[1] - sprite2.pos[1]
        #
        # the velocity of the centre of mass
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.dx * sprite1.mass + sprite2.dx * sprite2.mass) / sumofmasses
        sy = (sprite1.dy * sprite1.mass + sprite2.dy * sprite2.mass) / sumofmasses
        # if we sutract the velocity of the centre
        # of mass from the velocity of the sprite,
        # we get it's velocity relative to the
        # centre of mass. And relative to the
        # centre of mass, it looks just like the
        # sprite is hitting a mirror.
        #
        bdxs = sprite2.dx - sx
        bdys = sprite2.dy - sy
        cbdxs = sprite1.dx - sx
        cbdys = sprite1.dy - sy
        # (dirx,diry) is perpendicular to the mirror
        # surface. We use the dot product to
        # project to that direction.
        distancesquare = dirx * dirx + diry * diry
        if distancesquare == 0:
            # no distance? this should not happen,
            # but just in case, we choose a random
            # direction
            dirx = random.randint(0,11) - 5.5
            diry = random.randint(0,11) - 5.5
            distancesquare = dirx * dirx + diry * diry
        dp = (bdxs * dirx + bdys * diry) # scalar product
        dp /= distancesquare # divide by distance * distance.
        cdp = (cbdxs * dirx + cbdys * diry)
        cdp /= distancesquare
        # We are done. (dirx * dp, diry * dp) is
        # the projection of the velocity
        # perpendicular to the virtual mirror
        # surface. Subtract it twice to get the
        # new direction.
        #
        # Only collide if the sprites are moving
        # towards each other: dp > 0
        if dp > 0:
            sprite2.dx -= 2 * dirx * dp 
            sprite2.dy -= 2 * diry * dp
            sprite1.dx -= 2 * dirx * cdp 
            sprite1.dy -= 2 * diry * cdp
    # ----------- classes ------------------------
    class Text(pygame.sprite.Sprite):
        """a pygame Sprite displaying text"""
        def __init__(self, msg="The Python Game Book", color=(0,0,0)):
            self.groups = allgroup
            self._layer = 1
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.newmsg(msg,color)
            
        def update(self, time):
            pass # allgroup sprites need update method that accept time
        
        def newmsg(self, msg, color=(0,0,0)):
            self.image =  write(msg,color)
            self.rect = self.image.get_rect()
       
    class Bird(pygame.sprite.Sprite):
        """generic Bird class, to be called from SmallBird and BigBird"""
        image=[]  # list of all images
        birds = {} # a dictionary of all Birds, each Bird has its own number
        number = 0  
        waittime = 1.0 # seconds
        def __init__(self, layer = 4, bigbird = False ):
            self.groups = birdgroup, allgroup # assign groups 
            self._layer = layer                   # assign level
            #self.layer = layer
            pygame.sprite.Sprite.__init__(self,  self.groups  ) #call parent class. NEVER FORGET !
            self.pos = [random.randint(50,screen.get_width()-50),
                        random.randint(25,screen.get_height()-25)] 
            self.area = screen.get_rect()
            self.image = Bird.image[2]
            self.image = Bird.image[0]
            self.rect = self.image.get_rect()
            self.radius = max(self.rect.width, self.rect.height) / 2.0
            self.dx = 0   # wait at the beginning
            self.dy = 0            
            self.waittime = Bird.waittime # 1.0 # one second
            self.lifetime = 0.0
            self.waiting = True
            self.rect.center = (-100,-100) # out of visible screen
            self.crashing = False
            self.number = Bird.number # get my personal Birdnumber
            Bird.number+= 1           # increase the number for next Bird
            Bird.birds[self.number] = self # store myself into the Bird dictionary
            print("my number %i Bird number %i and i am a %s " % (self.number, Bird.number, getclassname(self)))
            self.mass = 100.0
            self.angle = 0.0
            self.boostspeed = 10 # speed to fly upward
            self.boostmax = 0.9 # max seconds of "fuel" for flying upward
            self.boostmin = 0.4 # min seconds of "fuel" for flying upward
            self.boosttime = 0.0 # time (fuel) remaining
      
        def kill(self):
            # a shower of red fragments, exploding outward
            for _ in range(self.frags):
				pygame.sprite.Sprite.kill(self) # kill the actual Bird 
            
        def speedcheck(self):
            #if abs(self.dx) > BIRDSPEEDMAX:
            #   self.dx = BIRDSPEEDMAX * (self.dx/abs(self.dx)) # dx/abs(dx) is 1 or -1
            #if abs(self.dy) > BIRDSPEEDMAX:
            #   self.dy = BIRDSPEEDMAX * (self.dy/abs(self.dy))
            if abs(self.dx) > 0 : 
                self.dx *= FRICTION  # make the Sprite slower over time
            if abs(self.dy) > 0 :
                self.dy *= FRICTION

        def areacheck(self):
            if not self.area.contains(self.rect):
                self.crashing = True # change colour later
                # --- compare self.rect and area.rect
                if self.pos[0] + self.rect.width/2 > self.area.right:
                    self.pos[0] = self.area.right - self.rect.width/2
                    self.dx *= -0.5 # bouncing off but loosing speed
                if self.pos[0] - self.rect.width/2 < self.area.left:
                    self.pos[0] = self.area.left + self.rect.width/2
                    self.dx *= -0.5 # bouncing off the side but loosing speed
                if self.pos[1] + self.rect.height/2 > self.area.bottom:
                    self.pos[1] = self.area.bottom - self.rect.height/2
                    #self.dy *= -1 # bouncing off the ground
                    #if reaching the bottom, the birds get a boost and fly upward to the sky
                    #at the bottom the bird "refuel" a random amount of "fuel" (the boostime)
                    self.dy = 0 # break at the bottom
                    self.dx *= 0.3 # x speed is reduced at the ground
                    self.boosttime = self.boostmin + random.random()* (self.boostmax - self.boostmin)
                if self.pos[1] - self.rect.height/2 < self.area.top:
                    self.pos[1] = self.area.top + self.rect.height/2
                    self.dy = 0 # stop when reaching the sky
                    #self.dy *= -1 
        def update(self, seconds):
            #---make Bird only visible after waiting time
            self.lifetime += seconds
            if self.lifetime > (self.waittime):
                self.waiting = False
            if self.waiting:
                self.rect.center = (-100,-100)
            else: # the waiting time (Blue Fragments) is over
                if self.boosttime > 0:   # boost flying upwards ?
                    self.boosttime -= seconds
                    self.dy -= self.boostspeed # upward is negative y !
                    self.ddx = -math.sin(self.angle*GRAD) 
                    self.ddy = -math.cos(self.angle*GRAD) 
                self.speedcheck()    # ------------- movement
                self.pos[0] += self.dx * seconds
                self.pos[1] += self.dy * seconds
                self.areacheck() # ------- check if Bird out of screen
                #--- calculate actual image: crasing, bigbird, both, nothing ?
                self.image = Bird.image[self.crashing+self.big] # 0 for not crashing, 1 for crashing
                self.image0 = Bird.image[self.crashing+self.big] # 0 for not crashing, 1 for crashing
                #--------- rotate into direction of movement ------------
                self.angle = math.atan2(-self.dx, -self.dy)/math.pi*180.0 
                self.image = pygame.transform.rotozoom(self.image0,self.angle,1.0)
                #--- calculate new position on screen -----
                self.rect.centerx = round(self.pos[0],0)
                self.rect.centery = round(self.pos[1],0)
                if self.hitpoints <= 0:
                    self.kill()
    
    
    class BigBird(Bird):
        """A big bird controlled by the player"""
        def __init__(self):
            self.big = 2 # smallsprites have the value 0 for this attribute (.big) -> important for Bird.image
            Bird.__init__(self) # create a "little" Bird but do more than that
            self.image = Bird.image[2] # big bird image
            self.pos = [screen.get_width()/2, screen.get_height()/2]
            self.rect = self.image.get_rect()
            self.angle = 0
            self.speed = 20.0 # base movement speed factor
            self.rotatespeed = 1.0 # rotating speed
            self.frags = 100
            self.cooldowntime = 0.08 #seconds
            self.cooldown = 0.0
            self.damage = 5 # how many damage one bullet inflict
            self.shots = 0
            self.radius = self.image.get_width() / 2.0
            self.mass = 400.0
        
        def kill(self):
            bombsound.play()
            Bird.kill(self)
            
        def update(self, time):
            """BigBird has its own update method, overwriting the 
               update method from the Bird class"""
            self.lifetime += seconds
            if self.lifetime > (self.waittime):
                self.waiting = False
            if self.waiting:
                self.rect.center = (-100,-100)
            else:
                #--- calculate actual image: crasing, bigbird, both, nothing ?
                self.image = Bird.image[self.crashing+self.big] # 0 for not crashing, 2 for big
                pressedkeys = pygame.key.get_pressed()
                self.ddx = 0.0
                self.ddy = 0.0
                if pressedkeys[pygame.K_w]: # forward
                         self.ddx = -math.sin(self.angle*GRAD) 
                         self.ddy = -math.cos(self.angle*GRAD) 
                if pressedkeys[pygame.K_s]: # backward
                         self.ddx = +math.sin(self.angle*GRAD) 
                         self.ddy = +math.cos(self.angle*GRAD) 
                if pressedkeys[pygame.K_e]: # right side
                         self.ddx = +math.cos(self.angle*GRAD)
                         self.ddy = -math.sin(self.angle*GRAD)
                if pressedkeys[pygame.K_q]: # left side
                         self.ddx = -math.cos(self.angle*GRAD) 
                         self.ddy = +math.sin(self.angle*GRAD) 
                
                # ------------move------------------
                if not self.waiting:
                    self.dx += self.ddx * self.speed
                    self.dy += self.ddy * self.speed
                #self.speedcheck()   # friction, maxspeed             
                self.pos[0] += self.dx * seconds
                self.pos[1] += self.dy * seconds
                # -- check if Bird out of screen
                self.areacheck()
                # ------------- rotate ------------------
                if pressedkeys[pygame.K_a]: # left turn , counterclockwise
                    self.angle += self.rotatespeed
                if pressedkeys[pygame.K_d]: # right turn, clockwise
                    self.angle -= self.rotatespeed
                self.oldcenter = self.rect.center
                self.image = pygame.transform.rotate(self.image, self.angle)
                self.rect = self.image.get_rect()
                self.rect.center = self.oldcenter
                #--- calculate new position on screen -----
                self.rect.centerx = round(self.pos[0],0)
                self.rect.centery = round(self.pos[1],0)
                         
    # ----------------- background artwork -------------  
    background = pygame.Surface((screen.get_width(), screen.get_height()))
    background.fill((255,255,255))     # fill white
    background.blit(write("navigate with w,a,s,d and q and e "),(50,40))
    background.blit(write("press SPACE to fire bullets"),(50,70))
    background.blit(write("press g to toggle gravity"), (50, 100))
    background.blit(write("Press ESC to quit "), (50,130))
    background = background.convert()  # jpg can not have transparency
    screen.blit(background, (0,0))     # blit background on screen (overwriting all)
    #-----------------define sprite groups------------------------
    birdgroup = pygame.sprite.Group() 
    # only the allgroup draws the sprite, so i use LayeredUpdates() instead Group()
    allgroup = pygame.sprite.LayeredUpdates() # more sophisticated, can draw sprites in layers 

    #-------------loading files from data subdirectory -------------------------------
    try: # load images into classes (class variable !). if not possible, draw ugly images
        Bird.image.append(pygame.image.load(os.path.join(folder,"babytux.png")))
        Bird.image.append(pygame.image.load(os.path.join(folder,"babytux_neg.png")))
    except:
        print("no image files 'babytux.png' and 'babytux_neg.png' in subfolder %s" % folder)
        print("therfore drawing ugly sprites instead")
        image = pygame.Surface((32,36))
        image.fill((255,255,255))
        pygame.draw.circle(image, (0,0,0), (16,18), 15,2)
        pygame.draw.polygon(image, (0,0,0), ((32,36),(0,36),(16,0)),1) # triangle
        image.set_colorkey((255,255,255))
        Bird.image.append(image) # alternative ugly image
        image2 = image.copy()
        pygame.draw.circle(image2, (0,0,255), (16,18), 13,0)
        Bird.image.append(image2)
    Bird.image.append(pygame.transform.scale2x(Bird.image[0])) # copy of first image, big bird
    Bird.image.append(pygame.transform.scale2x(Bird.image[1])) # copy of blue image, big bird
    Bird.image[0] = Bird.image[0].convert_alpha()
    Bird.image[1] = Bird.image[1].convert_alpha()
    Bird.image[2] = Bird.image[2].convert_alpha()
    Bird.image[3] = Bird.image[3].convert_alpha()

   
    # ------------- before the main loop ----------------------
    screentext = Text()
    clock = pygame.time.Clock()        # create pygame clock object 
    mainloop = True
    FPS = 60                           # desired max. framerate in frames per second. 
    amount = 7 # how many small birds should always be present on the screen
    player = BigBird() # big Bird
    overtime = 15 # time in seconds to admire the explosion of player before the game ends
    gameOver = False
    hits = 0  # how often the player was hitting a small Bird
    quota = 0 # hit/miss quota
    gravity = True
        
    while mainloop:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC
                elif event.key == pygame.K_x:
                    player.hitpoints -= 1
                    print(player.hitpoints)
                elif event.key == pygame.K_y:
                    player.hitpoints += 1
                    print(player.hitpoints)
                elif event.key == pygame.K_g:
                    gravity = not gravity # toggle gravity
                elif event.key == pygame.K_p: # get sprites at mouse position, print info
                    print("=========================")
                    print( "-----Spritelist---------")
                    spritelist = allgroup.get_sprites_at(pygame.mouse.get_pos())
                    for sprite in spritelist:
                        print(sprite, "Layer:",allgroup.get_layer_of_sprite(sprite))
                    print("------------------------")
         
   
        if player.shots > 0:
            quota = (float(hits)/player.shots )* 100
        pygame.display.set_caption("fps: %.2f gravity: %s hits:%i shots:%i quota:%.2f%%"  % (clock.get_fps(), 
                                     gravity, hits, player.shots, quota))
                                                 
        # ----------- clear, draw , update, flip -----------------  
        allgroup.clear(screen, background)
        allgroup.update(seconds)
        allgroup.draw(screen)           
        pygame.display.flip()         

if __name__ == "__main__":
    game()
