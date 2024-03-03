import ctypes
import time
import pygame

pygame.init()

pause = False   

shadows = True

clock = 0
 
#screen and camera
user32 = ctypes.windll.user32

og_width = user32.GetSystemMetrics(0)
og_height = user32.GetSystemMetrics(1)

#zoom variables
max_zoom_out = 1
zoom = 1
screen_width = og_width 
screen_height = og_height 
camera_x = og_width // 2
camera_y = og_height // 2

#chunk parameters, and config for modules
draw_distance = 2
world_length = 30
world_height = 12

block_size = 20
half_block_size = block_size//2
blocks_per_chunk = 32
chunk_size = blocks_per_chunk * block_size

#useful variables
blocks_per_half_chunk = blocks_per_chunk // 2
half_chunk_size = chunk_size // 2
max_x = world_length * chunk_size - half_chunk_size
min_x = -half_chunk_size

inventory_length = 10
inventory_height = 10


font = pygame.font.Font(None, 50)
smolfont = pygame.font.Font(None, 30)
smollerfont = pygame.font.Font(None, 20)

#colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CRIMSON = (157, 30, 50)
BLACK = (0,0,0)
GREEN = (30,170,30)
GREY = (100, 100, 100)
BRASS = (255, 170, 50)
BROWN = (88, 57, 39)


def time_in_ms(func, *args, **kwargs):
    start_time = time.time()
    func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    print(f'{func.__name__}: {elapsed_time} ms')