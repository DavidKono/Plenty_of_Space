import pygame
import config

final_screen = pygame.display.set_mode((config.screen_width, config.screen_height), pygame.FULLSCREEN)

#blocks start with 1
#weapons start with 2
#ammo starts with 3
#materials start with 4
#consumables start with 5

#each item has a corresponding physical sprite, item sprite

""" items_ids = {
    1000: void_block,
    1001: dirt_block,
    1002: grass_block,
    1004: stone_block,

    2001: rocket_launcher,
    2002: mgun,
    2003: drill,
    2004: dirtgun,

    2005: rocket mgun
    2006: cannon launcher

    3001: rockets,
    3002: bullets,

    5001: slime_spawner,
    5002: health_buff
} """

block_ids = {
    1000: "void_block",
    1001: "dirt_block",
    1002: "grass_block",
    1004: "stone_block",
    1007: "dark_stone"
}

#pygame .convert() needed
block_sprites = {
    0000: pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/blocks/block_damage.png").convert_alpha(),
    1000: pygame.Surface((config.block_size, config.block_size), pygame.SRCALPHA), #void
    1001: pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/blocks/dirt1.png").convert(), #dirt
    1002: pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/blocks/grass1.png").convert(), #grass
    1004: pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/blocks/pinkstone.png").convert(), #stone
    1005: pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/blocks/iron_ore.png").convert(), #iron
    1006: pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/blocks/oil.png").convert(), #oil
    1007: pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/blocks/dark_stone.png").convert() #dark_stone
}

weapon_sprites = {
    #"rlauncher": pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/weapons/rocket_launcher.png"),
    2000: pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/weapons/rocket_launcher.png"),
    2001: pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/weapons/rocket_launcher.png"),

    2002: pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/weapons/rocket_launcher.png"),
    2003: pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/weapons/rocket_launcher.png"),
    2004: pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/weapons/rocket_launcher.png")
}

ammo_sprites = {
    "m_rocket": pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/projectiles/m_rocket.png"),
    "rocket": pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/projectiles/rocket.png"),

    "bullet": pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/projectiles/bullet.png"),
    "db_bullet": pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/projectiles/db_bullet.png"),
    "green_bullet": pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/projectiles/green_bullet.png"),
    "grey_bullet": pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/projectiles/grey_bullet.png"),
    "pink_bullet": pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/projectiles/pink_bullet.png"),
    "purple_bullet": pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/projectiles/purple_bullet.png"),
    "red_bullet": pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/projectiles/red_bullet.png"),
    "teal_bullet": pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/projectiles/teal_bullet.png"),

    "seeking_slug" : pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/projectiles/seeking_slug.png"),
    "seeking_slug_unlit" : pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/projectiles/seeking_slug_unlit.png"),

    "mining_laser" : pygame.image.load("C:/Users/Daithi/Documents/Coding/plenty_of_space/sprites/projectiles/laser.png")

}