from pygame import *
import sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI
mixer.init()

class Game:
	def __init__(self):
		# game attributes
		self.max_level = 0
		self.max_health = 100
		self.cur_health = 100
		self.coins = 0
		# overworld
		self.overworld = Overworld(0, self.max_level, window, self.create_level)
		self.status =  'overworld'
		self.gameover_sound = mixer.Sound('../graphics/ui/gameover.wav')
		self.new_level_SOUND = mixer.Sound('../graphics/ui/new level.wav')

		self.ui = UI(window)
		mixer.music.load('../graphics/ui/music.mp3')
		mixer.music.set_volume(0.5)
		mixer.music.play(-1)

	def create_level(self, current_level):
		self.level = Level(current_level, window, self.create_overworld, self.change_coins, self.change_health)
		self.status = 'level'

	def create_overworld(self, current_level, new_max_level):
		# mixer.music.rewind()
		if new_max_level > self.max_level:
			self.max_level = new_max_level
			self.new_level_SOUND.play()
		self.overworld = Overworld(current_level, self.max_level, window, self.create_level)
		self.status = 'overworld'
	def change_coins(self, amount):
		self.coins += amount

	def change_health(self, amount):
		self.cur_health+=amount
	def check_game0ver(self):
		if self.cur_health <= 0:
			self.gameover_sound.play()
			self.cur_health = 100
			self.coins = 0
			self.max_level = 0
			self.overworld = Overworld(0, self.max_level, window, self.create_level)
			self.status =  'overworld'


	def run(self):
		if self.status == 'overworld':
			self.overworld.run()
		else:
			self.level.run()
			self.ui.show_health(self.cur_health, self.max_health)
			self.ui.show_coins(self.coins)
			self.check_game0ver()



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