import pygame

def main(screen, clock, font_grande, font_piccolo):
    running = True
    # variabili del gioco
    vittoria_sans = False

    while running:
        mPos = pygame.mouse.get_pos()

        screen.fill("black")
        # ... tutto il rendering del gioco ...

        # esempio semplice di vittoria contro Sans
        if vittoria_sans:
            testo_vittoria = font_grande.render("Hai sconfitto Sans!", True, "white")
            screen.blit(testo_vittoria, (300, 300))
            pygame.display.flip()
            pygame.time.delay(2000)  # mostra la scritta per 2 secondi

            # chiude il gioco completamente
            pygame.quit()
            exit()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

            # gestire qui i movimenti, attacchi, ecc.

        pygame.display.flip()
        clock.tick(60)

    # Questa riga non sarà mai raggiunta se si chiude correttamente
    pygame.quit()
    exit()