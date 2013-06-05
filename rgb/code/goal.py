################################################################################
# goal.py
################################################################################
# The green door that the player must touch to advance a level
################################################################################
# 10/09 Flembobs
################################################################################

from gameObject import GameObject

class Goal(GameObject):
   
   def __init__(self,gameScene,x,y):
      GameObject.__init__(self,gameScene,x,y,16,16)
      
   def draw(self):
      gE = self.gameScene.gameEngine
      
      imgStr = "goal"
      img = gE.resourceManager.getImage(imgStr)
      
      gE.screen.blit(img,(self.rect.x,self.rect.y))
