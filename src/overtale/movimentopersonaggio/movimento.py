import pygame
import sys

# INIZIALIZZAZIONE
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Movimento Confinato e Scaling")
clock = pygame.time.Clock()

# Definiamo la dimensione desiderata per le immagini (es. 64x64 pixel)
SPRITE_SIZE = (64, 64)

# Creiamo un Rect che rappresenta l'area dello schermo per i confini
screen_rect = screen.get_rect()

# 2. CARICAMENTO E RIDIMENSIONAMENTO
def caricaescala(nome_file):
    # Carica l'immagine, la scala alla dimensione scelta e ottimizza i pixel
    img = pygame.image.load(nome_file).convert_alpha()
    return pygame.transform.scale(img, SPRITE_SIZE)

try:
    sprites = {
        "up":    caricaescala("cavalierid.png"),
        "down":  caricaescala("cavalieri.png"),
        "left":  caricaescala("cavalieris.png"),
        "right": caricaescala("cavalieride.png")
    }
except pygame.error as e:
    print(f"Errore nel caricamento: {e}")
    pygame.quit()
    sys.exit()

# Stato iniziale
current_dir = "down"
# Il Rect ora avrà la dimensione esatta (64x64) definita in SPRITE_SIZE
player_rect = sprites[current_dir].get_rect(center=screen_rect.center)
vel = 5

# 3. CICLO PRINCIPALE
while True:
    screen.fill((40, 40, 40)) # Sfondo grigio

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimento
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= vel
        current_dir = "left"
    elif keys[pygame.K_RIGHT]:
        player_rect.x += vel
        current_dir = "right"
    elif keys[pygame.K_UP]:
        player_rect.y -= vel
        current_dir = "up"
    elif keys[pygame.K_DOWN]:
        player_rect.y += vel
        current_dir = "down"

    # Questa riga impedisce al giocatore di uscire dai limiti di schermo
    
    player_rect.clamp_ip(screen_rect)

    # Disegno
    screen.blit(sprites[current_dir], player_rect)

    pygame.display.flip()
    clock.tick(60)
