from settings import vertical_tile_num, tile_size, win_w
from pygame import *
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint

class Sky:
	def __init__(self, horizon, style = 'level'):
		self.top = image.load('../graphics/decorations/sky/top.png').convert()
		self.middle = image.load('../graphics/decorations/sky/middle.png').convert()
		self.bottom = image.load('../graphics/decorations/sky/bottom.png').convert()
		self.horizon = horizon

		self.top = transform.scale(self.top, (win_w, tile_size))
		self.middle = transform.scale(self.middle, (win_w, tile_size))
		self.bottom = transform.scale(self.bottom, (win_w, tile_size))

		self.style = style
		if self.style == 'overworld':
			palm_surfaces = import_folder('../graphics/overworld/palms')
			self.palms = []

			for surf in [choice(palm_surfaces) for image in range(10)]:
				x  = randint(0,win_w)
				y = (self.horizon*tile_size)+randint(50,100)
				rect = surf.get_rect(midbottom = (x,y))
				self.palms.append((surf, rect))
			cloud_surfaces = import_folder('../graphics/overworld/clouds')
			self.clouds = []

			for surf in [choice(cloud_surfaces) for image in range(10)]:
				x  = randint(0,win_w)
				y = randint(0,(self.horizon*tile_size)-100)
				rect = surf.get_rect(midbottom = (x,y))
				self.clouds.append((surf, rect))

	def draw(self,surface):
		for row in range(vertical_tile_num):
			y = row* tile_size
			if row < self.horizon:
				surface.blit(self.top, (0,y))
			elif row == self.horizon:
				surface.blit(self.middle, (0,y))
			else:
				surface.blit(self.bottom, (0,y))

		if self.style == 'overworld':
			for palm in self.palms:
				surface.blit(palm[0], palm[1])
			for cloud in self.clouds:
				surface.blit(cloud[0], cloud[1])




class Water:
	def __init__(self, top, level_width):
		start = -win_w
		tile_w = 192
		tile_x_amount = int((level_width + win_w*2) / tile_w)
		self.water_sprites = sprite.Group()

		for tile in range(tile_x_amount):
			x = tile * tile_w + start
			y = top
			tile_sprite = AnimatedTile(192, x,y, "../graphics/decorations/water")
			tile_sprite.speed = 0.1
			self.water_sprites.add(tile_sprite)
	def draw(self,surface, shift):
		self.water_sprites.update(shift)
		self.water_sprites.draw(surface)

class Clouds:
	def __init__(self, horizon, level_width, cloud_num, style = 'level'):
		cloud_surf_list = import_folder('../graphics/decorations/clouds')
		min_x  = - win_w
		max_x = level_width + win_w
		min_y = 0 
		max_y = horizon
		self.cloud_sprites = sprite.Group()

		for cloud in range(cloud_num):
			cloud = transform.scale(choice(cloud_surf_list), (150,80))
			x = randint(min_x, max_x)
			y = randint(min_y, max_y)
			tile_sprite =  StaticTile(0, x, y, cloud)
			self.cloud_sprites.add(tile_sprite)
	def draw(self, surface, shift):
		self.cloud_sprites.update(shift)
		self.cloud_sprites.draw(surface)