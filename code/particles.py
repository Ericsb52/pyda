import random

from settings import *
from support import*

class AnimationPlayer():
    def __init__(self,level):
        self.level = level
        self.frames = {
            # magic
            "flames":import_folder(flames_path),
            "aura": import_folder(aura_path),
            "heal": import_folder(heal_path),

            # attacks
            "claw":import_folder(claw_path),
            "slash": import_folder(slash_path),
            "sparkle": import_folder(sparkle_path),
            "leaf_attack": import_folder(leaf_attack_path),
            "thunder": import_folder(thunder_path),

            # monster deaths
            "squid": import_folder(squid_path),
            "raccoon": import_folder(raccoon_path),
            "spirit": import_folder(spirit_path),
            "bamboo": import_folder(bamboo_path),

            # leafs
            "leaf": (import_folder(leaf_path1),
                     import_folder(leaf_path2),
                     import_folder(leaf_path3),
                     import_folder(leaf_path4),
                     import_folder(leaf_path5),
                     import_folder(leaf_path6),
                     self.reflect_images(import_folder(leaf_path1)),
                     self.reflect_images(import_folder(leaf_path2)),
                     self.reflect_images(import_folder(leaf_path3)),
                     self.reflect_images(import_folder(leaf_path4)),
                     self.reflect_images(import_folder(leaf_path5)),
                     self.reflect_images(import_folder(leaf_path6))
                     )
        }
    def create_grass_particles(self,pos,groups):
        animation_frames = random.choice(self.frames["leaf"])
        ParticleEfect(self.level,pos,animation_frames,groups)

    def create_particles(self,attk_type,pos,groups):
        animation_frames = self.frames[attk_type]
        ParticleEfect(self.level,pos,animation_frames,groups,attk_type)

    def reflect_images(self,frames):
        new_frame = []
        for frame in frames:
            fipped_frame = pg.transform.flip(frame,True,False)
            new_frame.append(fipped_frame)
        return new_frame

class ParticleEfect(pg.sprite.Sprite):
    def __init__(self,level,pos,animation_frames, groups, type = None):
        super().__init__(groups)
        self.type = "magic"
        self.level = level
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image =  self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
