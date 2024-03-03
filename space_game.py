#this module handles overall gameloop, as well as input
     
import pygame
import random
import sys
import math

import config
import mobs_module
import player_module
import draw_module
import phys_module
import inven_module
import weapons_module
import items 
    
clock = pygame.time.Clock()
frame_rate = 60

#starter inventory
inven_module.create_item(0,0,1000,99)
inven_module.create_item(1,0,1001,999)
inven_module.create_item(2,0,1002,999)
#inven_module.inventory.grid[3, 0, 0] = "m_rlauncher"
inven_module.inventory.grid[3, 0, 0] = 2000
inven_module.inventory.grid[4, 0, 0] = 2001
""" inven_module.inventory.grid[5, 0, 0] = 2002
inven_module.inventory.grid[6, 0, 0] = 2003"""
inven_module.inventory.grid[7, 0, 0] = 2004 
inven_module.inventory.grid[8, 0, 0] = 2005
inven_module.inventory.update_hotbar()


def run_game():
    running = True
    while running:
        if config.pause == False:      
            #physics forces
            phys_module.gravity()
            phys_module.apply_drag_and_friction()

            #events
            events()
            key_holds()
            phys_module.mob_movement()
            
            #position update
            phys_module.update_pos()

            #collisions
            phys_module.collisions()         
            #phys_module.projectile_collisions()
            phys_module.call_p_collisions()

            #cooldowns
            degrade_cooldowns()

            #draw
            config.time_in_ms(draw_module.draw)

        else:
            paused_events()
            #draw
            config.time_in_ms(draw_module.draw)

        clock.tick(frame_rate)

#dev   
def random_colour():
    return random.randint(0,255),random.randint(0,255),random.randint(0,255) 

def calculate_mouse_angle():    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = (mouse_x - config.camera_x)  
    dy = (mouse_y - config.camera_y) 
    if dx == 0:   
        if dy > 0:
            angle = math.pi / 2  
        elif dy < 0:
            angle = -math.pi / 2  
        else:
            angle = 0
    else:
        angle = math.atan(dy/dx)
        if mouse_x < config.camera_x:
            angle = math.pi + angle
    return angle

def mouse_true_coords():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    true_x = mouse_x - config.camera_x + player_module.player.x
    true_y = mouse_y - config.camera_y + player_module.player.y

    true_x = phys_module.teleport_to_wrapped_x(true_x)
 
    return true_x, true_y


def exit():
    pygame.quit() 
    sys.exit()

def degrade_cooldowns():
    #if is weapon
    for x in range(config.inventory_length):
        for y in range(config.inventory_height):
            if str(inven_module.inventory.grid[x, y, 0])[0] == '2':
                degrade_cooldown(weapons_module.weapon_ids[inven_module.inventory.grid[x, y, 0]])

    """ for mob in mobs_module.moblist:
        degrade_cooldown(mob) """

    clock_update()

    player_module.player.jetpack_cooldown()

def clock_update():
    config.clock += 1

def degrade_cooldown(object):
    if object.cooldown < object.max_cooldown:
        object.cooldown -= 1
    if object.cooldown <= -1:
        object.cooldown = object.max_cooldown 

def paused_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                exit()
            if event.key == pygame.K_ESCAPE:
                config.pause = 0

            inven_module.inventory_events(event.key)

        inven_module.inventory_dragging(event.type)

        return

def events(): 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                exit()
    
            if event.key == pygame.K_ESCAPE:
                config.pause = 1

            if event.key == pygame.K_i:
                x,y = mouse_true_coords()
                mobs_module.create_mob("slender", x, y)

            if event.key == pygame.K_o:
                x,y = mouse_true_coords()
                mobs_module.create_mob("bomber", x, y)

            inven_module.inventory_events(event.key)

        return


def key_holds():
#events
    keys = pygame.key.get_pressed()

    #if player_module.player.grounded: 
    #ground movement
    if keys[pygame.K_w]:
        if player_module.player.grounded:
            player_module.player.y_vel = -10
    if keys[pygame.K_s]:
        player_module.player.y_vel += 0.5
    if keys[pygame.K_a]:
        player_module.player.x_vel -= 0.5
    if keys[pygame.K_d]:
        player_module.player.x_vel += 0.5
        
    #else:
    if keys[pygame.K_SPACE]:
        player_module.player.use_jetpack(calculate_mouse_angle())

    #zoom
    if keys[pygame.K_z]:
        if config.zoom < 1:
            config.zoom += 0.05
            apply_zoom()
    if keys[pygame.K_x]:
        if config.zoom > config.max_zoom_out:
            config.zoom -= 0.05
            apply_zoom()
    if keys[pygame.K_r]:
        player_module.player.reset()

    #item use
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        inven_module.inventory.use_item()

def variable_change(keys):
    if keys[pygame.K_c]:
        config.variable += 0.05
    if keys[pygame.K_v]:
        config.variable -= 0.05

def apply_zoom():
    config.screen_width = config.og_width * config.zoom
    config.camera_x = config.screen_width//2
    config.screen_height = config.og_height * config.zoom
    config.camera_y = config.screen_height//2

run_game()
pygame.quit() 