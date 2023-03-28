from pygame import *
import sys
from settings import *
from level import Level

window = display.set_mode((win_w, win_h))
clock = time.Clock()

level = Level(level_map, window)


while True:
	for ev in event.get():
		if ev.type == QUIT:
			quit()
			sys.exit()
	
	window.fill('grey')
	level.run()

	display.update()
	clock.tick(60)