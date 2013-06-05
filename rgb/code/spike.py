################################################################################
# spike.py
################################################################################
# The class definition for spikes that kill the player.
################################################################################
# 09/09 Flembobs
################################################################################

import os

from gameObject import GameObject
import colour as COLOUR

class Spike(GameObject):
   
   def __init__(self,gameScene,x,y,colour):
      GameObject.__init__(self,gameScene,x,y,16,16,colour)
      
   def draw(self):
      gE = self.gameScene.gameEngine
      
      imgStr = os.path.join("spikes",COLOUR.colourToWord(self.colour))
      img = gE.resourceManager.getImage(imgStr)
      
      gE.screen.blit(img,(self.rect.x,self.rect.y))
