import pygame
import sys
import sans_battle


def main(screen, clock, font_grande, font_piccolo):

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
            s = pygame.Surface((64, 64))
            s.fill(colore_fallback)
            return s

    try:
        mappa_img = pygame.image.load("mappa.png").convert()
        mappa_img = pygame.transform.scale(mappa_img, (WIDTH, HEIGHT))
    except:
        mappa_img = pygame.Surface((WIDTH, HEIGHT))
        mappa_img.fill((34, 139, 34))

    sprites = {
        "up":    carica_sprite("cavalierid.png",  (0, 255, 0)),
        "down":  carica_sprite("cavalieri.png",   (255, 0, 0)),
        "left":  carica_sprite("cavalieris.png",  (0, 0, 255)),
        "right": carica_sprite("cavalieride.png", (255, 255, 0))
    }

    # --- CARICAMENTO SANS E CESPUGLI (una volta sola, fuori dal loop) ---
    try:
        sans_img = pygame.image.load("sansi.png").convert_alpha()
        sans_img = pygame.transform.scale(sans_img, (70, 98))
    except:
        sans_img = pygame.Surface((70, 98))
        sans_img.fill((100, 149, 237))

    try:
        cespuglio_img = pygame.image.load("cespuglio.png").convert_alpha()
        cespuglio_img = pygame.transform.scale(cespuglio_img, (90, 90))
    except:
        cespuglio_img = pygame.Surface((90, 90))
        cespuglio_img.fill((0, 100, 0))

    # --- LISTA OGGETTI CON COLLISIONI (Alberi) ---
    alberi = [
        # Bordi della mappa
        pygame.Rect(0, 0, 900, 60),       # Bosco superiore
        pygame.Rect(0, 640, 900, 60),     # Bosco inferiore
        # Alberi sparsi sulla mappa
        pygame.Rect(220, 260, 120, 70),
        pygame.Rect(430, 460, 40, 50),
        pygame.Rect(610, 420, 40, 60),
        pygame.Rect(110, 380, 40, 50),
    ]

    current_dir = "down"
    player_rect = sprites[current_dir].get_rect(center=(450, 350))
    vel = 5
    sans_vivo = True
    battle_zone = pygame.Rect(770, 220, 60, 60)

    # --- GAME LOOP ---
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menù"

        # --- MOVIMENTO ---
        keys = pygame.key.get_pressed()
        vecchia_pos = player_rect.copy()

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

        # --- CONTROLLO COLLISIONI ---
        for albero in alberi:
            if player_rect.colliderect(albero):
                player_rect = vecchia_pos
                break

        player_rect.clamp_ip(screen.get_rect())

        # --- TRIGGER BATTAGLIA SANS ---
        if sans_vivo and player_rect.colliderect(battle_zone):
            risultato = sans_battle.UnderTale_Fight(screen, clock)
            if risultato == "VITTORIA":
                sans_vivo = False
            player_rect.x -= 100

        # --- DISEGNO (tutto dentro il loop, nell'ordine corretto) ---

        # 1. Sfondo / mappa
        screen.blit(mappa_img, (0, 0))

        # 2. Player
        screen.blit(sprites[current_dir], player_rect)

        # 3. Sans (solo se è ancora vivo) — disegnato PRIMA dei cespugli
        #    così i cespugli gli passano sopra e sembra nascosto
        if sans_vivo:
            screen.blit(sans_img, (777, 203))

        # 4. Cespugli (sopra sans, per l'effetto "nascosto")
        screen.blit(cespuglio_img, (730, 220))
        screen.blit(cespuglio_img, (800, 220))

        pygame.display.flip()
        clock.tick(60)