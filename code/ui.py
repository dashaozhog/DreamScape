from pygame import * 
font.init()
class UI:
	def __init__(self, surface):

		# setup
		self.display_surface = surface

		# health
		self.health_bar = image.load('../graphics/ui/healthbar.png').convert_alpha()
		self.health_bar_topleft = (52,19)
		self.bar_max_width = 82
		self.bar_height = 15
		# coin
		self.coin = transform.scale(image.load('../graphics/ui/coin.png').convert_alpha(), (24,24))
		self.coin_rect = self.coin.get_rect(center = (36, 60))
		self.font = font.Font("../graphics/ui/PublicPixel.ttf", 20)

	def show_health(self,cur, full):
		self.display_surface.blit(self.health_bar, (20,10)) 
		cur_health_ratio = cur/full
		cur_bar_width = self.bar_max_width*cur_health_ratio
		health_bar_rect = Rect((self.health_bar_topleft),(cur_bar_width,self.bar_height))
		draw.rect(self.display_surface, "#cd95f0",health_bar_rect)

	def show_coins(self, amount):
		self.display_surface.blit(self.coin, self.coin_rect)
		coins_label = self.font.render(str(amount), True, '#75005e')
		
		coins_label_rect = coins_label.get_rect(midleft = (self.coin_rect.right+4, self.coin_rect.centery))
		self.display_surface.blit(coins_label, coins_label_rect)