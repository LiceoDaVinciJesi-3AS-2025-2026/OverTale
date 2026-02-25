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
    
    running = True

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
