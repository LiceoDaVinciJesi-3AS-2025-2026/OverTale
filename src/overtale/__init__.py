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
    risposta_sì = font_piccolo.render("Si", True, "white")
    risposta_no = font_piccolo.render("No", True, "white")
    
    immagine_sfondo = pygame.image.load("sfondo_schermata.png")

    clock = pygame.time.Clock()
    schermata = "menù"
    
    running = True

    while running:
        # bisogna creare i pulsanti, lo start, il menù impostazioni (con i salvataggi, il volume, ecc.), la parte "esci" del menù (facile) e un modulo con la funzione per salvare il gioco.
        mPos = pygame.mouse.get_pos() 

        screen.blit(immagine_sfondo, (0, 0))
        # Schermata d'entrata
        if schermata == "menù":
            screen.blit(titolo, (350, 150))
            screen.blit(inizio, (500, 317))
            screen.blit(impostazioni, (380, 417))
            screen.blit(uscita_impostazioni, (525, 517))
        # Schermata d'uscita
        elif schermata == "uscita":
            screen.fill("black")
            screen.blit(uscita_gioco, (120, 150))
            screen.blit(risposta_sì, (500, 417))
            screen.blit(risposta_no, (650, 417))
        
        pygame.display.flip()

        for event in pygame.event.get():
# Il running = False è da togliere alla fine di tutto.
            if event.type == pygame.QUIT:
                schermata = "uscita"
                running = False
            
            if event.type == pygame.KEYDOWN:
                
                if schermata == "menù":
                    if event.key == pygame.K_ESCAPE:
                        schermata = "uscita"
            
                elif schermata == "uscita":
                    if event.key == pygame.K_ESCAPE:
                        schermata = "menù"

    pygame.quit()

if __name__ == "__main__":
    main()