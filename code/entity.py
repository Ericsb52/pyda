from settings import *



class Weapon(pg.sprite.Sprite):
    def __init__(self,player,game):
        self.game = game
        super().__init__([self.game.weapon_sprites,self.game.all_sprites])

        self.player = player
        self.type = "weapon"

        self.dir = self.player.status.split("_")[0]
        weapon_img_path = f"../graphics/weapons/{self.player.weapon}/{self.dir}.png"


        self.image = pg.image.load(weapon_img_path).convert_alpha()
        if self.dir == "right":
            self.rect = self.image.get_rect(midleft = self.player.rect.midright+Vector2(0,16))
        elif self.dir == "left":
            self.rect = self.image.get_rect(midright = self.player.rect.midleft+Vector2(0,16))
        elif self.dir == "up":
            self.rect = self.image.get_rect(midbottom = self.player.rect.midtop+Vector2(-10,0))
        elif self.dir == "down":
            self.rect = self.image.get_rect(midtop = self.player.rect.midbottom+Vector2(-10,0))
        else:
            self.image = pg.Surface((40, 40))
            self.rect = self.image.get_rect(center=self.player.rect.center)


    def update(self):
        if self.player.is_attacking == False:
            self.kill()

# not sure why we need this i made tha calls to heal and flame in the player
# may want to set this up as a object in the player that is created with the player
# and have it store all the logic for the magic system
# then it could be uses with a class system mage would get a magic system where a warior wouldent
class Magic_Player():
    def __init__(self,level):
        self.level = level
    def heal(self,target):
        self.level.animation_player.create_particles("aura",target.rect.center,[self.level.all_sprites])
        self.level.animation_player.create_particles("heal", target.rect.center+Vector2(0,-60), [self.level.all_sprites])

    def flame(self,strength,owner):
        if "right" in owner.status:
            direction = Vector2(1, 0)
        elif "left" in owner.status:
            direction = Vector2(-1, 0)
        elif "up" in owner.status:
            direction = Vector2(0, -1)
        elif "down" in owner.status:
            direction = Vector2(0, 1)
        for i in range(1,6):
            if direction.x:# horizontal
                offset_x = (direction.x * i)*TILESIZE
                x = owner.rect.centerx + offset_x + random.randint(-TILESIZE//3,TILESIZE//3)
                y = owner.rect.centery + random.randint(-TILESIZE//3,TILESIZE//3)
                self.level.animation_player.create_particles("flames", (x,y), [self.level.all_sprites,self.level.weapon_sprites])
            else: # vertical
                offset_y = (direction.y * i) * TILESIZE
                x = owner.rect.centerx + random.randint(-TILESIZE//3,TILESIZE//3)
                y = owner.rect.centery + offset_y + random.randint(-TILESIZE//3,TILESIZE//3)
                self.level.animation_player.create_particles("flames", (x, y), [self.level.all_sprites,self.level.weapon_sprites])


class UI:
    def __init__(self,level):
        self.level = level
        self.player = self.level.player
        self.screen = pg.display.get_surface()
        self.font = pg.font.Font(UI_FONT,UI_FONT_SIZE)

        self.health_bar_rect = pg.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pg.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon["graphic"]
            weapon = pg.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic["graphic"]
            magic = pg.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)


    def display(self):
        self.draw_bar(self.player.health,self.player.stats["health"],self.health_bar_rect,health_color)
        self.draw_bar(self.player.energy, self.player.stats["energy"], self.energy_bar_rect,energy_color)
        self.show_exp(self.player.exp)
        self.weapon_overlay()
        self.magic_overlay()
        # self.selection_box(10+ITEM_BOX_SIZE+10, self.screen.get_height() - 90,"Magic")

    def show_exp(self,info):
        text_surf = self.font.render("XP: "+str(int(info)),False,text_color)
        x = self.screen.get_width()
        y = self.screen.get_height()
        text_rect = text_surf.get_rect(bottomright = (x-70,y-20))

        pg.draw.rect(self.screen,ui_bg_color,text_rect.inflate(100,20))
        self.screen.blit(text_surf,text_rect)
        pg.draw.rect(self.screen, ui_border_color, text_rect.inflate(100, 20),3)

    def draw_bar(self,cur_ammount,max_ammount,bg_rect,color):
        pg.draw.rect(self.screen,ui_bg_color,bg_rect)
        ratio = cur_ammount / max_ammount
        cur_width = bg_rect.width * ratio
        cur_rect = bg_rect.copy()
        cur_rect.width = cur_width

        pg.draw.rect(self.screen,color,cur_rect)
        pg.draw.rect(self.screen,ui_border_color,bg_rect,3)

    def selection_box(self,left,top,name):
        text_surf = self.font.render(name, False, text_color)
        bg_rect = pg.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        text_rect = text_surf.get_rect(midbottom = (bg_rect.midtop))


        self.screen.blit(text_surf, text_rect)

        pg.draw.rect(self.screen,ui_bg_color,bg_rect)

        return bg_rect

    def weapon_overlay(self):
        bg_rect = self.selection_box(10, self.screen.get_height() - 90, "Space")
        weapon_surf = self.weapon_graphics[self.player.weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        if not self.player.can_switch_wep:
            pg.draw.rect(self.screen, ui_border_color_active, bg_rect, 3)
        else:
            pg.draw.rect(self.screen, ui_border_color, bg_rect, 3)
        text_surf = self.font.render("Q", False, text_color)
        text_rect = text_surf.get_rect(topleft=(bg_rect.x+5,bg_rect.y +1))


        self.screen.blit(weapon_surf,weapon_rect)
        self.screen.blit(text_surf, text_rect)

    def magic_overlay(self):
        bg_rect = self.selection_box(10+ITEM_BOX_SIZE+5, self.screen.get_height() - 90, "Tab")
        magic_surf = self.magic_graphics[self.player.magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        if not self.player.can_switch_magic:
            pg.draw.rect(self.screen, ui_border_color_active, bg_rect, 3)
        else:
            pg.draw.rect(self.screen, ui_border_color, bg_rect, 3)

        text_surf = self.font.render("E", False, text_color)
        text_rect = text_surf.get_rect(topleft=(bg_rect.x+5,bg_rect.y +1))

        self.screen.blit(magic_surf, magic_rect)
        self.screen.blit(text_surf, text_rect)



class Entity(pg.sprite.Sprite):
    def __init__(self,groups,level):
        super(Entity, self).__init__(groups)
        self.level  = level
        self.dir = Vector2()
        self.frame_index = 0
        self.animation_speed = animation_speed

        self.vulnerable = True
        self.hit_time = 0
        self.hit_cooldown = 500

    def wave_value(self):
        value = sin(pg.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
    def move(self, speed):
        if self.dir.magnitude() != 0:
            self.dir = self.dir.normalize()

        self.hitBox.centerx += self.dir.x * speed
        self.collisions("horizontal")
        self.hitBox.centery += self.dir.y * speed
        self.collisions("vertical")
        self.rect.center = self.hitBox.center

    def collisions(self, dir):
        if dir == "horizontal":
            for sprite in self.level.obstacle_sprites:
                if sprite.hitBox.colliderect(self.hitBox):
                    if self.dir.x > 0:
                        self.hitBox.right = sprite.hitBox.left
                    if self.dir.x < 0:
                        self.hitBox.left = sprite.hitBox.right

        if dir == "vertical":
            for sprite in self.level.obstacle_sprites:
                if sprite.hitBox.colliderect(self.hitBox):
                    if self.dir.y > 0:
                        self.hitBox.bottom = sprite.hitBox.top
                    if self.dir.y < 0:
                        self.hitBox.top = sprite.hitBox.bottom
