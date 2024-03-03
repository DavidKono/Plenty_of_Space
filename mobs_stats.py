import pygame
import config
import player_module
import phys_module
import math

#functions type

#only 1 ai used at a time, spritesheet and draw used based on current ai. will do for each mob (reuse detection)
""" 
def detection_ai():
    #idle animation
    #sets search node (at block)

def movement_ai():
    #running, jumping, falling animation
    #heads towards search node

def attack_ai():
    #attack animation
    #attacks if it can

def damaged_ai():
    #taking damage animation 

def ai(mob): """

def convert_sprite_to_frames(sprite, num_frames):
    width = sprite.get_width()//num_frames
    height = sprite.get_height()
    frames = []
    for i in range(num_frames):
        frames.append(sprite.subsurface(pygame.Rect(i * width, 0, width, height)))
    return frames

def convert_sprite_to_flipped_frames(sprite, num_frames):
    width = sprite.get_width()//num_frames
    height = sprite.get_height()
    frames = []
    for i in range(num_frames):
        frames.append(pygame.transform.flip(sprite.subsurface(pygame.Rect(i * width, 0, width, height)), True, False))
    return frames
        
mob_sprites = {
    "slender_idle" : convert_sprite_to_frames(pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/enemies/slender_idle_big.png"), 2),
    "slender_run" : convert_sprite_to_frames(pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/enemies/slender_run_big.png"), 2),
    "slender_flipped_run" : convert_sprite_to_flipped_frames(pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/enemies/slender_run_big.png"), 2),
    "bomber_running" : convert_sprite_to_frames(pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/enemies/bomb_fella.png"), 4),
    "bomber_running_flipped" : convert_sprite_to_flipped_frames(pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/enemies/bomb_fella.png"), 4)
}

def slender_ai(mob, player):
    #stay still till damaged
    current_frame =  get_current_frame(mob)

    if mob.health == mob.max_health:
        mob.surf = mob_sprites["slender_idle"][current_frame]

        """ mob.surf = pygame.Surface((mob.width * config.block_size, mob.height * config.block_size))
        mob.surf.fill((0,0,0)) """
    else:
        if mob.x > 0 & player.x < 0:
            mob.x_vel = -3
            mob.surf = mob_sprites["slender_flipped_run"][current_frame]
        else:
            if mob.x < player.x:
                mob.x_vel = 3
                mob.surf = mob_sprites["slender_run"][current_frame]
            elif mob.x > player.x:
                mob.x_vel = -3
                mob.surf = mob_sprites["slender_flipped_run"][current_frame]

def bomber_ai(mob, player):
    #stay still till damaged
    current_frame = get_current_frame(mob)

    if mob.health < 100 or math.hypot(mob.x - player.x, mob.y - player.y) < 40:
        phys_module.explode_enemy(mob, 20, 2)
        mob.death()

    if mob.x > 0 & player.x < 0:
        mob.x_vel = -3
        mob.surf = mob_sprites["bomber_running_flipped"][current_frame]
    else:
        if mob.x < player.x:
            mob.x_vel = 3
            mob.surf = mob_sprites["bomber_running"][current_frame]
        elif mob.x > player.x:
            mob.x_vel = -3
            mob.surf = mob_sprites["bomber_running_flipped"][current_frame]
          
def get_current_frame(mob):
    if config.clock - mob.last_clock > 30:
        mob.last_clock = config.clock
        mob.current_frame += 1
        if mob.current_frame == mob.num_frames:
            mob.current_frame = 0
    return mob.current_frame
    
def slender(x,y):
    width = 4
    height = 8

    num_frames = 2

    attack_cooldown = 20

    melee_damage = 10
    max_health = 200

    visual_damage = True
    
    ai = slender_ai

    return x, y, width, height, num_frames, attack_cooldown, melee_damage, max_health, visual_damage, ai

def bomber(x,y):
    width = 2
    height = 2

    num_frames = 4

    attack_cooldown = 20

    melee_damage = 10
    max_health = 200

    visual_damage = True
    
    ai = bomber_ai

    return x, y, width, height, num_frames, attack_cooldown, melee_damage, max_health, visual_damage, ai
    