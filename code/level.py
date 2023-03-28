from pygame import *
from tiles import Tile
from settings import tile_size,win_w
from player import Player
class Level:
	def __init__(self, level_data, surface):
		self.surface = surface
		self.worldshift = 0
		self.player = sprite.GroupSingle()
		self.setup(level_data)

	def setup(self, layout):
		self.tiles = sprite.Group()
		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index*tile_size
				y = row_index	* tile_size	
				if cell == 'X':
					tile = Tile((x,y), tile_size)
					self.tiles.add(tile)
				if cell == "P":	
					playerspr = Player((x,y))
					self.player.add(playerspr)

	def scroll_X(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < win_w/4 and direction_x<0:
			self.worldshift = 8
			player.speed = 0
		elif player_x >win_w - (win_w/4) and direction_x>0:
			self.worldshift = -8
			player.speed = 0
		else:
			self.worldshift = 0
			player.speed = 8

	def hor_collide(self):
		player = self.player.sprite

		player.rect.x +=player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
	def ver_collide(self):
		player = self.player.sprite
		player.apply_gravity()
		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True
		if player.on_ground and player.direction.y < 0 or player.direction.y >1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0:
			player.on_ceiling= False

					
		
	def run(self):

		self.tiles.update(self.worldshift)
		self.tiles.draw(self.surface)
		self.scroll_X()

		
		self.player.update()
		self.hor_collide()
		self.ver_collide()
		self.player.draw(self.surface)