#read
#physics module corresponds to all calculations that affect real coordinates

#store object positions and velocities as int

import config
import weapons_module
import mobs_module
import player_module
import chunks

import math

def gravity():
    player_module.player.y_vel += 1

    for entity in weapons_module.projectiles:
        if weapons_module.weapon_ids[entity.parent_weapon].gravity:
            entity.y_vel += 1
    for mob in mobs_module.moblist:
        mob.y_vel += 1

def mob_movement():
    for mob in mobs_module.moblist:
        mob.ai(mob, player_module.player)


def update_pos():
    player_module.player.x += int(player_module.player.x_vel)//2          
    player_module.player.x = teleport_to_wrapped_x(player_module.player.x)
    player_module.player.y += player_module.player.y_vel//2           

    for entity in weapons_module.projectiles:
        if isinstance(weapons_module.weapon_ids[entity.parent_weapon], weapons_module.accelerating_explosives_class):
            weapons_module.weapon_ids[entity.parent_weapon].accelerate(entity)
        
        if entity.distance_travelled > weapons_module.weapon_ids[entity.parent_weapon].max_range:
            weapons_module.projectiles.remove(entity)
        else:
            entity.distance_travelled += (entity.x_vel**2 + entity.y_vel**2)**0.5

    for mob in mobs_module.moblist:
        mob.x += int(mob.x_vel)        
        mob.x = teleport_to_wrapped_x(mob.x)
        mob.y += mob.y_vel         


