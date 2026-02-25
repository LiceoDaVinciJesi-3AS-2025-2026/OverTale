def main() -> None:
    import pygame
    
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("OverTale")
    
    font_grande = pygame.font.SysFont('Minecraft', 100)
    font_piccolo = pygame.font.SysFont('Minecraft', 67)
    
    # Questi sono tutti i titoli e le scritte (sono da finire).
    titolo = font_grande.render("OverTale", True, "white")
    uscita_gioco = font_grande.render("Vuoi uscire dal gioco?", True, "white")
    inizio = font_piccolo.render("Start", True, "white")
    impostazioni = font_piccolo.render("Impostazioni", True, "white")
    uscita_impostazioni = font_piccolo.render("Esci", True, "white")
    risposta_sì = font_piccolo.render("Sì", True, "white")
    risposta_no = font_piccolo.render("No", True, "white")

    clock = pygame.time.Clock()
    
<<<<<<< Updated upstream
=======
    running = True
>>>>>>> Stashed changes
    while running:
        # Schermata iniziale
        screen.fill("black")
        screen.blit(titolo, (500, 150))
        screen.blit(inizio, (550, 317))
        screen.blit(impostazioni, (550, 417))
        screen.blit(uscita_impostazioni, (550, 517))
        
        pygame.display.flip()

# Da controllare perché non me lo apre sul mio computer      
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                # Schermata d'uscita
                screen.blit(uscita_gioco, (500, 150))
                screen.blit(risposta_sì, (550, 417))
                screen.blit(risposta_no, (700, 417))
                
                pygame.display.flip()
                
                if event.type == pygame.QUIT:
                    running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen.blit(uscita_gioco, (500, 150))
                    screen.blit(risposta_sì, (550, 417))
                    screen.blit(risposta_no, (700, 417))
                    
                    running = False

    pygame.quit()
<<<<<<< Updated upstream

main()
=======
    
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
player = pygame.Rect(390, 300, 20, 20)
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

    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if keys[pygame.K_UP]:
        player.y -= player_speed
    if keys[pygame.K_DOWN]:
        player.y += player_speed

    player.clamp_ip(box)

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
        if player.colliderect(attack):
            hp -= 1
            attacks.remove(attack)  # Colpito, attacco rimosso

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
    pygame.draw.rect(screen, (255, 0, 0), player)

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
>>>>>>> Stashed changes
