import pygame
import sys
import random # Aggiunto per eventuali calcoli casuali

# INIZIALIZZAZIONE
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Movimento con Trigger Battaglia")
clock = pygame.time.Clock()

SPRITE_SIZE = (64, 64)
screen_rect = screen.get_rect()

# --- NUOVE VARIABILI PER IL COMBATTIMENTO ---
game_state = "MAP"  # Può essere "MAP" o "BATTLE"
# Creiamo un'area rossa che attiva il combattimento
battle_zone = pygame.Rect(500, 200, 150, 150) 
# Font per scritte a schermo
font = pygame.font.SysFont("Arial", 30)
# --------------------------------------------

def caricaescala(nome_file):
    try:
        img = pygame.image.load(nome_file).convert_alpha()
        return pygame.transform.scale(img, SPRITE_SIZE)
    except:
        # Crea un rettangolo colorato se l'immagine manca per testare il codice
        surf = pygame.Surface(SPRITE_SIZE)
        surf.fill((255, 0, 255))
        return surf

sprites = {
    "up":    caricaescala("cavalierid.png"),
    "down":  caricaescala("cavalieri.png"),
    "left":  caricaescala("cavalieris.png"),
    "right": caricaescala("cavalieride.png")
}

current_dir = "down"
player_rect = sprites[current_dir].get_rect(center=screen_rect.center)
vel = 5

# CICLO PRINCIPALE
while True:
    # 1. GESTIONE EVENTI
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Se siamo in battaglia e premiamo ESC, torniamo alla mappa (esempio)
        if game_state == "BATTLE" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = "MAP"
                player_rect.x -= 70 # Sposta il player fuori dalla zona per non riattivarlo subito

    # 2. LOGICA DI GIOCO
    if game_state == "MAP":
        # Movimento (Il tuo codice originale)
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

        player_rect.clamp_ip(screen_rect)

        # CONTROLLO COLLISIONE: Se il player tocca l'area di battaglia
        if player_rect.colliderect(battle_zone):
            game_state = "BATTLE"

    # 3. DISEGNO (RENDER)
    screen.fill((40, 40, 40)) 

    if game_state == "MAP":
        # Disegna la zona di attivazione (un quadrato rosso semi-trasparente)
        pygame.draw.rect(screen, (200, 0, 0), battle_zone, 2) 
        # Disegna il giocatore
        screen.blit(sprites[current_dir], player_rect)
        
    elif game_state == "BATTLE":
        # battaglia
        screen.fill((0, 0, 0)) # Sfondo nero tipico di Undertale
        
        # Box di battaglia
        battle_box = pygame.Rect(100, 350, 600, 200)
        pygame.draw.rect(screen, (255, 255, 255), battle_box, 3)
        
        # Testo di esempio
        battle_text = font.render("aaaaah sans ", True, (255, 255, 255))
        screen.blit(battle_text, (130, 380))
        
        # Disegna il cuore (l'anima) al centro del box
        pygame.draw.circle(screen, (255, 0, 0), (WIDTH//2, 450), 10)

    pygame.display.flip()
    clock.tick(60)