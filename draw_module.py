import config
import weapons_module

import mobs_module
import chunks
import player_module

import phys_module
import inven_module
import items
import math

import time

#pygame
import pygame

shadow_surf = pygame.Surface((config.screen_width//config.max_zoom_out, config.screen_height//config.max_zoom_out), pygame.SRCALPHA)

#maybe draw shadow chunk and remove viewcone, to see bg
crop_surf = pygame.Surface((config.screen_width//config.max_zoom_out, config.screen_height//config.max_zoom_out), pygame.SRCALPHA) #draw mobs and real surf (cropped if not in viewcone)
screen = pygame.Surface((config.screen_width//config.max_zoom_out, config.screen_height//config.max_zoom_out), pygame.SRCALPHA) #last 2 blitted here, then show player and proj
final_screen = pygame.display.set_mode((config.screen_width, config.screen_height), pygame.FULLSCREEN)

#todo
#curvature.
#first add draw mouse.
#draw mouse is blitted to screen, whole screen is wrapped with the curvature map

bg_sprites = {
    "day": pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/bg/grad1.png").convert(),
    "night": pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/bg/grad2.png").convert()
}

def draw_bg():
    #background
    screen.fill(get_sky_colour(player_module.player))
    screen.fill(get_sky_colour(player_module.player))
    bg_sprites["night"].set_alpha(100 - player_module.player.y//10)
    screen.blit(bg_sprites["night"], (0, 0))


chunk_shadow = pygame.Surface((config.chunk_size, config.chunk_size), pygame.SRCALPHA)
chunk_shadow.fill((0,0,0))
chunk_shadow.set_alpha(100)
def draw_chunks(chunk_list):
    rect = pygame.Rect(0, 0, config.chunk_size, config.chunk_size)

    player_chunk_x, player_chunk_y = chunks.get_chunk_coords(int(player_module.player.x), int(player_module.player.y) + config.block_size)
    x_min, x_max, y_min, y_max = chunks.chunk_draw_range(player_chunk_x, player_chunk_y)
    for x in range(x_min, x_max + 1):

        for y in range(int(y_min), int(y_max) + 1):
            if y > -1 and y < config.world_height:

                m = chunks.chunk_wrap(x)
                surf = chunk_list[m][y].surf
                #center corresponds to: chunk location, relative to player, plus half the screen size
                #rect.center = (config.og_width//2 + x * config.chunk_size - player_module.player.x, config.og_height//2 * + y * config.chunk_size - player_module.player.y)
                rect.center = ((config.og_width//2)//config.max_zoom_out + x  * config.chunk_size - player_module.player.x, (config.og_height//2)//config.max_zoom_out + y  * config.chunk_size - player_module.player.y)
                
                screen.blit(surf, rect)
                shadow_surf.blit(chunk_list[m][y].shadow_surf, rect)

                text = config.font.render(str(x), True, (255, 255, 255))
                screen.blit(text, rect.center)


#fix for wrap
def is_on_screen(x,y, player, entity):
    half_entity_width = entity.rect.width//2
    half_entity_height = entity.rect.width//2

    dist = config.draw_distance * config.chunk_size

    if player.x - dist - config.camera_x < x < player.x + dist + config.camera_x and config.player.y - dist - config.camera_y < y < player.y + dist + config.camera_y:
        return 1
    else: 
        return 0


def get_sky_colour(player):
    BABY_BLUE = (100, 200, 255)

    value = player.y/600
    if value < 0:
        value = 0
    if value > 1:
        value = 1

    sky_colour = tuple(element * value for element in BABY_BLUE)
    return sky_colour

#wraps object coordinates when drawing
def calculate_draw_center(object):
    #draw_wrapping
    if player_module.player.x > config.max_x - config.draw_distance * config.chunk_size and object.x < (config.draw_distance - 1/2) * config.chunk_size:
        offset = config.max_x - player_module.player.x + object.x + config.half_chunk_size
        object_draw_x = config.og_width//2 + offset
        return object_draw_x, config.og_height//2 + object.y - player_module.player.y

    elif player_module.player.x < (config.draw_distance - 1/2) * config.chunk_size and object.x >config. max_x - config.draw_distance * config.chunk_size: 
        offset = object.x - config.max_x - player_module.player.x - config.half_chunk_size
        object_draw_x = config.og_width//2 + offset
        return object_draw_x, config.og_height//2 + object.y - player_module.player.y
    
    else: 
        return config.og_width//2 + object.x - player_module.player.x, config.og_height//2 + object.y - player_module.player.y


def draw_mobs(moblist):
    for mob in moblist:
        x, y, = calculate_draw_center(mob)
        #if is_on_screen(x,y, mob):
        mob.rect.center = (x,y)
        mob.draw(crop_surf)


def draw_projectiles():
    for entity in weapons_module.projectiles:     
        entity.rotate_surf()
        x, y = calculate_draw_center(entity)
        entity.rect.center = (x,y)
        entity.draw(screen)


def draw_player():
    player_module.player.rect.center = ((config.og_width//2)//config.max_zoom_out, (config.og_height//2)//config.max_zoom_out)
    screen.blit(player_module.player.surf, player_module.player.rect)

def render_text(text_name, text, y):
    text_surface = config.font.render(text_name + ": " + str(text), True, config.WHITE)
    final_screen.blit(text_surface, (50, y)) 

def draw_inventory():
    inven_module.inventory.update_inventory()
    inven_module.inventory.draw_inventory(final_screen)

def draw_weapon(weapon):
    weapon.surf = pygame.transform.rotate(weapon.sprite, int(math.degrees(-inven_module.calculate_mouse_angle())))
    weapon.rect = weapon.surf.get_rect()
    weapon.rect.center = (config.og_width//2, config.og_height//2 - config.block_size//2)
    screen.blit(weapon.surf, weapon.rect)   

def mouse_true_coords():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    true_x = mouse_x - config.camera_x + player_module.player.x
    true_y = mouse_y - config.camera_y + player_module.player.y

    true_x = phys_module.teleport_to_wrapped_x(true_x)
 
    return true_x, true_y


import numpy as np
length = math.hypot(config.screen_width//2, config.screen_height//2)
shadow_polygon = np.array([[-length, -length], [-length, length], [length, length], [0,0], [length, -length]])
vision_polygon = np.array([[length, length], [0,0], [length, -length]])

origin = np.array([config.screen_width//2, config.screen_height//2 - config.block_size//2])

def rect_vision():

    angle_rad = inven_module.calculate_mouse_angle() 
    rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                [np.sin(angle_rad), np.cos(angle_rad)]])
    new_shadow_polygon = np.dot(shadow_polygon, rotation_matrix.T)
    new_shadow_polygon = new_shadow_polygon + origin

    new_vision_polygon = np.dot(vision_polygon, rotation_matrix.T)
    new_vision_polygon = new_vision_polygon + origin

    pygame.draw.polygon(crop_surf, (0,0,0,0), new_shadow_polygon)

    shadow_surf.fill((0,0,0,50))
    pygame.draw.polygon(shadow_surf, (0,0,0,0), new_vision_polygon)


def draw():

    draw_bg()
    config.time_in_ms(draw_chunks, chunks.chunk_list)
    config.time_in_ms(draw_mobs, mobs_module.moblist)

    rect_vision()
    screen.blit(shadow_surf, (0,0))
    screen.blit(crop_surf, (0,0))
    shadow_surf.fill((0,0,0,0))
    crop_surf.fill((0,0,0,0))

    config.time_in_ms(draw_player)
    config.time_in_ms(draw_projectiles)
    """ screen.fill(get_sky_colour(player_module.player))
    draw_chunks(chunks.chunk_list)
    draw_mobs(mobs.moblist)
    draw_player()
    draw_projectiles()  """

    if str(inven_module.inventory.grid[inven_module.inventory.selected_x, inven_module.inventory.selected_y, 0])[0] == '2':
        draw_weapon(weapons_module.weapon_ids[inven_module.inventory.grid[inven_module.inventory.selected_x, inven_module.inventory.selected_y, 0]])

    scaled_screen = pygame.transform.scale(screen, (int(config.og_width * config.zoom)//config.max_zoom_out, int(config.og_height * config.zoom)//config.max_zoom_out))
    scaled_rect = scaled_screen.get_rect()
    scaled_rect.center = (config.og_width//2, config.og_height//2)

    final_screen.blit(scaled_screen, scaled_rect)

    inven_module.inventory.draw_hotbar(final_screen)
    if config.pause:
        draw_inventory()


    start = time.time()
    render_text("x_true", player_module.player.x, 0)
    render_text("y_true", player_module.player.y, 50)
    render_text("x_vel", player_module.player.x_vel, 100)
    render_text("y_vel", player_module.player.y_vel, 150)
    #render_text("num rockets", len(weapons.projectiles), 200)
    #render_text("num mobs", len(mobs.moblist), 250)
    #render_text("health", player_module.player.health, 300)
    #render_text("grounded", player_module.player.grounded, 350)
    #render_text("hotbar selected", inven_module.inventory.selected_x, 400)
    mouse_x, mouse_y = mouse_true_coords()
    render_text("tru mouse_x", mouse_x, 200)
    render_text("tru mouse_y", mouse_x, 250)    
    chunk_x, chunk_y, block_x, block_y = chunks.true_to_block_coords(mouse_x, mouse_y)
    render_text("block mouse_y", block_y, 300)
    render_text("block chunk_y", chunk_y, 350)
    render_text("jetpack_percent", player_module.player.jetpack_percent, 400)

    if str(inven_module.inventory.grid[inven_module.inventory.selected_x, 0, 0])[0] == '2':
        render_text("weapon cooldown", weapons_module.weapon_ids[inven_module.inventory.grid[inven_module.inventory.selected_x, 0, 0]].cooldown, 450)

    render_text("inventory slot", inven_module.get_moused_inventory_slot(), 500)

    pygame.display.flip()


