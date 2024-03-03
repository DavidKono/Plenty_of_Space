import numpy as np
import config
import pygame
import chunks
import player_module
import items
import weapons_module
import math

box_size = 50
hotbar_length = config.inventory_length * box_size
inventory_pixel_height = config.inventory_height * box_size 

class Inventory_class:
    def __init__(self):
        self.grid = np.full((config.inventory_length, config.inventory_height, 2), 0, dtype=np.uint16)

        self.selected_x = 0
        self.selected_y = 0
        self.is_weapon = True

        self.blank_hotbar = pygame.Surface((hotbar_length, box_size), pygame.SRCALPHA)
        self.blank_hotbar.fill((*config.GREY, 179))
        self.hotbar_surf = self.blank_hotbar
        self.hotbar_rect = pygame.Rect(0, 0, hotbar_length, box_size)
        self.hotbar_rect.center = (config.og_width//2, config.og_height - 40)

        self.highlight = pygame.Surface((box_size, box_size), pygame.SRCALPHA)
        self.highlight.fill((*config.WHITE, 179))

        self.inventory_surf = pygame.Surface((hotbar_length, inventory_pixel_height), pygame.SRCALPHA)
        self.blank_inventory = pygame.Surface((hotbar_length, inventory_pixel_height), pygame.SRCALPHA)
        self.blank_inventory.fill((*config.GREY, 179))
        self.inventory_rect = pygame.Rect(0, 0, hotbar_length, inventory_pixel_height)
        self.inventory_rect.center = (config.og_width//2, config.og_height//2)
        self.inventory_surf.blit(self.blank_inventory, (0,0))


        self.is_dragging_item = False
        self.dragged_item_x = 0
        self.dragged_item_y = 0
    
    
    def draw_hotbar(self, screen):
        screen.blit(self.hotbar_surf, self.hotbar_rect)

    def update_hotbar(self):
        self.hotbar_surf.fill((0,0,0,0))
        self.hotbar_surf = self.blank_hotbar

        self.highlight_rect = self.highlight.get_rect(center=(self.selected_x * box_size + box_size//2, box_size//2))
        self.hotbar_surf.blit(self.highlight, self.highlight_rect)

        for x in range(config.inventory_length):
            id_text = str(self.grid[x, self.selected_y, 0])
            id_text_surface = config.smolfont.render(id_text, True, (255, 255, 255))

            text_rect = id_text_surface.get_rect(center=(x * box_size + box_size//2, box_size//2))
            self.hotbar_surf.blit(id_text_surface, text_rect) 

            count_text = str(self.grid[x, self.selected_y, 1])
            count_text_surface = config.smollerfont.render(count_text, True, (255, 255, 255))

            text_rect = count_text_surface.get_rect(center=(x * box_size + 3*box_size//4, 3*box_size//4))
            self.hotbar_surf.blit(count_text_surface, text_rect) 



    def draw_inventory(self, screen):
        screen.blit(self.inventory_surf, self.inventory_rect)

    def update_inventory(self):
        self.inventory_surf.fill((0,0,0,0))
        self.inventory_surf.blit(self.blank_inventory, (0,0))

        self.highlight_rect = self.highlight.get_rect(center=(self.selected_x * box_size + box_size//2, self.selected_y * box_size + box_size//2))
        self.inventory_surf.blit(self.highlight, self.highlight_rect)

        for y in range(config.inventory_height):
            for x in range(config.inventory_length):

                id_text = str(self.grid[x, y, 0])
                id_text_surface = config.smolfont.render(id_text, True, (255, 255, 255))

                text_rect = id_text_surface.get_rect(center=(x * box_size + box_size//2, y * box_size + box_size//2))
                self.inventory_surf.blit(id_text_surface, text_rect)  


                count_text = str(self.grid[x, y, 1])
                count_text_surface = config.smollerfont.render(count_text, True, (255, 255, 255))

                text_rect = count_text_surface.get_rect(center=(x * box_size + 3*box_size//4, y * box_size + 3*box_size//4))
                self.inventory_surf.blit(count_text_surface, text_rect)  


    def use_item(self):
        #if player has item in hotbar selected, use corresponding thing
        #eg weapon, fire, corresponding ammo goes down
        #block, place, item count goes down
        #consumable, use, item count goes down 
        first_digit = str(self.grid[self.selected_x, self.selected_y, 0])[0]
        if first_digit == "1":
            dev_create_block(self)
        elif first_digit == "2":
            fire_weapon(self)
        else:
            return  

inventory = Inventory_class()   

def create_item(x, y, item_name, count):
    inventory.grid[[x, x], [y, y], [0, 1]] = [item_name, count]


#use functions
def dev_create_block(self):
    mouse_x, mouse_y = chunks.mouse_true_coords()
    chunk_x, chunk_y, block_x, block_y = chunks.true_to_block_coords(mouse_x,mouse_y)

    #if drawing void
    if self.grid[self.selected_x, self.selected_y, 0] == 1000:
        if chunk_y < config.world_height:
            chunks.chunk_list[int(chunk_x)][int(chunk_y)].create_block(block_x,block_y, self.grid[self.selected_x, self.selected_y, 0]) 

    #normal drawing
    elif chunks.chunk_list[int(chunk_x)][int(chunk_y)].block_is_solid(int(block_x),int(block_y)) == False:
        if chunk_y < config.world_height:
            chunks.chunk_list[int(chunk_x)][int(chunk_y)].create_block(block_x,block_y, self.grid[self.selected_x, self.selected_y, 0]) 

            #remove 1 block and nullify if zero 
            self.grid[self.selected_x, self.selected_y, 1] -= 1
            if self.grid[self.selected_x, self.selected_y, 1] < 1:
                self.grid[self.selected_x, self.selected_y, 0] = 0

            self.update_hotbar()
            

def fire_weapon(self):
    angle = calculate_mouse_angle()
    weapons_module.weapon_ids[self.grid[self.selected_x, 0, 0]].fire(angle, player_module.player)
    weapons_module.weapon_ids[self.grid[self.selected_x, 0, 0]].cooldown -= 1
    return


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


#control hotbar and inventory
def inventory_events(event):
    if event == pygame.K_1:
        inventory.selected_x = 0
        inventory.update_hotbar()
    if event == pygame.K_2:
        inventory.selected_x = 1
        inventory.update_hotbar()
    if event == pygame.K_3:
        inventory.selected_x = 2
        inventory.update_hotbar()
    if event == pygame.K_4:
        inventory.selected_x = 3
        inventory.update_hotbar()
    if event == pygame.K_5:
        inventory.selected_x = 4
        inventory.update_hotbar()
    if event == pygame.K_6:
        inventory.selected_x = 5
        inventory.update_hotbar()
    if event == pygame.K_7:
        inventory.selected_x = 6
        inventory.update_hotbar()
    if event == pygame.K_8:
        inventory.selected_x = 7
        inventory.update_hotbar()
    if event == pygame.K_9:
        inventory.selected_x = 8
        inventory.update_hotbar()
    if event == pygame.K_0:
        inventory.selected_x = 9
        inventory.update_hotbar()

    if event == pygame.K_DOWN:
        move_hotbar(0, 1)
    if event == pygame.K_UP:
        move_hotbar(0, -1)
    if event == pygame.K_RIGHT:
        move_hotbar(1, 0)
    if event == pygame.K_LEFT:
        move_hotbar(-1, 0)


def inventory_dragging(event_type):
    if inventory.is_dragging_item == False:
        if event_type == pygame.MOUSEBUTTONDOWN:
            print("mouse down")
            inventory.is_dragging_item = True
            inventory.dragged_item_x, inventory.dragged_item_y = get_moused_inventory_slot()
            print(inventory.dragged_item_x, inventory.dragged_item_y)

    elif inventory.is_dragging_item == True:
        if event_type == pygame.MOUSEBUTTONUP:
            print("mouse up")
            inventory.is_dragging_item = False

            new_x, new_y = get_moused_inventory_slot()
            temp0 = inventory.grid[new_x, new_y, 0]
            temp1 = inventory.grid[new_x, new_y, 1]

            inventory.grid[new_x, new_y, 0] = inventory.grid[inventory.dragged_item_x, inventory.dragged_item_y, 0]
            inventory.grid[new_x, new_y, 1] = inventory.grid[inventory.dragged_item_x, inventory.dragged_item_y, 1]

            inventory.grid[inventory.dragged_item_x, inventory.dragged_item_y, 0] = temp0
            inventory.grid[inventory.dragged_item_x, inventory.dragged_item_y, 1] = temp1


    inventory.update_hotbar()
    return

#handles inventory wrapping
def move_hotbar(dx, dy):
    inventory.selected_x += dx
    inventory.selected_y += dy

    inventory.selected_x %= config.inventory_length
    inventory.selected_y %= config.inventory_height

    inventory.update_hotbar()


def get_moused_inventory_slot():
    mouse_x, mouse_y = pygame.mouse.get_pos()

    x = (mouse_x - config.camera_x + hotbar_length//2)//box_size
    y = (mouse_y - config.camera_y + inventory_pixel_height//2)//box_size

    return x, y

#def inventory_dragging():

