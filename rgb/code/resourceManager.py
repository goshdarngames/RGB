################################################################################
# resourceManager.py
################################################################################
# The resource manager loads and stores the images used in the game.
################################################################################
# 09/09 GoshDarnGames
################################################################################

import os
import pygame

IMAGE_DIR = os.path.join("data","images")

class ResourceManager:
   
   def __init__(self):
      self.images = dict()
      self.__loadImages()
   
   def getImage(self,img):
      img = os.path.join(IMAGE_DIR,img)
      return self.images[img]
   
   def __loadImages(self):
      
      walker = os.walk(IMAGE_DIR)
      
      while 1:
         try:
            contents = walker.next()
         except StopIteration:
            break
         
         files = contents[2]
         path = contents[0]
         for f in files:
            fname=os.path.join(path,f)
            surf = pygame.image.load(fname)
            surf.convert()
            
            #remove the png and use filename as dict key
            self.images[fname[:-4]]=surf
