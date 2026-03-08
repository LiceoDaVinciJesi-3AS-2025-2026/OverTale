import pygame
import sys
import sans_battle # Assicurati che il file si chiami esattamente così

# INIZIALIZZAZIONE
pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Undertale Clone - Esplorazione")
clock = pygame.time.Clock()

SPRITE_SIZE = (64, 64)
screen_rect = screen.get_rect()

#FUNZIONE CARICAMENTO IMMAGINI
def caricaescala(nome_file):
    try:
        img = pygame.image.load(nome_file).convert_alpha()
        return pygame.transform.scale(img, SPRITE_SIZE)
    except:
        # Crea un rettangolo colorato se l'immagine manca (rosa di debug)
        surf = pygame.Surface(SPRITE_SIZE)
        surf.fill((255, 0, 255))
        return surf

# Dizionario con immagini
sprites = {
    "up":    caricaescala("cavalierid.png"),
    "down":  caricaescala("cavalieri.png"),
    "left":  caricaescala("cavalieris.png"),
    "right": caricaescala("cavalieride.png")
}

current_dir = "down"
player_rect = sprites[current_dir].get_rect(center=(200, 200))
vel = 5

# Variabili Stato e Trigger
game_state = "MAP"
battle_zone = pygame.Rect(500, 300, 150, 150) 

#FUNZIONE TRANSIZIONE
def transizione_al_nero():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 10):
        fade.set_alpha(alpha)
        # Continuiamo a disegnare la mappa sotto
        screen.fill((40, 40, 40))
        pygame.draw.rect(screen, (200, 0, 0), battle_zone, 2)
        screen.blit(sprites[current_dir], player_rect)
        
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)

# CICLO PRINCIPALE
while True:
    # 1. GESTIONE EVENTI
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 2. LOGICA DI GIOCO (Mappa)
    if game_state == "MAP":
        keys = pygame.key.get_pressed()
        muovendo = False # Per evitare che cambi direzione se non premi nulla
        
        if keys[pygame.K_LEFT]:
            player_rect.x -= vel
            current_dir = "left"
            muovendo = True
        elif keys[pygame.K_RIGHT]:
            player_rect.x += vel
            current_dir = "right"
            muovendo = True
        elif keys[pygame.K_UP]:
            player_rect.y -= vel
            current_dir = "up"
            muovendo = True
        elif keys[pygame.K_DOWN]:
            player_rect.y += vel
            current_dir = "down"
            muovendo = True

        player_rect.clamp_ip(screen_rect)

        # COLLISIONE: Se entri nella zona di Sans
        if player_rect.colliderect(battle_zone):
            transizione_al_nero()
            
            # Lancio del combattimento dal file esterno
            risultato = sans_battle.UnderTale_Fight(screen, clock)
            
            # Al ritorno dalla battaglia
            print(f"Battaglia conclusa con: {risultato}")
            
            # Resettiamo la posizione del player per non restare nel trigger
            player_rect.x -= 100 
            pygame.event.clear() # Pulisce i tasti rimasti premuti

    # 3. DISEGNO (RENDER)
    screen.fill((40, 40, 40)) # Grigio mappa

    if game_state == "MAP":
        # Zona rossa trigger
        pygame.draw.rect(screen, (200, 0, 0), battle_zone, 2) 
        
        # Disegna il cavaliere nella direzione corrente
        screen.blit(sprites[current_dir], player_rect)

    pygame.display.flip()
    clock.tick(60)