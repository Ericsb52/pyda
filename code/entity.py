from settings import *

class Entity(pg.sprite.Sprite):
    def __init__(self,groups,level):
        super(Entity, self).__init__(groups)
        self.level  = level
        self.dir = Vector2()
        self.frame_index = 0
        self.animation_speed = animation_speed


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
