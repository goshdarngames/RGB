################################################################################
# player.py
################################################################################
# Class definition for the man that the player controls.
################################################################################
# 09/09 Flembobs
################################################################################

from gameObject import GameObject
from wall import Wall
from spike import Spike
from goal import Goal

import pygame
import os
import colour as COLOUR

################################################################################
# CONSTANTS
################################################################################

#number of ticks between each animation frame
TICKS_BETWEEN_ANIM_FRAMES = 3

#number of frames in the run animation
RUN_FRAMES = 4

JUMP_SPEED = -5 #speed added when player jumps
GRAV_ACC = 0.2 #acceleration caused by gravity
HOR_ACC = 0.3 #left/right run speed
FRICTION = 0.9 #horizontal friction

#Max x and y speeds
MAX_XSPEED = 5
MAX_YSPEED = 5

#Time until player respawns after death
RESPAWN_DELAY = 120

################################################################################
# CLASS DEFINITION
################################################################################

class Player(GameObject):
   
   def __init__(self,gameScene,x,y):
      GameObject.__init__(self,gameScene,x,y,16,16)
      
      self.direction = "right"
      self.img = "stationary"
      
      #Flag indicating if the player is in mid air
      self.jumping = True
      
      #The number of renders until the animation is updated
      self.animationTick = TICKS_BETWEEN_ANIM_FRAMES
      
      #The current frame of the animation
      self.animationFrame = 0
      
      #x and y speeds
      self.xspeed = 0.0
      self.yspeed = 0.0
      
      #The accurate x and y locations
      self.x = x
      self.y = y
      
      #Colours
      self.colour = (255,0,0) #active colour
      self.rColour1 = (0,255,0) #reserve colour 1
      self.rColour2 = (0,0,255) #reserve colour 2
   
   #----------------------------------------------------------------------------
   
   def draw(self):
      gE = self.gameScene.gameEngine
      
      img_str = os.path.join("man",COLOUR.colourToWord(self.colour),self.img)
      
      img = gE.resourceManager.getImage(img_str)
      
      if self.direction is "left":
         img = pygame.transform.flip(img,True,False)
      
      gE.screen.blit(img,(self.x,self.y))
      
      #update the animation
      self.animationTick -= 1
      if self.animationTick <= 0:
         self.animationFrame +=1
         self.animationFrame = self.animationFrame % RUN_FRAMES
         self.animationTick = TICKS_BETWEEN_ANIM_FRAMES
         
   #----------------------------------------------------------------------------
         
   def update(self):
      keys = pygame.key.get_pressed()
      
      #Decide what sprite state is to be drawn
      if keys[pygame.K_d]:
         self.direction = "right"
         self.img = "run"+str(self.animationFrame)
      elif keys[pygame.K_a]:
         self.direction = "left"
         self.img = "run"+str(self.animationFrame)
      else:
         self.img = "stationary"   
      if self.jumping:
         self.img = "jump"
      
      #see if player wants to change colour
      #use keydown event to prevent colour flashing if player holds the key
      for ev in self.gameScene.gameEngine.events:
         if ev.type == pygame.KEYDOWN:
         
            #swap colour with reserve colour
            if ev.key == pygame.K_LEFT:
               temp = self.rColour1
               self.rColour1 = self.colour
               self.colour = temp
               
            if ev.key == pygame.K_RIGHT:
               temp = self.rColour2
               self.rColour2 = self.colour
               self.colour = temp
            
      
      #apply gravity
      self.yspeed+=GRAV_ACC
      
      #move left and right
      if keys[pygame.K_d]:
         self.xspeed +=HOR_ACC
      if keys[pygame.K_a]:
         self.xspeed -= HOR_ACC
      
      #reduce xspeed according to friction
      self.xspeed*=FRICTION
      
      #detect if the player wants to jump
      if keys[pygame.K_w] or keys[pygame.K_SPACE]:
         if not self.jumping:
            self.yspeed += JUMP_SPEED
      
      #set jumping to true so that if there is not a collision the player will
      #be in jump mode
      self.jumping = True
      
      #cap speeds to max speed
      if self.yspeed > MAX_YSPEED:
         self.yspeed = MAX_YSPEED
      if self.yspeed < MAX_YSPEED*-1:
         self.yspeed = MAX_YSPEED*-1
         
      if self.xspeed > MAX_XSPEED:
         self.xspeed = MAX_XSPEED
      if self.xspeed < MAX_XSPEED*-1:
         self.xspeed = MAX_XSPEED*-1
      
      #move player according to speed
      self.__move(0,self.yspeed)
      self.__move(self.xspeed,0)   
   
   #----------------------------------------------------------------------------
      
   def __move(self,dx,dy):
      self.x+=dx
      self.y+=dy
      
      #rectangle for the player's collision (width set to 4 for accuracy)
      collisionRect = pygame.Rect(self.x+6,self.y,4,16)
      
      #large rectangle to detect if there is a platform below the player
      bigRect = collisionRect.inflate(0,1)
      bigRect.top = collisionRect.top
      
      #check for collisions
      for obj in self.gameScene.objects:
         
         #test if there is a colour collision
         if not COLOUR.colourCollision(self.colour,obj.colour):
            continue
         
         #Test if there is a collision with the buffer rectangle
         if bigRect.colliderect(obj.rect):
            if dy > 0 and isinstance(obj,Wall): #if moving down and obj's a wall
               self.jumping = False
               self.yspeed = 0
         else:
            continue
         
         #test if the small rectangle collides and resolve the collision
         if collisionRect.colliderect(obj.rect):
            
            #colliding with a wall
            if isinstance(obj,Wall):
               if dx > 0: #moving right, hit left of wall
                  self.x = obj.rect.left-10
               if dx < 0: #moving left, hit right of wall
                  self.x = obj.rect.right-6
               
               if dy > 0: #moving down, hit top of wall
                  self.y = obj.rect.top-16
               if dy < 0: #moving up, hit bottom of wall
                  self.y = obj.rect.bottom
                  
            #colliding with spikes
            if isinstance(obj,Spike):
               self.gameScene.explosion(self.x,self.y,self.colour)
               self.gameScene.spawnTime = RESPAWN_DELAY
               self.gameScene.player = None
               
            #colliding with goal
            if isinstance(obj,Goal):
               self.gameScene.level+=1
               self.gameScene.loadLevel()
