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
        self.stats = {"health":100,"energy":60,"attack":10,"magic":10,"speed":player_speed}
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

    def take_damage(self,ammount,type):
        if self.vulnerable:
            self.health -= ammount
            self.vulnerable = False
            self.hit_time = pg.time.get_ticks()
            self.level.animation_player.create_particles(type,self.rect.center,[self.level.all_sprites])
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
        self.energy_recovery()
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

    def get_magic_dmg(self):
        base_dmg = self.stats["magic"]
        weapon_dmg = magic_data[self.magic]["strength"]
        return base_dmg + weapon_dmg

    def create_magic(self,style,strength,cost):
        if style == "heal":
            self.heal(strength,cost)

        if style == "flame":
            self.cast_flames(strength,cost)

    def energy_recovery(self):
        if self.energy < self.stats["energy"]:
            self.energy += regen_rate*self.stats["magic"]
        else:
            self.energy = self.stats["energy"]
    def cast_flames(self,strength,cost):
        if self.energy >= cost:
            self.energy -= cost
            # play flame sound
            if "right" in self.status:
                direction = Vector2(1, 0)
            elif "left" in self.status:
                direction = Vector2(-1, 0)
            elif "up" in self.status:
                direction = Vector2(0, -1)
            elif "down" in self.status:
                direction = Vector2(0, 1)
            for i in range(1, 6):
                if direction.x:  # horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x = self.rect.centerx + offset_x + random.randint(-TILESIZE // 3, TILESIZE // 3)
                    y = self.rect.centery + random.randint(-TILESIZE // 3, TILESIZE // 3)
                    self.level.animation_player.create_particles("flames", (x, y),
                                                                 [self.level.all_sprites, self.level.weapon_sprites])
                else:  # vertical
                    offset_y = (direction.y * i) * TILESIZE
                    x = self.rect.centerx + random.randint(-TILESIZE // 3, TILESIZE // 3)
                    y = self.rect.centery + offset_y + random.randint(-TILESIZE // 3, TILESIZE // 3)
                    self.level.animation_player.create_particles("flames", (x, y),
                                                                 [self.level.all_sprites, self.level.weapon_sprites])

    def heal(self,amount,cost):
        if self.health < self.stats["health"]:
            if self.energy >= cost:
                self.energy -= cost
                self.health += amount
                self.level.animation_player.create_particles("aura", self.rect.center, [self.level.all_sprites])
                self.level.animation_player.create_particles("heal", self.rect.center + Vector2(0, -60),
                                                             [self.level.all_sprites])
                # play heal sound
                if self.health >= self.stats["health"]:
                    self.health = self.stats["health"]
                if self.energy < 0:
                    self.energy = 0

            else:
                pass
                #play error sound
        else:
            pass
            # play error sound

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



