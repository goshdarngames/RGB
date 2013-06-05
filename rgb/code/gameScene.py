################################################################################
# gameScene.py
################################################################################
# This scene handles the main game logic.
################################################################################
# 09/09 Flembobs
################################################################################

import pygame
import random
import os
import colour as COLOUR

from scene import Scene
from player import Player
from wall import Wall
from spike import Spike
from goal import Goal
from gameOver import GameOver
from particles import *

################################################################################
# CLASS DEFINITION
################################################################################

class GameScene(Scene):
   
   def __init__(self,gameEngine):
      Scene.__init__(self, gameEngine)
      
      self.player = None
      self.objects = []
      
      self.spawn = (0,0) #spawn point of current level
      self.spawnTime = 0 #time until the player is respawned
      
      self.particleManager = ParticleManager(self)
      
      self.level = 1
      self.loadLevel()
   
   #----------------------------------------------------------------------------
      
   def update(self):
   
      self.particleManager.update()
   
      if self.spawnTime == 0:
         self.player.update()
      #player needs to be respawned
      elif self.spawnTime == 1:
         self.spawnTime = 0
         self.player = Player(self,self.spawn[0],self.spawn[1])
      else:
         self.spawnTime-=1
         
   #----------------------------------------------------------------------------
      
   def render(self):
      
      for obj in self.objects:
         obj.draw()
      
      self.particleManager.render()
      
      if self.player is not None:
         self.player.draw()
         self.drawHUD()
         
   #----------------------------------------------------------------------------
   
   def drawHUD(self):
      
      gE = self.gameEngine
      
      #left arrow
      imgStr = os.path.join("hud",COLOUR.colourToWord(self.player.rColour1))
      img = gE.resourceManager.getImage(imgStr)
      gE.screen.blit(img,(0,464))
      
      #right arrow
      imgStr = os.path.join("hud",COLOUR.colourToWord(self.player.rColour2))
      img = gE.resourceManager.getImage(imgStr)
      img = pygame.transform.flip(img,True,False)
      gE.screen.blit(img,(16,464))
         
   #----------------------------------------------------------------------------
   
   def explosion(self,x,y,colour):
      numParticles = random.random()*100+100
      
      for i in range(0,int(numParticles)):
         
         xspeed = random.random()*5
         yspeed = random.random()*5
         
         if int(xspeed) is 0:
            yspeed+=1
         
         if random.random()<0.5:
            xspeed *= -1
         
         if random.random()<0.5:
            yspeed *= -1 
         
         particle = Particle(x,y,xspeed,yspeed,colour,random.random()*90+30)
         
         self.particleManager.queueAddParticle(particle)
   
   #----------------------------------------------------------------------------
      
   def loadLevel(self):
      try:
         f = open("data/levels/%03d"%self.level)
      except IOError:
         self.gameEngine.scene = GameOver(self.gameEngine)
         return
      
      del self.objects[:]
      x=y=0   
      
      while 1:
         row = f.readline()
         if not row:
            break
            
         for col in row:
            
            obj=None
            
            #S == start
            if col == "S":
               self.player = Player(self,x,y)
               self.spawn = (x,y)
               
            #E == end
            if col == "E":
               obj = Goal(self,x,y)
            
            #walls
            if col == "W":
               obj = Wall(self,x,y,(255,255,255))
            if col == "R":
               obj = Wall(self,x,y,(255,0,0))
            if col == "G":
               obj = Wall(self,x,y,(0,255,0))
            if col == "B":
               obj = Wall(self,x,y,(0,0,255))
            if col == "M":
               obj = Wall(self,x,y,(255,0,255))
            if col == "C":
               obj = Wall(self,x,y,(0,255,255))
            if col == "Y":
               obj = Wall(self,x,y,(255,255,0))
               
            #spikes
            if col == "w":
               obj = Spike(self,x,y,(255,255,255))
            if col == "r":
               obj = Spike(self,x,y,(255,0,0))
            if col == "g":
               obj = Spike(self,x,y,(0,255,0))
            if col == "b":
               obj = Spike(self,x,y,(0,0,255))
            if col == "m":
               obj = Spike(self,x,y,(255,0,255))
            if col == "c":
               obj = Spike(self,x,y,(0,255,255))
            if col == "y":
               obj = Spike(self,x,y,(255,255,0))
            
               
            if obj is not None:
               self.objects.append(obj)
            x+=16
         y+=16
         x=0
