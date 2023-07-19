import pygame as pg
import sys
from debug import debug
from pygame.math import Vector2
import random

# game setup
WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 64
title = "The Legend of Pyda"
icon_path = "../graphics/player/down/down_0.png"

# Gen Colors
water_color = "#71ddee"
ui_bg_color = "#222222"
ui_border_color = "#111111"
text_color = "#EEEEEE"
# ui colors
health_color = "red"
energy_color = "yellow"
ui_border_color_active = "gold"

# tile settings
# grass tile
hibox_x_offset_grass = -25
hibox_y_offset_grass = -25
# object tile
hibox_x_offset_obj = -25
hibox_y_offset_obj = -80

grass_path = "../graphics/Grass"
obj_path = "../graphics/objects"
floor_img_path = "../graphics/tilemap/ground.png"
# layout paths
layout_boundary_path = "../map/map_FloorBlocks.csv"
layout_grass_path = "../map/map_Grass.csv"
layout_object_path = "../map/map_LargeObjects.csv"
layout_entity_path = "../map/map_Entities.csv"

#  UI settings
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 180
ITEM_BOX_SIZE = 80
UI_FONT = "../graphics/font/joystix.ttf"
UI_FONT_SIZE = 18



# player settings
player_speed = 5
attk_cooldown = 500
animation_speed = 0.15
animation_path = "../graphics/player"
hibox_x_offset = -10
hibox_y_offset = -20

# weapon settings
weapon_data = {
    "sword":{"cooldown":100,"damage":15,"graphic":"../graphics/weapons/sword/full.png"},
    "lance":{"cooldown":400,"damage":30,"graphic":"../graphics/weapons/lance/full.png"},
    "axe":{"cooldown":300,"damage":20,"graphic":"../graphics/weapons/axe/full.png"},
    "rapier":{"cooldown":50,"damage":8,"graphic":"../graphics/weapons/rapier/full.png"},
    "sai":{"cooldown":80,"damage":10,"graphic":"../graphics/weapons/sai/full.png"}

}

magic_data = {
    "flame":{"strength":5,"cost":20,"graphic":"../graphics/particles/flame/fire.png"},
    "heal":{"strength":20,"cost":10,"graphic":"../graphics/particles/heal/heal.png"}
}

# Enemy settings
monster_data = {
    "squid":{"health":100,"exp":100,"damage":20,"attack_type":"slash","attack_snd":"../audio/attack/slash.wave","speed":3,"resistance":3,"attack_radius":80,"notice_radius":360,"attack_cooldown":1000},
    "raccoon":{"health":300,"exp":250,"damage":40,"attack_type":"claw","attack_snd":"../audio/attack/claw.wave","speed":2,"resistance":3,"attack_radius":120,"notice_radius":400,"attack_cooldown":1000},
    "spirit":{"health":100,"exp":110,"damage":8,"attack_type":"thunder","attack_snd":"../audio/attack/fireball.wave","speed":4,"resistance":3,"attack_radius":60,"notice_radius":350,"attack_cooldown":1000},
    "bamboo":{"health":70,"exp":120,"damage":6,"attack_type":"leaf_attack","attack_snd":"../audio/attack/slash.wave","speed":3,"resistance":3,"attack_radius":50,"notice_radius":300,"attack_cooldown":1000}
}












