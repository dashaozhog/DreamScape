from pygame import *
import sys
from settings import *
from overworld import Overworld
from level import Level

class Game:
	def __init__(self):
		self.max_level = 2
		self.overworld = Overworld(1, self.max_level, window, self.create_level)
		self.status =  'overworld'

	def create_level(self, current_level):
		self.level = Level(current_level, window, self.create_overworld)
		self.status = 'level'

	def create_overworld(self, current_level, new_max_level):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(current_level, self.max_level, window, self.create_level)
		self.status = 'overworld'
	def run(self):
		if self.status == 'overworld':
			self.overworld.run()
		else:
			self.level.run()
window = display.set_mode((win_w, win_h))
clock = time.Clock()
game = Game()

while True:
	for ev in event.get():
		if ev.type == QUIT: 
			quit()
			sys.exit()
	window.fill('grey')
	game.run()

	display.update()
	clock.tick(60) 