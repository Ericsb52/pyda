import random

from settings import *
from tile import *
from player import *
from support import *
from enemy import *
from entity import *
from particles import *


class All_sprites_Camera_Group(pg.sprite.Group):
    def __init__(self):
        super(All_sprites_Camera_Group, self).__init__()
        self.screen = pg.display.get_surface()
        self.offset_x = self.screen.get_width()//2
        self.offset_y = self.screen.get_height()//2
        self.offset = Vector2()

        self.floor_img = pg.image.load(floor_img_path)
        self.floor_rect = self.floor_img.get_rect(topleft = (0,0))


    def custom_draw(self,player):
        self.offset.x = player.rect.centerx - self.offset_x
        self.offset.y = player.rect.centery - self.offset_y
        self.floor_offset_pos = self.floor_rect.topleft - self.offset
        self.screen.blit(self.floor_img,self.floor_offset_pos)

        for sprite in sorted(self.sprites(),key=lambda sprite:sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image,offset_pos)


class Level:
    def __init__(self):
        self.screen = pg.display.get_surface()
        # sprite groups
        self.all_sprites = All_sprites_Camera_Group()
        self.obstacle_sprites = pg.sprite.Group()
        self.weapon_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.destroyable_sprites = pg.sprite.Group()

        # create map
        self.create_map()
        self.ui = UI(self)

        self.animation_player = AnimationPlayer(self)




    def create_map(self):
        layouts = {
            "boundary":import_csv_layout(layout_boundary_path),
            "grass":import_csv_layout(layout_grass_path),
            "object":import_csv_layout(layout_object_path),
            "entities":import_csv_layout(layout_entity_path)
        }
        graphics = {
            "grass":import_folder(grass_path),
            "objects":import_folder(obj_path)
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index,col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile(self,(x, y), [self.obstacle_sprites],"invisable",)
                        if style == "grass":
                            Tile(self,(x,y),
                                 [self.all_sprites,self.obstacle_sprites,self.destroyable_sprites],
                                 "grass",
                                 surf=random.choice(graphics["grass"]))
                        if style == "object":
                            Tile(self,(x,y),[self.all_sprites,self.obstacle_sprites],"object",surf=graphics["objects"][int(col)]),
                        if style == "entities":
                            if col == "394":
                                self.player = Player((x,y), self.all_sprites, self)
                            else:
                                if col == "390":
                                    monster_type = "bamboo"
                                elif col == "391":
                                    monster_type = "spirit"
                                elif col == "392":
                                    monster_type = "raccoon"
                                elif col == "393":
                                    monster_type = "squid"

                                Enemy(self,monster_type,(x,y),[self.all_sprites,self.enemy_sprites])






        #         if col == "x":
        #
        #         if col == "p":
        #             self.player = Player((x,y),self.all_sprites,self)

    def level_events(self):
        pass

    def level_update(self):
        self.all_sprites.update()

        # player attack logic
        # checking if player hit an enemy
        if self.weapon_sprites:
            for wep in self.weapon_sprites:
                hits = pg.sprite.spritecollide(wep,self.enemy_sprites,False)
                if hits:
                    for hit in hits:
                        hit.take_damage(wep.type)

        # cheking if we hit grass or other destroyable object
        if self.weapon_sprites:
            for wep in self.weapon_sprites:
                hits = pg.sprite.spritecollide(wep, self.destroyable_sprites, False)
                if hits:
                    for hit in hits:
                        pos  = hit.rect.center
                        offset = Vector2(0,75)
                        for i in range(random.randint(3,6)):
                            self.animation_player.create_grass_particles(pos-offset, [self.all_sprites])
                        hit.destroy()

    def level_draw(self):
        self.screen.fill("black")
        self.all_sprites.custom_draw(self.player)

    def debug_Text(self):
        debug(self.player.dir)
        debug(self.player.status,y = 40,x = 10)
        debug(len(self.weapon_sprites),y=75,x=10)

    def run(self):

        self.level_events()
        self.level_update()
        self.level_draw()
        self.ui.display()

        # self.debug_Text()


