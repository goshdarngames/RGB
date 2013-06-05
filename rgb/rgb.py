################################################################################
# rgb.py
################################################################################
# Contains the game engine.
################################################################################
# 09/09 Flembobs
################################################################################

import pygame
import os

from code.resourceManager import ResourceManager
from code.gameScene import GameScene

class GameEngine:
   
   #############################################################################
   # INIT
   #############################################################################
   
   def __init__(self):      
      #Initialise pygame
      os.environ["SDL_VIDEO_CENTERED"] = "1"
      pygame.init()

      # Set up the display
      pygame.display.set_caption("RGB")
      self.screen = pygame.display.set_mode((640, 480))

      self.clock = pygame.time.Clock()
      
      self.resourceManager = ResourceManager()
      
      self.scene = GameScene(self)
      
      self.events = []
      
   
   #############################################################################
   # MAIN GAME LOOP
   #############################################################################
   
   def loop(self):
   
      while True:
         
         self.__getEvents()
         
         self.clock.tick(60)
         self.screen.fill((0,0,0))
         
         self.scene.update()
         self.scene.render()
         
         pygame.display.flip()
         
         if self.__checkQuit():
            break
         
   #############################################################################
   # FUNCTIONS
   #############################################################################
   
   def __checkQuit(self):
   
      for e in self.events:
         if e.type == pygame.QUIT:
            return True
         if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            return True
   
      return False
      
   def __getEvents(self):
      self.events = pygame.event.get()
   
################################################################################
# Executable Logic
################################################################################

gE = GameEngine()
gE.loop()
pygame.quit()
