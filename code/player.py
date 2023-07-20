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

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def take_damage(self,ammount):
        if self.vulnerable:
            self.health -= ammount
            self.vulnerable = False
            self.hit_time = pg.time.get_ticks()
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
            self.create_attack()
        elif attk_type == "magic":
            style = list(magic_data.keys())[self.magic_index]
            strength = magic_data[style]["strength"] + self.stats["magic"]
            cost = magic_data[style]["cost"]
            self.create_magic(style, strength, cost)

    def create_attack(self):
        Weapon(self,self.level)

    def get_weapon_dmg(self):
        base_dmg =self.stats["attack"]
        weapon_dmg = weapon_data[self.weapon]["damage"]
        return base_dmg+weapon_dmg

    def create_magic(self,style,strength,cost):
        print(style)
        print(strength)
        print(cost)

    def cooldowns(self):
        cur_time = pg.time.get_ticks()
        if self.is_attacking:
            if cur_time - self.attk_time >= self.attk_cooldown + weapon_data[self.weapon]["cooldown"]:
                self.is_attacking = False

        if not self.can_switch_wep:
            if cur_time - self.switchTime >= self.switch_dur:
                self.can_switch_wep = True

        if not self.can_switch_magic:
            if cur_time - self.switchTime_magic >= self.switch_dur_magic:
                self.can_switch_magic = True

        if not self.vulnerable:
            if cur_time - self.hit_time >= self.hit_cooldown:
                self.vulnerable = True



