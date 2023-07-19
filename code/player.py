from settings import *
from support import  *
from entity import *

class Player(Entity):
    def __init__(self,pos,groups,level):
        super(Player, self).__init__(groups,level)
        # refreences
        self.import_assets()
        # sprite and hit box
        self.image = pg.image.load("../graphics/player/down/down_0.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitBox = self.rect.inflate(hibox_x_offset,hibox_y_offset)
        self.z = ""
        self.status = "down"

        # player Actions
        self.is_attacking = False
        self.attk_cooldown = attk_cooldown
        self.attk_time = 0

        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_wep = True
        self.switchTime = 0
        self.switch_dur = 200

        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.switchTime_magic = 0
        self.switch_dur_magic = 200

        # Stats
        # base Stats
        self.stats = {"health":100,"energy":60,"attack":10,"magic":4,"speed":player_speed}
        # cur stats
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.exp = 123
        self.speed = self.stats["speed"]

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitBox.center)

    def get_status(self):
        # if idle
        if self.dir.x == 0 and self.dir.y == 0:
            self.status = self.status.split("_")[0] +"_idle"

        if self.is_attacking:
            self.dir.x = 0
            self.dir.y = 0
            self.status = self.status.split("_")[0] + "_attack"

    def import_assets(self):
        path = animation_path
        self.animations = {"up":[],"down":[],"left":[],"right":[],
                      "up_idle":[],"down_idle":[],"left_idle":[],"right_idle":[],
                      "up_attack":[],"down_attack":[],"left_attack":[],"right_attack":[],
                      }
        for animation in self.animations.keys():
            fullpath = path+"/"+animation
            self.animations[animation] = import_folder(fullpath)

    def update(self):
        self.inputs()
        self.get_status()
        self.animate()
        self.cooldowns()
        self.move(self.speed)

    def inputs(self):
        # get all keys that are pressed
        keys = pg.key.get_pressed()
        if not self.is_attacking:
            # movind up or down
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.status = "up"
                self.dir.y = -1
            elif keys[pg.K_DOWN] or keys[pg.K_s]:
                self.status = "down"
                self.dir.y = 1
            else:
                self.dir.y =0

            # moving left or right
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.status = "left"
                self.dir.x = -1
            elif keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.status = "right"
                self.dir.x = 1
            else:
                self.dir.x = 0

            # attack input
            if keys[pg.K_SPACE] :
                self.attacking("weapon")

            # magic input
            if keys[pg.K_TAB] :
                self.attacking("magic")


            if keys[pg.K_q] and self.can_switch_wep :
                self.swap_weapon()

            if keys[pg.K_e] and self.can_switch_magic :
                self.swap_magic()

    def swap_magic(self):
        self.can_switch_magic = False
        self.switchTime_magic = pg.time.get_ticks()
        if self.magic_index < len(list(magic_data.keys())) - 1:
            self.magic_index += 1
        else:
            self.magic_index = 0
        print(self.magic_index)
        self.magic = list(magic_data.keys())[self.magic_index]

    def swap_weapon(self):
        self.can_switch_wep = False
        self.switchTime = pg.time.get_ticks()
        if self.weapon_index < len(list(weapon_data.keys()))-1:
            self.weapon_index += 1
        else:
            self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]

    def attacking(self, attk):
        self.is_attacking = True
        self.attk_time = pg.time.get_ticks()
        attk_type = attk
        if attk_type == "weapon":
            print("attk wep")
            self.create_attack()

        elif attk_type == "magic":
            style = list(magic_data.keys())[self.magic_index]
            strength = magic_data[style]["strength"] + self.stats["magic"]
            cost = magic_data[style]["cost"]
            self.create_magic(style, strength, cost)

    def create_attack(self):
        Weapon(self,self.level)

    def create_magic(self,style,strength,cost):
        print(style)
        print(strength)
        print(cost)

    def cooldowns(self):
        cur_time = pg.time.get_ticks()
        if self.is_attacking:
            if cur_time - self.attk_time >= self.attk_cooldown:
                self.is_attacking = False

        if not self.can_switch_wep:
            if cur_time - self.switchTime >= self.switch_dur:
                self.can_switch_wep = True

        if not self.can_switch_magic:
            if cur_time - self.switchTime_magic >= self.switch_dur_magic:
                self.can_switch_magic = True



class Weapon(pg.sprite.Sprite):
    def __init__(self,player,game):
        self.game = game
        super().__init__([self.game.weapon_sprites,self.game.all_sprites])

        self.player = player

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



