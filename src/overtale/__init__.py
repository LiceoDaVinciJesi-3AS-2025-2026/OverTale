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
    
    # Questa è l'immagine dello sfondo.
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
            
            # Questi sono i pulsanti del menù: la funzione 'get_rect' crea un rettangolo intorno alla scritta specificata con la sua variabile ( specifico anche il punto di partenza, cioè il topleft=(x, y)).
            pulsante_inizio = inizio.get_rect(topleft=(500,317))
            pulsante_impostazioni = impostazioni.get_rect(topleft=(380, 417))
            pulsante_uscita_impostazioni = uscita_impostazioni.get_rect(topleft=(525, 517))
            # Qua sono da aggiungere i pulsanti dell'inizio, delle impostazioni e dell'uscita.
            
        # Schermata d'uscita
        elif schermata == "uscita":
            screen.fill("black")
            screen.blit(uscita_gioco, (120, 150))
            screen.blit(risposta_sì, (500, 417))
            screen.blit(risposta_no, (650, 417))
            
            # Questi sono i pulsanti della scgermata di uscita (spiego che cos'è 'get_rect' nella parte del menù).
            pulsante_risposta_sì = risposta_sì.get_rect(topleft=(500, 417))
            pulsante_risposta_no = risposta_no.get_rect(topleft=(650, 417))
            # Qua sono da aggiungere i pulsanti del sì e del no.
        
        elif schermata == "impostazioni":
            # devo creare tutta la schermata per le impostazioni (volume, salvataggio e uscita).
        
        pygame.display.flip()
        # Questa parte del programma serve per le varie schermate: quando il videogiocatore preme un determinato tasto,
        # la variabile 'schermata' cambia valore e, in base a esso, cambia la schermata.
        # Per esempio, se premo il tasto esc (pygame.K_ESCAPE) e schermata = "menù", allora schermata diventa "uscita".
        
        for event in pygame.event.get():
# Il running = False è da togliere alla fine di tutto.
            if event.type == pygame.QUIT:
                schermata = "uscita"
                running = False
            
            if event.type == pygame.KEYDOWN:
                
                if schermata == "menù":
                    if event.key == pygame.K_ESCAPE:
                        schermata = "uscita"
                
                        # Devo aggiungere i vari comandi per i diversi tipi di pulsanti della schermata (se premo quel determinato pulsante, il programma fa qualcosa).
                
                elif schermata == "uscita":
                    if event.key == pygame.K_ESCAPE:
                        schermata = "menù"
#                   if event.type == pygame.MOUSEBUTTONDOWN:
                        # Devo aggiungere i vari comandi per i diversi tipi di pulsanti della schermata (se premo quel determinato pulsante, il programma fa qualcosa).
            
            # In questa parte indico quello che succede quando premi i pulsanti. Non devo specificare con quale schermata mi trovo perché i suoi tasti specifici
            # fanno parte solo di uno specifico stato dello schermo("menù", "impostazioni" e "uscita").
            # Per esempio, non posso premere il tasto 'pulsante_risposta_sì' se ' schermata = menù ' perché non ne fa parte e quindi non esiste in quel momento.
            if event.type == pygame.MOUSEBUTTONDOWN:
                
#                 if pulsante_inizio.collidepoint(mPos):
#                     # Qui inizia il gioco.
#                 
#                 elif pulsante_impostazioni.collidepoint(mPos):
#                         schermata = "impostazioni"
                
                if pulsante_uscita_impostazioni.collidepoint(mPos):
                    schermata = "uscita"
                
                elif pulsante_risposta_sì.collidepoint(mPos):
                    running = False
                
                elif pulsante_risposta_no.collidepoint(mPos):
                    schermata = "menù"

    pygame.quit()

if __name__ == "__main__":
    main()


# Per fare la funzione dei salvataggi, unisco il programma scritto da chatgpt con le funzione del modulo ' PlatformDirs ' (la funzione che devo usare mi crea automaticamente una cartella per i salvataggi dalla parte dell'utente).
# Per l'audio e i salvataggi, creerò un modulo nella stessa cartella con le varie funzione per i salvataggi, per spegnere o accendere il volume e per calibrarlo.