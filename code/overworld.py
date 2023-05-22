from pygame import *
from game_data import levels
from support import import_folder
from decorations import Sky, Clouds
from settings import win_w

class Node(sprite.Sprite):
	def __init__(self, pos, status, icon_speed, path):
		super().__init__()
		self.speed = 0.15
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = transform.scale(self.frames[int(self.frame_index)], (128,128))
		if status == 'available':
			self.status = 'available'
		else:
			self.status = 'locked'

		self.rect = self.image.get_rect(center = pos)

		self.detection_zone = Rect(self.rect.centerx-(icon_speed/2),self.rect.centery-(icon_speed/2),icon_speed,icon_speed)

	def animate(self):
		self.frame_index +=self.speed
		if int(self.frame_index) >= 1:
			self.frame_index = 0
		self.image = transform.scale(self.frames[int(self.frame_index)], (128,128))
	def update(self):
		if self.status == 'available':
			self.animate()
		else:
			tint_surf = self.image.copy()
			tint_surf.fill("#f1e9f2", None, BLEND_RGBA_MULT)
			self.image.blit(tint_surf, (0,0))

class Icon(sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.pos = pos
		self.image = image.load('../graphics/overworld/owlet.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
	def update(self):
		self.rect.center = self.pos

class Overworld:
	def __init__(self, start_level, max_level, surface, create_level):

		self.display_surface = surface
		self.max_level = max_level
		self.current_level = start_level
		self.create_level = create_level

		self.moving = False
		self.move_dir = math.Vector2(0,0)
		self.speed = 8
		
		self.setup_nodes()
		self.setup_icon()
		self.sky = Sky(7, 'overworld')
		
	def setup_nodes(self):
		self.nodes = sprite.Group()

		for index,node in enumerate(levels.values()):
			if index <= self.max_level:
				node_sprite = Node(node['node_pos'], 'available', self.speed, node['node_graphics'])
			else:
				node_sprite = Node(node['node_pos'], 'locked', self.speed, node['node_graphics'])
			self.nodes.add(node_sprite)
	def draw_paths(self):
		if self.max_level!=0:
			points = [node['node_pos'] for index,node in enumerate(levels.values()) if index <= self.max_level]
			draw.lines(self.display_surface, "#f1e9f2", False, points, 6)

	def setup_icon(self):
		self.icon = sprite.GroupSingle()
		icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
		self.icon.add(icon_sprite)

	def input(self):
		keys = key.get_pressed()
		if not self.moving:
			if keys[K_RIGHT] and self.current_level <  self.max_level:
				self.move_dir = self.get_movement_data('next')
				self.current_level+=1
				self.moving = True
			elif keys[K_LEFT] and self.current_level>0:
				self.move_dir = self.get_movement_data('prev')
				self.current_level-=1
				self.moving = True
			elif keys[K_SPACE]:
				self.create_level(self.current_level)


	def get_movement_data(self, target):
		start = math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
		if target == 'next' :
			end = math.Vector2(self.nodes.sprites()[self.current_level+1].rect.center)
		else:
			end = math.Vector2(self.nodes.sprites()[self.current_level-1].rect.center)
		return(end - start).normalize()


	def update_icon_pos(self):
		if self.moving and self.move_dir:
			self.icon.sprite.pos += self.move_dir * self.speed
			target_node = self.nodes.sprites()[self.current_level]
			if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
				self.moving = False
				self.move_dir = math.Vector2(0,0)

	def run(self):
		self.input()
		self.update_icon_pos()
		self.icon.update()
		self.nodes.update()
		self.sky.draw(self.display_surface)
		self.draw_paths()
		self.nodes.draw(self.display_surface)
		self.icon.draw(self.display_surface)
		
