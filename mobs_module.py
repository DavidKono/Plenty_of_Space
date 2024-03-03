import pygame
import config
import numpy as np
import mobs_stats
import config
import player_module

moblist = []

class mob_class():
    def __init__(self, x, y, width, height, num_frames, attack_cooldown, melee_damage, max_health, visual_damage, ai):

        self.x = x
        self.y = y

        self.x_vel = 0
        self.y_vel = 0

        self.width = width
        self.height = height

        self.num_frames = num_frames

        self.grounded = 0

        self.current_frame = 0
        self.last_clock = config.clock

        self.attack_cooldown = attack_cooldown
        self.attack_clock = config.clock
        self.melee_damage = melee_damage

        self.max_health = max_health
        self.health = max_health
        self.visual_damage = visual_damage

        self.ai = ai

        self.rect = pygame.Rect(0, 0, self.width * config.block_size, self.height * config.block_size)
        self.surf = pygame.Surface((self.width * config.block_size, self.height * config.block_size))

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        show_health(self, screen)

    def check_attack_cooldown(self):
        if config.clock - self.attack_clock > self.attack_cooldown:
            self.last_clock = config.clock
            return True
        
    def death(self):
        moblist.remove(self)

def damage_and_death(entity, damage):
    entity.health -= damage
    if entity.health < 1:
        entity.death()
    """ if entity.visual_damage:
        entity.mob_destruction(damage) """

def show_health(self, screen):
    text_surface = config.font.render(str(self.health), True, config.WHITE)
    screen.blit(text_surface, (self.rect.topleft[0], self.rect.center[1] - (self.width+1) * config.block_size))

def create_mob(mob_type, x, y):
    if mob_type == "slender": moblist.append(mob_class(*mobs_stats.slender(x,y)))
    if mob_type == "bomber" : moblist.append(mob_class(*mobs_stats.bomber(x,y)))