#return num of frames to interp
def get_interp_fps(speed_x, speed_y):
    #need to ensure x and y change by max of 20 pixels per frame
    if speed_x//config.block_size < 1 and speed_y//config.block_size < 1:
        return 1

    return max(int(speed_x//config.block_size + 1), int (speed_y//config.block_size + 1))


def call_p_collisions():
    for entity in weapons_module.projectiles:

        p_collisions(entity)

#this both checks collisions and updates position because of frame interp
def p_collisions(entity):
    weapon = weapons_module.weapon_ids[entity.parent_weapon]

    interp_fps = get_interp_fps(entity.x_vel, entity.y_vel)
    for _ in range(interp_fps):

        chunk_x, chunk_y, block_x, block_y = chunks.true_to_block_coords(entity.x, entity.y)
        if 0 <= chunk_y < config.world_height:
            if chunks.chunk_list[int(chunk_x)][int(chunk_y)].block_is_solid(int(block_x),int(block_y)):

                if isinstance(weapon, weapons_module.explosives_class):
                    explode_projectile(chunk_x, chunk_y, block_x, block_y, entity)

                else:
                    terrain_damage(chunk_x, chunk_y, block_x, block_y, weapon.destructiveness, weapon.damage)

                projectile_piercing(entity)
                return
            else: 
                for mob in mobs_module.moblist:
                    if entity_collisions(entity, mob):
                        mobs_module.damage_and_death(mob, weapon.damage)
                        explode_projectile(chunk_x, chunk_y, block_x, block_y, entity)

                        #no more collisions if entity does not pierce
                        if projectile_piercing(entity):
                            return
        
        entity.x += entity.x_vel//interp_fps
        entity.x = teleport_to_wrapped_x(entity.x)
        entity.y += entity.y_vel//interp_fps
        entity.rect.center = (entity.x, entity.y)

def projectile_piercing(projectile):
    projectile.piercing -= 1
    if projectile.piercing < 1:
        weapons_module.projectiles.remove(projectile)
        return True
    return False
    

def explode_projectile(chunk_x, chunk_y, block_x, block_y, entity):
    weapon = weapons_module.weapon_ids[entity.parent_weapon]
    radius_explosion(chunk_x, chunk_y, block_x, block_y, weapon.rad, weapon.destructiveness, weapon.max_splash_damage)
    if isinstance(weapons_module.weapon_ids[entity.parent_weapon], weapons_module.explosives_class):
        player_knockback(entity)
        mob_splash_damage(entity) 

def explode_enemy(enemy, rad, destructiveness):
    chunk_x, chunk_y, block_x, block_y = chunks.true_to_block_coords(enemy.x, enemy.y)
    #square_explosion(chunk_x, chunk_y, block_x, block_y, rad, destructiveness)
    radius_explosion(chunk_x, chunk_y, block_x, block_y, rad, destructiveness, enemy.melee_damage)

def mob_splash_damage(projectile):
    weapon = weapons_module.weapon_ids[projectile.parent_weapon]
    for mob in mobs_module.moblist:
        dist = entity_distance(mob, projectile)
        if dist < weapon.rad * config.block_size:
            #damage = max_splash when dist is 0, damage = 0 when dist = rad * block_size
            mobs_module.damage_and_death(mob, int(weapon.max_splash_damage * (1 - dist/(weapon.rad * config.block_size))))
            

def player_knockback(entity):
    weapon = weapons_module.weapon_ids[entity.parent_weapon]
    range_val = weapon.rad * config.block_size
    if abs(entity.x - player_module.player.x) < range_val and abs(entity.y - player_module.player.y) < range_val:
        dx = player_module.player.x - entity.x
        dy = player_module.player.y - entity.y

        mag = math.sqrt(dx**2 + dy**2)
        if mag != 0:
            x_comp = dx / mag
            y_comp = dy / mag

        player_module.player.x_vel += x_comp * weapon.kb_speed
        player_module.player.y_vel += y_comp * weapon.kb_speed

def teleport_to_wrapped_x(x):
    if x < config.min_x:
        x += config.world_length * config.chunk_size 
    elif x > config.max_x: 
        x -= config.world_length * config.chunk_size
    return x

#simple explosion for complete block removal in radius
#def explosion(chunk_x, chunk_y, block_x, block_y, explosion_rad):
""" def square_explosion(chunk_x, chunk_y, block_x, block_y, explosion_rad, destructiveness, damage):
    chx, chy, blkx, blky = int(chunk_x), int(chunk_y), int(block_x), int(block_y)
    for y in range(-explosion_rad, explosion_rad):
        for x in range(-explosion_rad, explosion_rad):
            chx, chy, blkx, blky = chunks.chunk_block_addition(x, y, int(chunk_x), int(chunk_y), int(block_x), int(block_y))    
            if chy < config.world_height:
                if destructiveness >= chunks.chunk_list[int(chunk_x)][int(chunk_y)].block_hardness(int(block_x),int(block_y)):
                    chunks.chunk_list[int(chunk_x)][int(chunk_y)].health_grid[int(block_x),int(block_y)] -= damage
                    chunks.chunk_list[int(chx)][int(chy)].draw_block(blkx,blky, 1000)
                    chunks.chunk_list[int(chx)][int(chy)].create_block(blkx,blky, 1000)

                    if chunks.chunk_list[int(chunk_x)][int(chunk_y)].health_grid[int(block_x),int(block_y)] < 0:
                        chunks.chunk_list[int(chx)][int(chy)].create_block(blkx,blky, 1000) """

def radius_explosion(chunk_x, chunk_y, block_x, block_y, explosion_rad, destructiveness, damage):
    chx, chy, blkx, blky = int(chunk_x), int(chunk_y), int(block_x), int(block_y)
    for y in range(-explosion_rad, explosion_rad):
        for x in range(-explosion_rad, explosion_rad): 
            rad_to_block = math.hypot(y,x)
            if rad_to_block <= explosion_rad and chy < config.world_height:
                chx, chy, blkx, blky = chunks.chunk_block_addition(x, y, int(chunk_x), int(chunk_y), int(block_x), int(block_y)) 

                damage_at_distance = damage*(explosion_rad - rad_to_block)/explosion_rad
                terrain_damage(chx, chy, blkx, blky, destructiveness, damage_at_distance)

def terrain_damage(chunk_x, chunk_y, block_x, block_y, destructiveness, damage):
    if destructiveness >= chunks.chunk_list[int(chunk_x)][int(chunk_y)].block_hardness(int(block_x),int(block_y)):
        chunks.chunk_list[int(chunk_x)][int(chunk_y)].health_grid[int(block_x),int(block_y)] -= damage
        
        #replace if destroyed
        if chunks.chunk_list[int(chunk_x)][int(chunk_y)].health_grid[int(block_x),int(block_y)] < 0:
            chunks.chunk_list[int(chunk_x)][int(chunk_y)].create_block(block_x,block_y, 1000)
        #else show damage on current block
        else:
            chunks.chunk_list[int(chunk_x)][int(chunk_y)].draw_block(block_x,block_y, chunks.chunk_list[int(chunk_x)][int(chunk_y)].grid[int(block_x),int(block_y)])
        
def entity_collisions(entity1, entity2):
    if entity1.rect.colliderect(entity2.rect):
        return 1
    if entity1.rect.center[0] - entity1.rect.width//2 - entity2.rect.width//2 < entity2.rect.center[0] < entity1.rect.center[0] + entity1.rect.width//2 + entity2.rect.width//2:
        if entity1.rect.center[1] - entity1.rect.height//2 - entity2.rect.height//2 < entity2.rect.center[1] < entity1.rect.center[1] + entity1.rect.height//2 + entity2.rect.height//2:
            return 1 
        
def entity_distance(entity1, entity2):
    x_dist = entity1.rect.center[0] - entity2.rect.center[0]
    y_dist = entity1.rect.center[1] - entity2.rect.center[1]

    return int(math.hypot(x_dist, y_dist))


def collisions():
    terrain_collisions(player_module.player)

    for mob in mobs_module.moblist:
        terrain_collisions(mob)

    for mob in mobs_module.moblist:
        if entity_collisions(player_module.player, mob):
            if mob.check_attack_cooldown():
                mobs_module.damage_and_death(player_module.player, mobs_module.moblist[0].melee_damage)


def terrain_collisions(object):
    chunk_x, chunk_y, block_x, block_y = chunks.true_to_block_coords(object.x, object.y)
    if chunk_y > -2:

        block_y_distance = object.height//2
        block_x_distance = object.width//2

        #first check grounding
        temp_chunk_x, temp_chunk_y, temp_block_x, temp_block_y = chunks.chunk_block_addition(0, block_y_distance, chunk_x, chunk_y, block_x, block_y)
        
        #important: chunk wraps to minus ie the underground. dont check collisions above build limit (chunk 0)
        if temp_chunk_y > -1 and temp_chunk_y < config.world_height:
            if chunks.chunk_list[int(temp_chunk_x)][int(temp_chunk_y)].block_is_solid(int(temp_block_x),int(temp_block_y)):
                object.grounded = 1
                x,y = chunks.block_coords_to_true_coords(temp_chunk_x, temp_chunk_y, temp_block_x, temp_block_y)                 
                object.y = y - block_y_distance * config.block_size 
                object.y_vel = 0
            #else, check collisions below
            else:
                object.grounded = 0
                temp_chunk_x, temp_chunk_y, temp_block_x, temp_block_y = chunks.chunk_block_addition(0, -block_y_distance, chunk_x, chunk_y, block_x, block_y)
                if chunks.chunk_list[int(temp_chunk_x)][int(temp_chunk_y)].block_is_solid(int(temp_block_x),int(temp_block_y)):
                    if temp_chunk_y > -1 and temp_chunk_y < config.world_height:
                        x,y = chunks.block_coords_to_true_coords(temp_chunk_x, temp_chunk_y, temp_block_x, temp_block_y)                 
                        object.y = y + block_y_distance * config.block_size + config.block_size
                        object.y_vel = 0

        #check sides
        temp_chunk_x, temp_chunk_y, temp_block_x, temp_block_y = chunks.chunk_block_addition(block_x_distance, 0, chunk_x, chunk_y, block_x, block_y)
        if chunks.chunk_list[int(temp_chunk_x)][int(temp_chunk_y)].block_is_solid(int(temp_block_x),int(temp_block_y)):
            if temp_chunk_y > -1 and temp_chunk_y < config.world_height:
                x,y = chunks.block_coords_to_true_coords(temp_chunk_x, temp_chunk_y, temp_block_x, temp_block_y)                 
                object.x = x - block_x_distance * config.block_size - config.block_size//2 
                object.x_vel = 0
            
        else:
            temp_chunk_x, temp_chunk_y, temp_block_x, temp_block_y = chunks.chunk_block_addition(-block_x_distance, 0, chunk_x, chunk_y, block_x, block_y)
            if chunks.chunk_list[int(temp_chunk_x)][int(temp_chunk_y)].block_is_solid(int(temp_block_x),int(temp_block_y)):
                if temp_chunk_y > -1 and temp_chunk_y < config.world_height:
                    x,y = chunks.block_coords_to_true_coords(temp_chunk_x, temp_chunk_y, temp_block_x, temp_block_y)                 
                    object.x = x + block_x_distance * config.block_size + config.block_size//2 
                    object.x_vel = 0
          

def apply_drag_and_friction():
    drag(player_module.player)
    friction(player_module.player)

    for mob in mobs_module.moblist:
        friction(mob)
        drag(mob)

def drag(object):
    drag_coeff = 0.001
    #when on ground
    x_drag = 0
    y_drag = 0
    

    if -0.2 < object.x_vel < 0.2:
        object.x_vel = 0
    elif object.x_vel > 0.2:
        x_drag = -drag_coeff * object.x_vel**2
    elif object.x_vel < -0.2:
        x_drag = drag_coeff * object.x_vel**2

    if -0.2 < object.y_vel < 0.2:
        object.y_vel = 0
    elif object.y_vel > 0.2:
        y_drag = -drag_coeff * object.y_vel**2
    elif object.y_vel < -0.2:
        y_drag = drag_coeff * object.y_vel**2
    
    object.x_vel += int(x_drag)
    object.y_vel += int(y_drag)


def friction(object):
    if object.grounded:
        if object.x_vel > 0:
            object.x_vel -= 0.3
        if object.x_vel < 0:
            object.x_vel += 0.3