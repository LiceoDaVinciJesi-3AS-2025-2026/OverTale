import pygame
import sys
import sans_battle

# --- IMPOSTAZIONE DEBUG ---
MOSTRA_COLLISIONI = True # Cambia in False quando vuoi giocare normalmente

pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Undertale_Fight")
clock = pygame.time.Clock()

# --- CARICAMENTO ASSET ---
def carica_sprite(nome, colore_fallback):
    try:
        img = pygame.image.load(nome).convert_alpha()
        return pygame.transform.scale(img, (64, 64))
    except:
        s = pygame.Surface((64, 64)); s.fill(colore_fallback); return s

try:
    mappa_img = pygame.image.load("mappa.png").convert()
    mappa_img = pygame.transform.scale(mappa_img, (WIDTH, HEIGHT))
except:
    mappa_img = pygame.Surface((WIDTH, HEIGHT)); mappa_img.fill((34, 139, 34))

sprites = {
    "up": carica_sprite("cavalierid.png", (0, 255, 0)),
    "down": carica_sprite("cavalieri.png", (255, 0, 0)),
    "left": carica_sprite("cavalieris.png", (0, 0, 255)),
    "right": carica_sprite("cavalieride.png", (255, 255, 0))
}

# --- LISTA OGGETTI CON COLLISIONI (Alberi) ---
alberi = [
    pygame.Rect(0, 0, 900, 60),            # Bosco superiore
    pygame.Rect(0, 640, 900, 60),          # Bosco inferiore
    pygame.Rect(220, 240, 30, 50),       # Cluster sinistra
    pygame.Rect(300, 280, 20, 50),        # Albero centrale
    pygame.Rect(620, 420, 20,50)        # Bosco Sans
]

current_dir = "down"
player_rect = sprites[current_dir].get_rect(center=(450, 350))
vel = 5
sans_vivo = True # uuuh yea è vivo Fah
battle_zone = pygame.Rect(750, 200, 100, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()

    # --- MOVIMENTO ---
    keys = pygame.key.get_pressed()
    vecchia_pos = player_rect.copy()

    if keys[pygame.K_LEFT]: player_rect.x -= vel; current_dir = "left"
    elif keys[pygame.K_RIGHT]: player_rect.x += vel; current_dir = "right"
    elif keys[pygame.K_UP]: player_rect.y -= vel; current_dir = "up"
    elif keys[pygame.K_DOWN]: player_rect.y += vel; current_dir = "down"

    # --- CONTROLLO COLLISIONI ---
    for albero in alberi:
        if player_rect.colliderect(albero):
            player_rect = vecchia_pos
            break
    
    player_rect.clamp_ip(screen.get_rect())

    # Trigger Sans
    if sans_vivo and player_rect.colliderect(battle_zone):
        risultato = sans_battle.UnderTale_Fight(screen, clock)
        if risultato == "VITTORIA": sans_vivo = False
        player_rect.x -= 100

    # DISEGNO
    # 1. Disegna lo sfondo
    screen.blit(mappa_img, (0, 0))
    
    screen.blit(sprites[current_dir], player_rect)

    pygame.display.flip()
    clock.tick(60)