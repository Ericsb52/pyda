
from settings import *
from support import  *
from entity import *

class Enemy(Entity):
    def __init__(self,level,monster_type,pos,groups):
        super(Enemy, self).__init__(groups,level)
        self.sprite_type = "enemy"


        self.import_graphics(monster_type)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitBox = self.rect.inflate(-10,-10)
        self.z = ""

        # stats
        self.monster_name = monster_type
        monster_info = monster_data[self.monster_name]
        self.health = monster_info["health"]
        self.exp = monster_info["exp"]
        self.speed = monster_info["speed"]
        self.attk_dmg = monster_info["damage"]
        self.resistance = monster_info["resistance"]
        self.attk_radius = monster_info["attack_radius"]
        self.agro_radius = monster_info["notice_radius"]
        self.attk_type = monster_info["attack_type"]

        self.can_attack = True
        self.attack_time = 0
        self.attack_cooldown = monster_info["attack_cooldown"]



    def take_damage(self,type):
        if self.vulnerable:
            self.dir = self.get_move_info()[1]
            if type == "weapon":
                self.health -= self.level.player.get_weapon_dmg()
            else: # magic damage
                pass
            self.hit_time = pg.time.get_ticks()
            self.vulnerable = False
    def hit_reaction(self):
        if not self.vulnerable:
            self.dir *= -self.resistance

    def cooldown_timers(self):
        cur_time = pg.time.get_ticks()

        if not self.can_attack:
            if cur_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if cur_time - self.hit_time >= self.hit_cooldown:
                self.vulnerable = True
    def check_death(self):
        if self.health <= 0:
            self.kill()

    def import_graphics(self,name):
        self.animations = {"idle":[],"move":[],"attack":[]}
        main_path = f"../graphics/monsters/{name}/"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path+animation)

    def get_move_info(self):
        enemy_vec = Vector2(self.rect.center)
        player_vec = Vector2(self.level.player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = Vector2(0,0)
        return distance,direction

    def get_status(self):
        distance,direction = self.get_move_info()

        if distance <= self.attk_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "attack"
        elif distance <= self.agro_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self):
        if self.status == "attack":
            self.attack()

        elif self.status =="move":
            self.dir = self.get_move_info()[1]
        else:
            self.dir = Vector2()

    def attack(self):
        self.attack_time = pg.time.get_ticks()
        self.level.player.take_damage(self.attk_dmg)
        # spawn particals at players location based on attack type

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitBox.center)
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):

        self.animate()
        self.cooldown_timers()
        self.get_status()
        self.actions()
        self.hit_reaction()
        self.move(self.speed)
        self.check_death()
