import pygame

#--------------------------
# Minecraft 2D -- Variables
#--------------------------


#the maximum number of each resource that can be held
#----------------------------------------------------

MAXTILES  = 12


#the title bar text/image
#------------------------

pygame.display.set_caption('pygame window')
pygame.display.set_icon(pygame.image.load('player.png'))


#variables for representing colours
#----------------------------------

BLACK = (0,     0,     0  )
BROWN = (153,   76,    0  )
GREEN = (0,     255,   0  )
BLUE  = (0,     0,     255)
WHITE = (255,   255,   255)


#variables representing the different resources
#----------------------------------------------

DIRT    = 0
GRASS   = 1
WATER   = 2
BRICK   = 3
WOOD    = 4
PLANK	= 5

#a list of all game resources
#----------------------------

resources = [DIRT,GRASS,WATER,BRICK,WOOD,PLANK]


#a dictionary linking resources to textures
#------------------------------------------

textures =   {
                DIRT    : pygame.image.load('dirt.png'),
                GRASS   : pygame.image.load('grass.png'),
                WATER   : pygame.image.load('water.png'),
                BRICK   : pygame.image.load('brick.png'),
				WOOD	: pygame.image.load('wood.png'),
				PLANK	: pygame.image.load('plank.png')
             }


#the number of each resource that we have to start with
#------------------------------------------------------

inventory =   {
                DIRT    : 10,
                GRASS   : 10,
                WATER   : 10,
                BRICK   : 3,
				WOOD	: 5,
				PLANK	: 5
            }


#the player image
#----------------

PLAYER = pygame.image.load('player.png')


#rules to make new objects
#-------------------------

craft = {
            BRICK    : { WATER : 1, DIRT : 2 },
			PLANK	 : { WOOD : 3 }
        }


#instructions list
#-----------------

instructions =  [
                    "Minecraft 2D",
                    "Instructions:",
                    "   ARROW KEYS = move",
                    "   SPACE = Pick up tile",
                    "   NUMBER KEYS = Place tile",
                    "   SHIFT + NUMBER KEYS = Craft tile",
                    "",
                    "Crafting Rules:",
                    "   BRICK = 2xDIRT + 1xWATER",
					"   PLANK = 3xWOOD"
                ]
