#----------------------------
# Minecraft 2D
#----------------------------

import pygame, sys, random
from pygame.locals import *
from variables import *

#variables for the map size
TILESIZE  = 20
MAPWIDTH  = 30
MAPHEIGHT = 20

#maps each resource to the EVENT key used to place/craft it
controls = {event:event+49 for event in range(len(resources))}

#maps each resource to the KEYBOARD key used to place/craft it
invKeys = {key:str(1+key) for key in range(len(resources))}


class Map:
	def __init__(self, tileSize, initialWidth, initialHeight):
		self.tileSize = tileSize
		self.width = initialWidth
		self.height = initialHeight
		
		self.tiles = [ [DIRT for w in range(self.width)] for h in range(self.height) ]
		
		#loop through each row
		for rw in range(self.height):
			#loop through each column in that row
			for cl in range(self.width):
				#pick a random number between 0 and 10
				randomNumber = random.randint(0,10)
				#WATER if the random number is a 1 or a 2
				if randomNumber in [1,2]:
					tile = WATER
				#GRASS if the random number is a 3 or a 4
				elif randomNumber in [3,4]:
					tile = GRASS
				# WOOD if the random number is 5
				elif randomNumber in [5]:
					tile = WOOD
				#otherwise it's DIRT
				else:
					tile = DIRT
				#set the position in the map.tiles to the randomly chosen tile
				self.tiles[rw][cl] = tile
		

class Player:
	def __init__(self):
		self.pos = [0,0]
		self.inventory = {}
		for item in resources:
			self.inventory[item] = 0
		
class Game:
	def __init__(self, map, player):
		self.map = map
		self.player = player
	
	def eventLoop(self):
		#get all the user events
		for event in pygame.event.get():
			#if the user wants to quit
			if event.type == QUIT:
				#and the game and close the window
				pygame.quit()
				sys.exit()
			#if a key is pressed
			elif event.type == KEYDOWN:
				#if the right arrow is pressed
				if event.key == K_RIGHT and self.player.pos[0] < MAPWIDTH - 1:
					#change the self.player's x position
					self.player.pos[0] += 1
				if event.key == K_LEFT and self.player.pos[0] > 0:
					#change the self.player's x position
					self.player.pos[0] -= 1
				if event.key == K_UP and self.player.pos[1] > 0:
					#change the self.player's x position
					self.player.pos[1] -= 1
				if event.key == K_DOWN and self.player.pos[1] < MAPHEIGHT -1:
					#change the self.player's x position
					self.player.pos[1] += 1
				if event.key == K_SPACE:
					#what resource is the self.player standing on?
					currentTile = self.map.tiles[self.player.pos[1]][self.player.pos[0]]

					#if the user doesn't already have too many...
					if self.player.inventory[currentTile] < MAXTILES:

						#self.player now has 1 more of this resource
						self.player.inventory[currentTile] += 1
						#the self.player is now standing on dirt
						self.map.tiles[self.player.pos[1]][self.player.pos[0]] = DIRT

				for key in controls:    

					#if this key was pressed
					if (event.key == controls[key]):

						#CRAFT if shift is also pressed
						mods = pygame.key.get_mods()
						if mods & KMOD_SHIFT:

							#if the item can be crafted
							if key in craft:

								#keeps track of whether we have the resources
								#to craft this item
								canBeMade = True
								#for each item needed to craft...
								for i in craft[key]:
									#...if we don't have enough...
									if craft[key][i] > self.player.inventory[i]:
										#...we can't craft it!
										canBeMade = False
										break
								#if we can craft it (we have all needed resources)
								if canBeMade == True:
									#take each item from the self.player.inventory
									for i in craft[key]:
										self.player.inventory[i] -= craft[key][i]
									#add the crafted item to the self.player.inventory
									self.player.inventory[key] += 1
									
						#PLACE if shift wasn't pressed
						else:

							#get the tile the self.player is standing on
							currentTile = self.map.tiles[self.player.pos[1]][self.player.pos[0]]
							#if we have the item to place and not too many
							#of the item we're standing on
							if (self.player.inventory[key] > 0 and self.player.inventory[currentTile] < MAXTILES) or (self.player.inventory[key] > 0 and currentTile == DIRT):
								#take it from the self.player.inventory
								self.player.inventory[key] -= 1
								#if not full of dirt, then add it
								if not (currentTile == DIRT and self.player.inventory[DIRT] >19):
									#swap it with the tile we are standing on
									self.player.inventory[currentTile] += 1
								#place the item
								self.map.tiles[self.player.pos[1]][self.player.pos[0]] = key

	def start(self):
		fpsClock = pygame.time.Clock()
		
		#set up the display
		pygame.init()
		DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE + 400, MAPHEIGHT*TILESIZE + 70))

		#add a font for our inventory
		INVFONT = pygame.font.Font('FreeSansBold.ttf', 12)
				
		while True:
			#fill the background in black	    
			DISPLAYSURF.fill(BLACK)
			
			self.eventLoop()
							
			#loop through each row
			for row in range(MAPHEIGHT):
				#loop through each column in the row
				for column in range(MAPWIDTH):
					#draw the resource at that position in the map.tiles, using the correct image
					DISPLAYSURF.blit(textures[self.map.tiles[row][column]], (column*TILESIZE,row*TILESIZE))
				
			#display the player at the correct position 
			DISPLAYSURF.blit(PLAYER,(self.player.pos[0]*TILESIZE, self.player.pos[1]*TILESIZE))

			#draw a rectangle behind the instructions
			pygame.draw.rect(DISPLAYSURF, BLACK, (MAPWIDTH*TILESIZE, 0, 200, MAPHEIGHT * TILESIZE))

			#display the inventory, starting 10 pixels in
			xPosition = 10
			
			for item in resources:
				#add the image
				DISPLAYSURF.blit(textures[item],(xPosition,MAPHEIGHT*TILESIZE+20))
				xPosition += 30
				#add the text showing the amount in the inventory
				textObj = INVFONT.render(str(self.player.inventory[item]), True, WHITE, BLACK)
				DISPLAYSURF.blit(textObj,(xPosition,MAPHEIGHT*TILESIZE+20))

				#display the key
				textObj = INVFONT.render("Key : " + invKeys[item], True, WHITE, BLACK)
				DISPLAYSURF.blit(textObj,(xPosition-TILESIZE,MAPHEIGHT*TILESIZE+20+TILESIZE))

				#move along to place the next player.inventory item
				xPosition += 50
		   
			#add the text showing each line of the instructions
			pos = 10
			for item in instructions:
				craftText = INVFONT.render(item, True, WHITE, BLACK)
				DISPLAYSURF.blit(craftText,(MAPWIDTH*TILESIZE+20,pos))
				pos+=20

			#update the display
			pygame.display.update()
			#create a short delay
			fpsClock.tick(24)

def main():
	map = Map(TILESIZE, MAPWIDTH, MAPHEIGHT)
	player = Player()
	game = Game(map, player)
	game.start()

if __name__ == '__main__':	
	main()
