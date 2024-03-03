import items
import weapons_module


""" def m_rlauncher():
    #weapon data
    #weapon_sprite = items.weapon_sprites["rlauncher"]
    id = 2000
    weapon_sprite = items.weapon_sprites[2000]
    reload_time = 10
    cooldown = 10

    #projectile data
    explosion_rad = 3
    initial_vel = 25
    proj_gravity = True
    proj_destructiveness = 2
    proj_piercing = 1
    damage = 10
    max_splash_damage = 60
    kb_speed = 50

    bullet_type = "m_rocket"

    max_range = 1000000

    return weapons_module.explosives_class(id, weapon_sprite, reload_time, cooldown, initial_vel, proj_gravity, proj_destructiveness, proj_piercing, damage, bullet_type, max_range, explosion_rad, kb_speed, max_splash_damage) """

def add_explosive_properties(weapon, explosion_rad, max_splash_damage, kb_speed):
    weapon.max_splash_damage = max_splash_damage
    weapon.rad = explosion_rad
    weapon.kb_speed = kb_speed


def m_rlauncher():
    #weapon data
    id = 2000
    weapon_sprite = items.weapon_sprites[2000]
    #weapon_sprite = items.weapon_sprites["rlauncher"]
    reload_time = 10

    initial_vel = 25

    #projectile data
    proj_gravity = True
    proj_destructiveness = 2
    proj_piercing = 1
    damage = 10

    explosion_rad = 3
    max_splash_damage = 60
    kb_speed = 50

    bullet_type = "m_rocket"

    max_range = 1000000

    return weapons_module.explosives_class(id, weapon_sprite, reload_time, initial_vel, proj_gravity, proj_destructiveness, proj_piercing, damage, bullet_type, max_range)
    explosion_rad, kb_speed, max_splash_damage

def rlauncher():
    #weapon data
    #weapon_sprite = items.weapon_sprites["rlauncher"]
    id = 2001
    weapon_sprite = items.weapon_sprites[2000]
    reload_time = 100
    cooldown = 100

    #projectile data
    explosion_rad = 10
    initial_vel = 25
    proj_gravity = True
    proj_destructiveness = 2
    proj_piercing = 1
    damage = 20
    max_splash_damage = 100
    kb_speed = 50

    bullet_type = "rocket"

    max_range = 1000000

    return (id, weapon_sprite, reload_time, cooldown, initial_vel, proj_gravity, proj_destructiveness, proj_piercing, damage, bullet_type, max_range, explosion_rad, kb_speed, max_splash_damage)

def teal_sniper():
    #weapon data
    #weapon_sprite = items.weapon_sprites["rlauncher"]
    id = 2002
    weapon_sprite = items.weapon_sprites[2000]
    max_cooldown = 200
    cooldown = 200

    #projectile data
    proj_rad = 1
    initial_vel = 100
    proj_gravity = True
    proj_destructiveness = 2
    proj_piercing = 6
    damage = 100
    splash_damage = False
    max_splash_damage = 0
    knockback = False
    kb_speed = 0

    bullet_sprite_name = "teal_bullet"

    max_range_bool = False
    max_range = 1000

    return (id, weapon_sprite, max_cooldown, cooldown, proj_rad, initial_vel, proj_gravity, proj_destructiveness, proj_piercing, damage, splash_damage, max_splash_damage, knockback, kb_speed, bullet_sprite_name, max_range_bool, max_range)

def mgun():
    #weapon data
    #weapon_sprite = items.weapon_sprites["rlauncher"]
    id = 2003
    weapon_sprite = items.weapon_sprites[2000]
    max_cooldown = 10
    cooldown = 10

    #projectile data
    proj_rad = 1
    initial_vel = 25
    proj_gravity = True
    proj_destructiveness = 2
    proj_piercing = 0
    damage = 3
    splash_damage = False
    max_splash_damage = 0
    knockback = False
    kb_speed = 0

    bullet_sprite_name = "bullet"

    max_range_bool = False
    max_range = 1000

    return (id, weapon_sprite, max_cooldown, cooldown, proj_rad, initial_vel, proj_gravity, proj_destructiveness, proj_piercing, damage, splash_damage, max_splash_damage, knockback, kb_speed, bullet_sprite_name, max_range_bool, max_range)


def slug_launcher():
    #weapon data
    #weapon_sprite = items.weapon_sprites["rlauncher"]
    id = 2004
    weapon_sprite = items.weapon_sprites[2000]
    reload_time = 100
    cooldown = 100

    #projectile data
    explosion_rad = 0
    initial_vel = 25
    proj_gravity = True
    proj_destructiveness = 2 
    proj_piercing = 1
    damage = 30
    max_splash_damage = 0
    kb_speed = 20

    bullet_type = "seeking_slug"

    max_range = 1000

    acceleration = 2
    accel_delay = 15

    return (id, weapon_sprite, reload_time, cooldown, initial_vel, proj_gravity, proj_destructiveness, proj_piercing, damage, bullet_type, max_range, explosion_rad, kb_speed, max_splash_damage, acceleration, accel_delay)


def mining_laser():
    #weapon data
    #weapon_sprite = items.weapon_sprites["rlauncher"]
    id = 2005
    weapon_sprite = items.weapon_sprites[2000]
    reload_time = 5
    cooldown = 5

    #projectile data
    initial_vel = 20
    proj_gravity = False
    proj_destructiveness = 4
    proj_piercing = 3
    damage = 15

    bullet_type = "mining_laser"

    max_range = 200

    return (id, weapon_sprite, reload_time, cooldown, initial_vel, proj_gravity, proj_destructiveness, proj_piercing, damage, bullet_type, max_range)



weapon_ids = {
    2000 : m_rlauncher(),
    2001 : weapons_module.explosives_class(*rlauncher()), #rocket launcher
    2004 : weapons_module.accelerating_explosives_class(*slug_launcher()),

    2005 : weapons_module.lasers_class(*mining_laser()),
} 

#within funcs, append explosive damage, momentum damage method, charge, acceleration
#when running, hasattr

#replace fire method with charge fire
#replace direct collision, with explosion or momentum damage
#replace direct position update with acceleration update