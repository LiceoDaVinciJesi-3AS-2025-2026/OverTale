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
    uscita_menù = font_piccolo.render("Esci", True, "white")
    uscita_impostazioni = font_piccolo.render("Esci", True, "white")
    risposta_sì = font_piccolo.render("Si", True, "white")
    risposta_no = font_piccolo.render("No", True, "white")
    volume = font_piccolo.render("Volume", True, "white")
    salvataggio = font_piccolo.render("Salva", True, "white")
    
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
            screen.blit(titolo, (500, 150))
            screen.blit(inizio, (585, 317))
            screen.blit(impostazioni, (505, 417))
            screen.blit(uscita_menù, (595, 517))
            
            # Questi sono i pulsanti del menù: la funzione 'get_rect' crea un rettangolo intorno alla scritta specificata con la sua variabile ( specifico anche il punto di partenza, cioè il topleft=(x, y)).
            pulsante_inizio = inizio.get_rect(topleft=(585,317))
            pulsante_impostazioni = impostazioni.get_rect(topleft=(505, 417))
            pulsante_uscita_menù = uscita_menù.get_rect(topleft=(595, 517))
            
        # Schermata d'uscita
        elif schermata == "uscita":
            screen.fill("black")
            screen.blit(uscita_gioco, (250, 150))
            screen.blit(risposta_sì, (500, 417))
            screen.blit(risposta_no, (650, 417))
            
            # Questi sono i pulsanti della schermata di uscita (spiego che cos'è 'get_rect' nella parte del menù).
            pulsante_risposta_sì = risposta_sì.get_rect(topleft=(500, 417))
            pulsante_risposta_no = risposta_no.get_rect(topleft=(650, 417))
        
        elif schermata == "impostazioni":
            screen.fill("black")
            screen.blit(volume, (550, 200))
            screen.blit(salvataggio, (570, 350))
            screen.blit(uscita_impostazioni, (585, 500))
            
            pulsante_volume = volume.get_rect(topleft=(550, 200))
            pulsante_salvataggio = salvataggio.get_rect(topleft=(570, 350))
            pulsante_uscita_impostazioni = uscita_impostazioni.get_rect(topleft=(585, 500))
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
            # Questa parte riguarda le reazioni del gioco quando premi un tasto della tastiera (l'unico tasto è esc).
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    if schermata == "menù":
                        schermata = "uscita"
                    
                    elif schermata == "uscita" or schermata == "impostazioni":
                        schermata = "menù"
                    
            # Qua sono programmate tutte le reazioni del gioco quando premi i pulsanti.        
            if event.type == pygame.MOUSEBUTTONDOWN:

                if schermata == "menù":
                    
#                     if pulsante_inizio.collidepoint(mPos):
#                         qui inizia il gioco
                    if pulsante_impostazioni.collidepoint(mPos):
                        schermata = "impostazioni"

                    elif pulsante_uscita_menù.collidepoint(mPos):
                        schermata = "uscita"


                elif schermata == "uscita":

                    if pulsante_risposta_sì.collidepoint(mPos):
                        running = False

                    elif pulsante_risposta_no.collidepoint(mPos):
                        schermata = "menù"
                
                elif schermata == "impostazioni":
                    
#                     if pulsante_volume.collidepoint(mPos):
#                         qua c'è la parte del volume.
                    
#                     elif pulsante_salvataggio.collidepoint(mPos):
#                         qua c'è la parte del salvataggio.
                    
                    if pulsante_uscita_impostazioni.collidepoint(mPos):
                        schermata = "menù"
    
    pygame.quit()

if __name__ == "__main__":
    main()


# Per fare la funzione dei salvataggi, unisco il programma scritto da chatgpt con le funzione del modulo ' PlatformDirs ' (la funzione che devo usare mi crea automaticamente una cartella per i salvataggi dalla parte dell'utente).
# Per l'audio e i salvataggi, creerò un modulo nella stessa cartella con le varie funzione per i salvataggi, per spegnere o accendere il volume e per calibrarlo.