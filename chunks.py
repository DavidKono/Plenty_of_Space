import random
import pygame
import numpy as np
import config
import player_module
import items
import phys_module

world_length = config.world_length
world_height = config.world_height 
block_size = config.block_size
blocks_per_chunk = config.blocks_per_chunk
screen_width = config.screen_width 
screen_height = config.screen_height
chunk_size = blocks_per_chunk * block_size


void = pygame.Surface((config.block_size, config.block_size), pygame.SRCALPHA)
void.fill((0,0,0,0))
#void

solidity_mapping = {
    1000: False,
    1001: True,
    1002: True,
    1004: True,
    1005: True,
    1006: False,
    1007: True
}

hardness_mapping = {
    1000: 0,
    1001: 1,
    1002: 1,
    1004: 2,
    1005: 3,
    1006: 3,
    1007: 3
}

health_mapping = {
    1000: 0,
    1001: 50,
    1002: 50,
    1004: 200,
    1005: 500,
    1006: 0,
    1007: 1000
}


VOID = pygame.Color(0, 0, 0, 0)
BLUE = (100, 100, 255)
BABY_BLUE = (100, 200, 255)
BROWN = (88, 57, 39)

block_shadow = pygame.Surface((config.block_size, config.block_size), pygame.SRCALPHA)
block_shadow.fill((0, 0, 0, 20))
shadow_chunk = pygame.Surface((config.chunk_size, config.chunk_size), pygame.SRCALPHA)
shadow_chunk.fill((0, 0, 0, 20))

class chunk_class():
    def __init__(self, block_number):
        self.block_number = block_number
        
        self.surf = pygame.Surface((chunk_size, chunk_size), pygame.SRCALPHA)
        self.shadow_surf = pygame.Surface((chunk_size, chunk_size), pygame.SRCALPHA)

        self.grid = np.full((blocks_per_chunk, blocks_per_chunk), block_number, dtype=np.uint16)
        self.health_grid = np.full((blocks_per_chunk, blocks_per_chunk), health_mapping[block_number], dtype=np.int16)

        self.render_grid()

    def block_is_solid(self, x, y):
        return solidity_mapping[self.grid[x,y]]
    
    def block_hardness(self, x, y):
        return hardness_mapping[self.grid[x,y]]
             
    #updates health visual or converts destroyed block to void
    def create_block(self, x,y, block_number):
        #needs to replace with void, not draw empty alpha channel on top
        if block_number == 1000:
            self.surf.fill((0, 0, 0, 0), (x * config.block_size, y * config.block_size, config.block_size, config.block_size))
            self.grid[int(x)][int(y)] = 1000  
            self.health_grid[int(x)][int(y)] = 1

            if config.shadows:
                self.shadow_surf.fill((0, 0, 0, 0), (x * config.block_size, y * config.block_size, config.block_size, config.block_size))

        else:
            self.surf.blit(items.block_sprites[block_number], (x * block_size, y * block_size))
            self.grid[int(x),int(y)] = block_number
            self.health_grid[int(x),int(y)] = health_mapping[block_number]

            if config.shadows:
                self.shadow_surf.blit(block_shadow, (x * block_size, y * block_size))

    def draw_block(self, x,y, block_number):
        self.surf.blit(items.block_sprites[block_number], (x * block_size, y * block_size))

        if block_number != 1000:
            dam_surf = items.block_sprites[0000]
            num = ((health_mapping[block_number] - self.health_grid[int(x),int(y)])/health_mapping[block_number]) * 255
            dam_surf.set_alpha(num)  

            self.surf.blit(dam_surf, (x * block_size, y * block_size))  

    def render_grid(self):
        for x in range(blocks_per_chunk):
            for y in range(blocks_per_chunk):
                self.surf.blit(items.block_sprites[self.block_number], (x * block_size, y * block_size))

        #init w shadow
        if self.block_number != 1000:
            self.shadow_surf.blit(shadow_chunk, (0,0))



#block and chunk calculations
def get_chunk_coords(x, y):
    chunk_x = (x + config.half_chunk_size) // config.chunk_size 
    chunk_y = (y + config.half_chunk_size) // config.chunk_size

    return chunk_x, chunk_y 

def chunk_wrap(chunk_x):
    if chunk_x > config.world_length -1:
        chunk_x -= config.world_length
    elif chunk_x < 0:
        chunk_x += config.world_length 
    return chunk_x


def true_to_block_coords(x,y):
    x += config.half_block_size
    #y += config.half_block_size

    chunk_x, chunk_y = get_chunk_coords(x, y)

    block_x = (x - chunk_x * config.chunk_size) // config.block_size + config.blocks_per_half_chunk 
    block_y = (y - chunk_y * config.chunk_size) // config.block_size + config.blocks_per_half_chunk 

    chunk_x = chunk_wrap(chunk_x)

    return chunk_x, chunk_y, block_x, block_y

