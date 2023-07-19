# Eric Broadbent
# 7/11/23
# Zelda like action rpg
from settings import *
from level import *

# left off at 4:57:28 just finished seting up enemy starting on player enamy interactions

class Game:
	def __init__(self):
		  
		# general setup
		pg.init()
		self.screen = pg.display.set_mode((WIDTH,HEIGTH))
		pg.display.set_caption(title)
		self.icon = pg.image.load(icon_path).convert_alpha()
		pg.display.set_icon(self.icon)
		self.clock = pg.time.Clock()
		self.level = Level()
	
	def run(self):
		while True:
			self.game_events()
			self.update()
			self.draw()
			self.clock.tick(FPS)

	def game_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()

	def update(self):
		self.level.run()

	def draw(self):


		pg.display.update()


if __name__ == '__main__':
	game = Game()
	game.run()
