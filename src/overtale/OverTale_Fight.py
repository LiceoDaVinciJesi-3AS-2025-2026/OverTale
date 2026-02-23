#Sistema di Combattimento

import pygame
import sys
import random

pygame.init()

#------------------#

# Parametri finestra
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)

#------------------#

# Stati di gioco
PLAYER_TURN = "PLAYER_TURN"
ENEMY_TURN = "ENEMY_TURN"
game_state = PLAYER_TURN

#------------------#

# Battle box
box = pygame.Rect(250, 180, 300, 250)

#------------------#

# Player
player_img = pygame.image.load("Hawking.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))

player_rect = player_img.get_rect()
player_rect.center = box.center  # parte al centro della battle box

player_speed = 5
hp = 100

#------------------#

# Nemico
enemy_hp = 50

#------------------#

# Attacchi nemici
attacks = []
enemy_attack_timer = 0
enemy_attack_duration = 180  # frame turno nemico

#------------FUNZIONI------------#

def handle_player_movement():
    keys = pygame.key.get_pressed()

    # Velocità normale
    speed = player_speed
    
    # Se tieni premuto SHIFT vai più lento (stile Undertale)
    if keys[pygame.K_LSHIFT]:
        speed = 2

    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
    if keys[pygame.K_UP]:
        player_rect.y -= speed
    if keys[pygame.K_DOWN]:
        player_rect.y += speed

    player_rect.clamp_ip(box)
#--------------------------------#

def spawn_attack():
    x = random.randint(box.left, box.right - 10)
    rect = pygame.Rect(x, box.top, 10, 30)
    attacks.append(rect)

#--------------------------------#

def update_attacks():
    for attack in attacks:
        attack.y += 5

    # Rimuove attacchi fuori dal box
    attacks[:] = [a for a in attacks if a.top < box.bottom]

#--------------------------------#

def check_collisions():
    global hp
    for attack in attacks[:]:
        if player_rect.colliderect(attack):
            hp -= 1
            attacks.remove(attack)

#--------------------------------#

def enemy_turn():
    global enemy_attack_timer, game_state

    enemy_attack_timer += 1

    handle_player_movement()
    update_attacks()
    check_collisions()

    # Genera attacchi casuali
    if random.randint(1, 15) == 1:
        spawn_attack()

    # Fine turno nemico
    if enemy_attack_timer >= enemy_attack_duration:
        enemy_attack_timer = 0
        attacks.clear()
        game_state = PLAYER_TURN

#--------------------------------#

def player_turn(events):
    global game_state, enemy_hp

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:  # Attacca
                damage = random.randint(5, 15)
                enemy_hp -= damage
                print("Hai fatto", damage, "danni!")
                game_state = ENEMY_TURN

            if event.key == pygame.K_x:  # Mercy
                print("Hai risparmiato il nemico!")
                pygame.quit()
                sys.exit()

#--------------------------------#

def draw():
    screen.fill((0, 0, 0))

    # Nemico
    pygame.draw.rect(screen, (255, 255, 255), (350, 60, 100, 80))

    # Battle box
    pygame.draw.rect(screen, (255, 255, 255), box, 3)

    # Player
    screen.blit(player_img, player_rect)

    # Attacchi nemici
    for attack in attacks:
        pygame.draw.rect(screen, (255, 255, 255), attack)

    # HP Player
    pygame.draw.rect(screen, (255, 0, 0), (50, 500, max(hp,0) * 2, 20))
    hp_text = font.render("HP", True, (255, 255, 255))
    screen.blit(hp_text, (10, 495))

    # HP Nemico
    pygame.draw.rect(screen, (0, 255, 0), (300, 40, max(enemy_hp,0) * 2, 15))

    # Menu turno player
    if game_state == PLAYER_TURN:
        text = font.render("Z = Fight   X = Mercy", True, (255, 255, 0))
        screen.blit(text, (220, 450))

    pygame.display.flip()

#--------------------------------#
    
# Game loop
while True:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == PLAYER_TURN:
        player_turn(events)
    elif game_state == ENEMY_TURN:
        enemy_turn()

    draw()
    clock.tick(60)