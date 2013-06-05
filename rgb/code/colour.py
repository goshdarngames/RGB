################################################################################
# colour.py
################################################################################
# A group of functions for managing the colour use within the game.
################################################################################
# 09/09 Flembobs
################################################################################

def colourToWord(colour):
   """
   Translates an (r,g,b) tuple into its english equivalent.
   """

   word = {
      (255,0,0):"red",
      (0,255,0):"green",
      (0,0,255):"blue",
      
      (255,255,0):"yellow",
      (0,255,255):"cyan",
      (255,0,255):"magenta",
      
      (255,255,255):"white"
   }
   return word[colour]
   
def colourCollision(c1,c2):
   """
   Tests two (r,g,b) tuples to see if the colours overlap, returning true if so.
   """
   
   for i in range(0,3):
      if c1[i] & c2[i]:
         return True
   return False
