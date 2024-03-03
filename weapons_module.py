import pygame
import math
import config
import items
#import weapons_stats

projectiles = []

class weapons_class():
    def __init__(self, id, weapon_sprite, reload_time, initial_vel, proj_gravity, proj_destructiveness, proj_piercing, damage, bullet_type, max_range):

        self.id = id
        self.sprite = weapon_sprite
        self.surf = self.sprite
        self.rect = self.surf.get_rect()

        self.max_cooldown = reload_time
        self.cooldown = reload_time
        self.initial_vel = initial_vel
        self.gravity = proj_gravity

        self.piercing = proj_piercing
        self.destructiveness = proj_destructiveness
        self.damage = damage

        self.bullet_type = bullet_type

        self.max_range = max_range  
        self.distance_travelled = 0

    def fire(self, angle, player):
        if self.cooldown == self.max_cooldown:
            projectiles.append(projectile_class(self.initial_vel, angle, player, self.bullet_type, self.id, self.piercing))
            self.cooldown -= 1


class explosives_class(weapons_class):
    def __init__(self, id, weapon_sprite, reload_time, cooldown, initial_vel, proj_gravity, proj_destructiveness, proj_piercing, damage, bullet_type, max_range, explosion_rad, kb_speed, max_splash_damage):
        super().__init__(id, weapon_sprite, reload_time, cooldown, initial_vel, proj_gravity, proj_destructiveness, proj_piercing, damage, bullet_type, max_range)
        self.rad = explosion_rad
        self.kb_speed = kb_speed
        self.max_splash_damage = max_splash_damage

class accelerating_explosives_class(explosives_class):
    def __init__(self, id, weapon_sprite, reload_time, cooldown, initial_vel, proj_gravity, proj_destructiveness, proj_piercing, damage, bullet_type, max_range, explosion_rad, kb_speed, max_splash_damage, acceleration, proj_accel_delay):
        super().__init__(id, weapon_sprite, reload_time, cooldown, initial_vel, proj_gravity, proj_destructiveness, proj_piercing, damage, bullet_type, max_range, explosion_rad, kb_speed, max_splash_damage)

        self.acceleration = acceleration
        self.proj_accel_delay = proj_accel_delay

    def accelerate(self, entity):
        if entity.accel_timer <= config.clock:

            magnitude = math.hypot(entity.x_vel + entity.y_vel)

            if magnitude != 0:
                norm_x_vel = entity.x_vel / magnitude
                norm_y_vel = entity.y_vel / magnitude

                entity.x_vel += self.acceleration * norm_x_vel
                entity.y_vel += self.acceleration * norm_y_vel

    def fire(self, angle, player):
        if self.cooldown == self.max_cooldown:
            projectiles.append(accelerating_projectile_class(self.initial_vel, angle, player, self.bullet_type, self.id, self.piercing, self.proj_accel_delay))
            self.cooldown -= 1

class lasers_class(weapons_class):
    def __init__(self, id, weapon_sprite, reload_time, cooldown, initial_vel, proj_gravity, proj_destructiveness, proj_piercing, damage, bullet_type, max_range):
        super().__init__(id, weapon_sprite, reload_time, cooldown, initial_vel, proj_gravity, proj_destructiveness, proj_piercing, damage, bullet_type, max_range)

class projectile_class():
    def __init__(self, projectile_vel, angle, player, projectile_sprite_name, parent_weapon, piercing):
        self.projectile_sprite_name = projectile_sprite_name

        self.x = player.x 
        self.y = player.y - config.block_size//2

        self.x_vel = math.cos(angle) * projectile_vel
        self.y_vel = math.sin(angle) * projectile_vel
        self.x_vel += player.x_vel
        self.y_vel += player.y_vel

        self.distance_travelled = 0

        self.parent_weapon = parent_weapon

        self.piercing = piercing

        self.rect = pygame.Rect(0, 0, 0, 0)
    
    def rotate_surf(self):
        bullet_tilt = math.degrees(calculate_angle(self.x_vel, self.y_vel))
        self.surf = pygame.transform.rotate(items.ammo_sprites[self.projectile_sprite_name], bullet_tilt)  
        self.rect = self.surf.get_rect()

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

class accelerating_projectile_class(projectile_class):
    def __init__(self, projectile_vel, angle, player, projectile_sprite_name, parent_weapon, piercing, proj_accel_delay):
        super().__init__(projectile_vel, angle, player, projectile_sprite_name, parent_weapon, piercing)
    
        self.accel_timer = config.clock + proj_accel_delay

def calculate_angle(dx, dy):
    angle = math.atan(dy/dx)
    if dx < 0:
        angle = math.pi - angle 
    if dx > 0:
        angle = -angle
    return angle

""" weapon_ids = {
    2000 : explosives_class(*weapons_stats.m_rlauncher()), #mgun rocket launcher
    2001 : explosives_class(*weapons_stats.rlauncher()), #rocket launcher
    2004 : accelerating_explosives_class(*weapons_stats.slug_launcher()),

    2005 : lasers_class(*weapons_stats.mining_laser()),
}  """

""" 2002 : weapons_class(*weapons_stats.teal_sniper()), 
    2003 : weapons_class(*weapons_stats.mgun()), 
    2004 : weapons_class(*weapons_stats.slug_launcher())  """