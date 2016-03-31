################################################################################
# Wall.py
################################################################################
# The class for walls/platforms.
################################################################################
# 09/09 GoshDarnGames
################################################################################

from gameObject import GameObject

class Wall(GameObject):
   
   def __init__(self,gameScene,x,y,colour):
      GameObject.__init__(self,gameScene,x,y,16,16,colour)
