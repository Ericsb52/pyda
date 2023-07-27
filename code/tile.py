from settings import *

class Tile(pg.sprite.Sprite):
    def __init__(self,level,pos,groups,sprite_type,surf = pg.Surface((TILESIZE,TILESIZE))):
        super(Tile, self).__init__(groups)
        self.level = level
        self.sprite_type = sprite_type
        self.image = surf
        if sprite_type == "object":
            self.rect = self.image.get_rect(topleft = (pos[0],pos[1]-TILESIZE))
            self.hitBox = self.rect.inflate(hibox_x_offset_obj,hibox_y_offset_obj)
        else:
            self.rect = self.image.get_rect(topleft = pos)
            self.hitBox = self.rect.inflate(hibox_x_offset_grass,hibox_y_offset_grass)
        self.z = ""

    def destroy(self):


        self.kill()



