import pygame
import config
import weapons_module
import math

class player_class():
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.x_vel = 0
        self.y_vel = 0

        self.max_x_vel = 20               
        self.max_y_vel = 20

        self.width = 2
        self.height = 4

        self.surf = pygame.Surface((self.width * config.block_size, self.height * config.block_size))  
        self.surf.fill(config.WHITE)
        self.rect = pygame.Rect(0, 0, self.width * config.block_size, self.height * config.block_size)                                    

        self.grounded = 0

        self.colour = (255,255,255)

        #self.weapon = weapons_module.weapon_ids["m_rlauncher"]
        self.weapon = weapons_module.weapon_ids[2000]
        

        self.starter_health = 100
        self.health = 100
        self.visual_damage = False

        self.jetpack_percent = 100

    def death(self):
        self.reset()

    def reset(self):
        self.health = self.starter_health
        self.x = 0
        self.y = 0
        self.x_vel = 0
        self.y_vel = 0

    def use_jetpack(self, angle):
        if self.jetpack_percent > 5:
            jetpack_speed = 1.5
            self.x_vel += jetpack_speed * math.cos(angle)
            self.y_vel += jetpack_speed * math.sin(angle)
            self.jetpack_percent -= 2
            
    def jetpack_cooldown(self):
        update_increment = 1
        if self.jetpack_percent <= 100:
            self.jetpack_percent = min(self.jetpack_percent + update_increment, 100)


player = player_class(10 * config.chunk_size, 0)