from pygame import *
from settings import win_h, win_w
from game_data import levels
font.init()

class Level:
	def __init__(self, current_level, surface, create_overworld):

		self.display_surface = surface
		self.current_level = current_level
		level_data = levels[current_level]
		level_content = level_data['content']
		self.new_max_level = level_data['unlock']
		self.create_overworld = create_overworld

		self.font = font.Font(None, 40)
		self.text_surface = self.font.render(level_content, True, "white")
		self.text_rect = self.text_surface.get_rect(center = (win_w/2, win_h/2))


	def input(self):
		keys = key.get_pressed()
		if keys[K_RETURN]:
			self.create_overworld(self.current_level, self.new_max_level)
		if keys[K_ESCAPE]:
			self.create_overworld(self.current_level,0)
	def run(self):
		self.input()
		self.display_surface.blit(self.text_surface, self.text_rect)