def chunk_draw_range(player_chunk_x, player_chunk_y):
    x_min, x_max = int((player_chunk_x - config.draw_distance)), int((player_chunk_x + config.draw_distance))
    y_min, y_max = player_chunk_y - config.draw_distance, player_chunk_y + config.draw_distance

    return x_min, x_max, y_min, y_max


#this handles chunk wrap and block overflow correctly so use whenever a block is getting added to chunk
def chunk_block_addition(block_x_distance, block_y_distance, chunk_x, chunk_y, block_x, block_y):
    block_x += block_x_distance
    chunk_x += block_x // config.blocks_per_chunk
    block_x %= config.blocks_per_chunk

    block_y += block_y_distance
    chunk_y += block_y // config.blocks_per_chunk
    block_y %= config.blocks_per_chunk

    chunk_x = chunk_wrap(chunk_x)

    return chunk_x, chunk_y, block_x, block_y

def block_coords_to_true_coords(chunk_x, chunk_y, block_x, block_y):
    x = chunk_x * config.chunk_size + (block_x - config.blocks_per_half_chunk) * config.block_size
    y = chunk_y * config.chunk_size + (block_y - config.blocks_per_half_chunk) * config.block_size
    return x, y

def mouse_true_coords():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    true_x = mouse_x - config.camera_x + player_module.player.x
    true_y = mouse_y - config.camera_y + player_module.player.y

    true_x = phys_module.teleport_to_wrapped_x(true_x)
 
    return true_x, true_y


#create chunk
def generate_ore_veins(block_id, ore_size, veins_per_chunk, min_chunk_y, max_chunk_y):

    dy = max_chunk_y - min_chunk_y
    num_chunks = config.world_length * dy
    num_veins = veins_per_chunk * num_chunks
    for _ in range(num_veins):
        chunk_x = random.randint(0, world_length -1)
        chunk_y = random.randint(min_chunk_y, world_height -1)
        block_x = random.randint(0, blocks_per_chunk -1)
        block_y = random.randint(0, blocks_per_chunk -1)

        chunk_list[chunk_x][chunk_y].create_block(block_x, block_y, block_id)
        for _ in range(ore_size):
            block_x_distance = random.randint(-1,1)
            block_y_distance = random.randint(-1,1)
            chunk_x, chunk_y, block_x, block_y = chunk_block_addition(block_x_distance, block_y_distance, chunk_x, chunk_y, block_x, block_y)

            if chunk_y < world_height: 
                chunk_list[chunk_x][chunk_y].create_block(block_x, block_y, block_id)


def generate_pools(block_id, pools_per_chunk, min_chunk_y, max_chunk_y):
    pool_length = random.randint(5, 20)
    pool_height = random.randint(2, 10)

    dy = max_chunk_y - min_chunk_y
    num_chunks = config.world_length * dy
    num_pools = pools_per_chunk * num_chunks
    for _ in range(num_pools):
        chunk_x = random.randint(0, world_length -1)
        chunk_y = random.randint(min_chunk_y, world_height -1)
        block_x = random.randint(0, blocks_per_chunk -1)
        block_y = random.randint(0, blocks_per_chunk -1)

        chunk_list[chunk_x][chunk_y].create_block(block_x, block_y, block_id)
        for _ in range(pool_length):
            for _ in range(pool_height):
                block_x_distance = random.randint(-1,1)
                block_y_distance = random.randint(-1,1)

                chunk_x, chunk_y, block_x, block_y = chunk_block_addition(block_x_distance, block_y_distance, chunk_x, chunk_y, block_x, block_y)

                if chunk_y < world_height and chunk_y > min_chunk_y: 
                    chunk_list[chunk_x][chunk_y].create_block(block_x, block_y, block_id)
        
        


def generate_chunks(world_length, world_height):
    chunk_list = []
    for _ in range(world_length):
        row = []
        for y in range(world_height):
            #draw sky chunks as blue, ground is random
            if y < 2:
                row.append(chunk_class(1000))
            elif y == 2:
                row.append(chunk_class(1001))
            elif y < world_height -2: 
                row.append(chunk_class(1004))
            #last 2 are darkstone
            else:
                row.append(chunk_class(1007))
        
        chunk_list.append(row)

    return chunk_list


chunk_list = generate_chunks(config.world_length, config.world_height)
generate_ore_veins(1005, 1, 10, 2, 3)
generate_ore_veins(1005, 5, 10, 3, config.world_height - 1)
generate_pools(1006, 10, 2, 3)