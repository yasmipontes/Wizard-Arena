import pgzrun
import math
import random
from pygame import Rect

WIDTH = 800
HEIGHT = 600
TITLE = "Dungeon Wizard Arena"
CELL_SIZE = 16
GRID_W = WIDTH // CELL_SIZE
GRID_H = HEIGHT // CELL_SIZE

mode = "MENU"
level = 1
enemies = []
walls = []
floor_tiles = []
camera_x = 0
camera_y = 0
anim_frame = 0
anim_counter = 0
damage_cooldown = 0
player_hurt_flash = 0
attack_animation = 0
attack_direction = "right"
music_enabled = True
sounds_enabled = True
attack_cooldown = 0

buttons = {
    "start": Rect(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50),
    "music": Rect(WIDTH//2 - 100, HEIGHT//2 + 10, 200, 50),
    "exit": Rect(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50)
}

class Hero:
    def __init__(self):
        self.x = 3
        self.y = 3
        self.hp = 100
        self.max_hp = 100
        self.frame = 0
        self.facing = "right"
        self.moving = False
        
    def move(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < GRID_W and 0 <= ny < GRID_H:
            if (nx, ny) not in walls:
                self.x = nx
                self.y = ny
                self.moving = True
                if dx > 0: self.facing = "right"
                elif dx < 0: self.facing = "left"
                return True
        return False
            
    def attack(self):
        global attack_animation, attack_direction, attack_cooldown
        
        if attack_cooldown > 0:
            return False
        
        attack_range = 3
        attack_direction = self.facing
        attack_animation = 15
        attack_cooldown = 30
        
        if sounds_enabled:
            try:
                sounds.attack.play()
            except:
                pass
        
        # Atacar TODOS os inimigos no alcance (corrigido)
        killed_any = False
        for e in enemies[:]:
            dist = abs(e.x - self.x) + abs(e.y - self.y)
            if dist <= attack_range:
                e.hp -= 30
                if e.hp <= 0:
                    enemies.remove(e)
                    self.hp = min(self.max_hp, self.hp + 10)
                    killed_any = True
        
        return killed_any

    def draw(self):
        sprite_name = "wizzard_m_idle_anim_f" + str(self.frame)
        if self.moving:
            sprite_name = "wizzard_m_run_anim_f" + str(self.frame)
        
        px = (self.x * CELL_SIZE) - camera_x + WIDTH // 2 - CELL_SIZE // 2
        py = (self.y * CELL_SIZE) - camera_y + HEIGHT // 2 - CELL_SIZE // 2
        
        actor = Actor(sprite_name)
        actor.topleft = (px, py)
        
        if player_hurt_flash > 0 and player_hurt_flash % 2 == 0:
            screen.draw.filled_rect(Rect(px, py, CELL_SIZE, CELL_SIZE), (255, 0, 0, 100))
        
        actor.draw()
        
        # Animação de ataque (raio elétrico)
        if attack_animation > 0:
            attack_offset = 25 if attack_direction == "right" else -25
            attack_x = px + attack_offset
            attack_y = py + CELL_SIZE // 2
            
            # Brilho externo (maior)
            glow_size = int(attack_animation * 1.8)
            screen.draw.filled_circle((attack_x, attack_y), glow_size, (100, 180, 255))
            
            electric_size = int(attack_animation * 1.2)
            screen.draw.filled_circle((attack_x, attack_y), electric_size, (150, 200, 255))
            
            for i in range(4):
                angle = (i * 90 + attack_animation * 20) % 360
                spark_len = electric_size + random.randint(-3, 3)
                end_x = attack_x + int(spark_len * math.cos(math.radians(angle)))
                end_y = attack_y + int(spark_len * math.sin(math.radians(angle)))
                screen.draw.line((attack_x, attack_y), (end_x, end_y), (200, 255, 255))
            
            core_size = int(attack_animation * 0.6)
            screen.draw.filled_circle((attack_x, attack_y), core_size, (255, 255, 255))
        
        bar_width = 30
        bar_height = 4
        hp_percent = self.hp / self.max_hp
        screen.draw.filled_rect(Rect(px, py - 6, bar_width, bar_height), "red")
        screen.draw.filled_rect(Rect(px, py - 6, int(bar_width * hp_percent), bar_height), "green")

class Enemy:
    def __init__(self, x, y, enemy_type="skelet"):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.frame = 0
        self.facing = "right"
        self.move_cooldown = 0
        
        if enemy_type == "big_demon":
            self.hp = 300
            self.max_hp = 300
            self.damage = 20
        elif enemy_type == "ogre":
            self.hp = 100
            self.max_hp = 100
            self.damage = 15
        else:
            self.hp = 50
            self.max_hp = 50
            self.damage = 10

    def update(self):
        global damage_cooldown, player_hurt_flash
        
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
        
        dist = abs(self.x - player.x) + abs(self.y - player.y)
        
        if dist < 10 and self.move_cooldown == 0:
            # Mover em direção ao jogador (mais devagar)
            self.move_cooldown = 15  # Cooldown de 15 frames entre movimentos
            
            dx = 0
            dy = 0
            
            if player.x > self.x:
                dx = 1
                self.facing = "right"
            elif player.x < self.x:
                dx = -1
                self.facing = "left"
            
            if player.y > self.y:
                dy = 1
            elif player.y < self.y:
                dy = -1
            
            if random.randint(0, 1) == 0:
                nx, ny = self.x + dx, self.y
            else:
                nx, ny = self.x, self.y + dy
            
            if 0 <= nx < GRID_W and 0 <= ny < GRID_H and (nx, ny) not in walls:
                self.x = nx
                self.y = ny
        elif self.move_cooldown == 0:
            if random.randint(0, 100) < 2:
                self.move_cooldown = 20
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                nx, ny = self.x + dx, self.y + dy
                
                if 0 <= nx < GRID_W and 0 <= ny < GRID_H and (nx, ny) not in walls:
                    self.x = nx
                    self.y = ny
                    if dx > 0: self.facing = "right"
                    elif dx < 0: self.facing = "left"
        
        if dist <= 1 and damage_cooldown <= 0:
            player.hp -= self.damage
            damage_cooldown = 30
            player_hurt_flash = 10
            if sounds_enabled:
                try:
                    sounds.monster_attack_sound.play()
                except:
                    pass

    def draw(self):
        sprite_name = f"{self.type}_idle_anim_f{self.frame}"
        
        px = (self.x * CELL_SIZE) - camera_x + WIDTH // 2 - CELL_SIZE // 2
        py = (self.y * CELL_SIZE) - camera_y + HEIGHT // 2 - CELL_SIZE // 2
        
        actor = Actor(sprite_name)
        actor.topleft = (px, py)
        actor.draw()
        
        bar_width = 20
        bar_height = 3
        hp_percent = self.hp / self.max_hp
        screen.draw.filled_rect(Rect(px, py - 5, bar_width, bar_height), "red")
        screen.draw.filled_rect(Rect(px, py - 5, int(bar_width * hp_percent), bar_height), "green")

player = Hero()
decorations = []
sounds_initialized = False

def init_sounds():
    global sounds_initialized
    if not sounds_initialized:
        try:
            # Carregar sons e ajustar volume usando métodos nativos do PgZero
            # O PgZero expõe set_volume() através dos objetos Sound
            sounds.attack.set_volume(0.05)  # 5% volume
            sounds.monster_attack_sound.set_volume(0.3)
            sounds.death_sound.set_volume(0.5)
            music.set_volume(0.15)
            sounds_initialized = True
        except:
            sounds_initialized = True

def generate_dungeon(double_size=False):
    global floor_tiles, walls, GRID_W, GRID_H, decorations
    floor_tiles = []
    walls = []
    decorations = []
    
    if double_size:
        GRID_W = int((WIDTH // CELL_SIZE) * 1.5)
        GRID_H = int((HEIGHT // CELL_SIZE) * 1.5)
    else:
        GRID_W = WIDTH // CELL_SIZE
        GRID_H = HEIGHT // CELL_SIZE
    
    for y in range(GRID_H):
        for x in range(GRID_W):
            floor_type = random.randint(1, 8)
            floor_tiles.append((x, y, f"floor_{floor_type}"))
    
    for x in range(GRID_W):
        walls.append((x, 0))
        walls.append((x, GRID_H - 1))
    for y in range(GRID_H):
        walls.append((0, y))
        walls.append((GRID_W - 1, y))
    
    if not double_size:
        for _ in range(3):
            room_w = random.randint(6, 10)
            room_h = random.randint(6, 10)
            room_x = random.randint(5, GRID_W - room_w - 5)
            room_y = random.randint(5, GRID_H - room_h - 5)
            
            for x in range(room_x, room_x + room_w):
                if abs(x - 3) + abs(room_y - 3) > 3:
                    walls.append((x, room_y))
                walls.append((x, room_y + room_h - 1))
            for y in range(room_y, room_y + room_h):
                if abs(room_x - 3) + abs(y - 3) > 3:
                    walls.append((room_x, y))
                walls.append((room_x + room_w - 1, y))
            
            door_side = random.randint(0, 3)
            if door_side == 0 and (room_x + room_w//2, room_y) in walls:
                walls.remove((room_x + room_w//2, room_y))
            elif door_side == 1 and (room_x, room_y + room_h//2) in walls:
                walls.remove((room_x, room_y + room_h//2))
            
            for _ in range(random.randint(1, 3)):
                dec_x = room_x + random.randint(1, room_w - 2)
                dec_y = room_y + random.randint(1, room_h - 2)
                if (dec_x, dec_y) not in walls:
                    decorations.append((dec_x, dec_y, random.choice(["crate", "column", "skull"])))
    
    num_walls = 100 if double_size else 50
    for _ in range(num_walls):
        wx = random.randint(2, GRID_W - 3)
        wy = random.randint(2, GRID_H - 3)
        if (wx, wy) not in walls and abs(wx - 3) + abs(wy - 3) > 3:
            walls.append((wx, wy))
    
    if double_size:
        mid_x = GRID_W // 2
        for y in range(GRID_H // 2 - 3, GRID_H // 2 + 3):
            for x in range(mid_x - 2, mid_x + 2):
                if (x, y) in walls:
                    walls.remove((x, y))

def setup_level(lvl):
    global enemies, player
    enemies = []
    
    is_double = (lvl == 3)
    generate_dungeon(double_size=is_double)
    
    player.x = 3
    player.y = 3
    
    if lvl == 1:
        # Fase 1: 8 inimigos (6 esqueletos, 2 imps)
        enemy_types = ["skelet"] * 6 + ["imp"] * 2
        spawn_area = (10, GRID_W - 10, 10, GRID_H - 10)
        
    elif lvl == 2:
        enemy_types = ["skelet"] * 4 + ["imp"] * 4 + ["ogre"] * 4
        spawn_area = (10, GRID_W - 10, 10, GRID_H - 10)
        
    else:
        enemy_types_area1 = ["skelet"] * 3 + ["imp"] * 2 + ["ogre"] * 3
        for enemy_type in enemy_types_area1:
            for _ in range(15):
                ex = random.randint(5, GRID_W // 2 - 10)
                ey = random.randint(5, GRID_H - 5)
                if (ex, ey) not in walls and abs(ex - player.x) + abs(ey - player.y) > 8:
                    enemies.append(Enemy(ex, ey, enemy_type))
                    break
        
        # Segunda área (direita): Boss + 4 inimigos
        enemy_types_area2 = ["imp"] * 2 + ["ogre"] * 2
        for enemy_type in enemy_types_area2:
            for _ in range(15):
                ex = random.randint(GRID_W // 2 + 10, GRID_W - 5)
                ey = random.randint(5, GRID_H - 5)
                if (ex, ey) not in walls:
                    enemies.append(Enemy(ex, ey, enemy_type))
                    break
        
        # Boss no canto direito
        boss_x = GRID_W - 10
        boss_y = GRID_H // 2
        enemies.append(Enemy(boss_x, boss_y, "big_demon"))
        return
    
    for enemy_type in enemy_types:
        for _ in range(15):
            ex = random.randint(spawn_area[0], spawn_area[1])
            ey = random.randint(spawn_area[2], spawn_area[3])
            if (ex, ey) not in walls and abs(ex - player.x) + abs(ey - player.y) > 8:
                enemies.append(Enemy(ex, ey, enemy_type))
                break

def draw():
    global anim_frame, anim_counter
    screen.clear()
    screen.fill((20, 12, 28))
    
    if mode == "MENU":
        screen.draw.text("DUNGEON WIZARD ARENA", center=(WIDTH//2, 150), fontsize=50, color="white")
        
        for btn_name, rect in buttons.items():
            color = (70, 50, 100) if btn_name != "exit" else (100, 30, 30)
            screen.draw.filled_rect(rect, color)
            screen.draw.rect(rect, (200, 200, 200))
            
            # Button text
            if btn_name == "start":
                text = "START GAME"
            elif btn_name == "music":
                text = f"MUSIC: {'ON' if music_enabled else 'OFF'}"
            else:
                text = "EXIT"
            
            screen.draw.text(text, center=rect.center, fontsize=30, color="white")
        
        screen.draw.text("Use ARROWS to move | SPACE to attack", center=(WIDTH//2, 500), fontsize=20, color="gray")
        
    elif mode == "GAME":
        for tx, ty, tile_name in floor_tiles:
            px = (tx * CELL_SIZE) - camera_x + WIDTH // 2 - CELL_SIZE // 2
            py = (ty * CELL_SIZE) - camera_y + HEIGHT // 2 - CELL_SIZE // 2
            if -CELL_SIZE < px < WIDTH and -CELL_SIZE < py < HEIGHT:
                actor = Actor(tile_name)
                actor.topleft = (px, py)
                actor.draw()
        
        for wx, wy in walls:
            px = (wx * CELL_SIZE) - camera_x + WIDTH // 2 - CELL_SIZE // 2
            py = (wy * CELL_SIZE) - camera_y + HEIGHT // 2 - CELL_SIZE // 2
            if -CELL_SIZE < px < WIDTH and -CELL_SIZE < py < HEIGHT:
                actor = Actor("wall_mid")
                actor.topleft = (px, py)
                actor.draw()
        
        for dx, dy, dec_type in decorations:
            px = (dx * CELL_SIZE) - camera_x + WIDTH // 2 - CELL_SIZE // 2
            py = (dy * CELL_SIZE) - camera_y + HEIGHT // 2 - CELL_SIZE // 2
            if -CELL_SIZE < px < WIDTH and -CELL_SIZE < py < HEIGHT:
                actor = Actor(dec_type)
                actor.topleft = (px, py)
                actor.draw()
        
        for e in enemies:
            e.draw()
        
        player.draw()
        
        screen.draw.text(f"Nivel: {level}", (10, 10), fontsize=25, color="white")
        screen.draw.text(f"HP: {int(player.hp)}/{player.max_hp}", (10, 35), fontsize=20, color="red")
        screen.draw.text(f"Inimigos: {len(enemies)}", (10, 60), fontsize=20, color="yellow")
        
    elif mode == "WIN":
        screen.draw.text("VITORIA!", center=(400, 280), fontsize=80, color="gold")
        screen.draw.text("Voce completou todas as dungeons!", center=(400, 360), fontsize=30, color="white")
        screen.draw.text("Pressione ESC para sair", center=(400, 410), fontsize=20, color="gray")
    
    elif mode == "GAME_OVER":
        screen.draw.text("GAME OVER", center=(400, 280), fontsize=80, color="red")
        screen.draw.text("Pressione R para recomecar", center=(400, 360), fontsize=30, color="white")
        screen.draw.text("Pressione ESC para sair", center=(400, 410), fontsize=20, color="gray")

def update():
    global mode, level, camera_x, camera_y, anim_frame, anim_counter, damage_cooldown, player_hurt_flash, attack_animation, attack_cooldown
    
    init_sounds()
    
    if music_enabled:
        try:
            if not music.is_playing("the_frog_and_the_mouse"):
                music.play("the_frog_and_the_mouse")
        except:
            pass
    else:
        try:
            music.stop()
        except:
            pass
    
    if mode == "GAME":
        if damage_cooldown > 0:
            damage_cooldown -= 1
        if player_hurt_flash > 0:
            player_hurt_flash -= 1
        if attack_animation > 0:
            attack_animation -= 1
        if attack_cooldown > 0:
            attack_cooldown -= 1
        
        target_cam_x = player.x * CELL_SIZE
        target_cam_y = player.y * CELL_SIZE
        camera_x += (target_cam_x - camera_x) * 0.1
        camera_y += (target_cam_y - camera_y) * 0.1
        
        anim_counter += 1
        if anim_counter >= 10:
            anim_counter = 0
            anim_frame = (anim_frame + 1) % 4
            player.frame = anim_frame
            for e in enemies:
                e.frame = anim_frame
        
        player.moving = False
        
        for e in enemies[:]:
            e.update()
            if e.hp <= 0:
                enemies.remove(e)
        
        if len(enemies) == 0:
            level += 1
            if level > 3:
                mode = "WIN"
            else:
                setup_level(level)
                player.hp = min(player.max_hp, player.hp + 30)
        
        if player.hp <= 0:
            mode = "GAME_OVER"
            if sounds_enabled:
                try:
                    sounds.death_sound.play()
                except Exception as ex:
                    print(f"Erro ao tocar som de morte: {ex}")

def on_mouse_down(pos):
    global mode, level, music_enabled, sounds_enabled, damage_cooldown, player_hurt_flash, attack_animation, attack_cooldown, camera_x, camera_y
    
    if mode == "MENU":
        if buttons["start"].collidepoint(pos):
            mode = "GAME"
            level = 1
            damage_cooldown = 0
            player_hurt_flash = 0
            attack_animation = 0
            attack_cooldown = 0
            camera_x = 0
            camera_y = 0
            player.hp = player.max_hp
            player.x = 3
            player.y = 3
            setup_level(level)
        elif buttons["music"].collidepoint(pos):
            music_enabled = not music_enabled
            sounds_enabled = not sounds_enabled
        elif buttons["exit"].collidepoint(pos):
            exit()

def on_key_down(key):
    global mode, level
    
    if mode == "GAME":
        if key == keys.LEFT:
            player.move(-1, 0)
        elif key == keys.RIGHT:
            player.move(1, 0)
        elif key == keys.UP:
            player.move(0, -1)
        elif key == keys.DOWN:
            player.move(0, 1)
        elif key == keys.SPACE:
            player.attack()
    
    elif mode == "GAME_OVER" and key == keys.R:
        mode = "MENU"
        level = 1
        player.hp = player.max_hp
        player.x = 3
        player.y = 3
    
    if key == keys.ESCAPE:
        exit()

pgzrun.go()