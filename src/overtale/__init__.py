def main() -> None:
    import pygame
    # È un modulo a parte con tutte le funzioni per salvare nel gioco
    import salvataggi
    # È un modulo a parte con tutte le funzione per lo svolgimento del gioco
    import movimento
    
    pygame.init()
    
    audio_disponibile = True
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("musica_menù.mp3") 
        pygame.mixer.music.play(- 1)
    except pygame.error:
        print("Il gioco non avrà la musica di sottofondo perché questo computer ha le funzione dell'audio disabilitate.")
        audio_disponibile = False
    
    musica_attiva = audio_disponibile

    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("OverTale")
    
    # È il volume di default del gioco
    volume_musica = 0.50
    
    if audio_disponibile:
        pygame.mixer.music.set_volume(volume_musica) 
    
    font_grande = pygame.font.SysFont('Minecraft', 100)
    font_piccolo = pygame.font.SysFont('Minecraft', 67)
    
    # Questi sono tutti i titoli e le scritte.
    titolo = font_grande.render("OverTale", True, "white")
    uscita_gioco = font_grande.render("Vuoi uscire dal gioco?", True, "white")
    regolazione_volume = font_grande.render("Calibra il volume:", True, "white")
    attivazione_volume = font_grande.render("Musica:", True, "white")
    meno_volume = font_grande.render("-", True, "white")
    più_volume = font_grande.render("+", True, "white")
    creazione_nuovo_salvataggio = font_grande.render("Crea nuovo salvataggio", True, "white")
    selezione_salvataggi = font_grande.render("Seleziona salvataggio", True, "white")
    conferma_salvataggio = font_grande.render("Vuoi creare un salvataggio?", True, "white")
    salvataggi_disponibili = font_grande.render("Salvataggi esistenti:", True, "white")
    
    inizio = font_piccolo.render("Start", True, "white")
    impostazioni = font_piccolo.render("Impostazioni", True, "white")
    uscita_menù = font_piccolo.render("Esci", True, "white")
    uscita_impostazioni = font_piccolo.render("Esci", True, "white")
    uscita_volume = font_piccolo.render("Esci", True, "white")
    risposta_sì = font_piccolo.render("Si", True, "white")
    risposta_no = font_piccolo.render("No", True, "white")
    volume = font_piccolo.render("Volume", True, "white")
    salvataggio = font_piccolo.render("Salva", True, "white")
    uscita_salvataggio = font_piccolo.render("Esci", True, "white")
    risposta_sì_salvataggio = font_piccolo.render("Sì", True, "white")
    risposta_no_salvataggio = font_piccolo.render("No", True, "white")
    uscita_selezione_salvataggi = font_piccolo.render("Esci", True, "white")
    
    # Questa è l'immagine dello sfondo.
    immagine_sfondo = pygame.image.load("sfondo_schermata.png")

    clock = pygame.time.Clock()
    schermata = "menù"
    
#    # Queste sono le variabili per il controllo del tempo del volume.
#     tempo_click = 0
#     ultimo_scorrimento = 0
#     ritardo = 1000
#     intervallo = 50
    
    running = True
    gioco_effettivo = False

    while running:
        
        # Dopo che avrai vinto, il gioco ti chiederà di premere esc per uscire per ricominciare
        if gioco_effettivo:
            risultato = movimento.main(screen, clock, font_grande, font_piccolo)
            
            # la funzione main di movimento.py contiene il ciclo (while True) che le permette 
            # di ritornare "menù"
            if risultato == "menù":
                gioco_effettivo = False
                schermata = "menù"
            
                screen = pygame.display.set_mode((1280, 720))
        
        mPos = pygame.mouse.get_pos()
#         # Questa è una funzione che indica quando il mouse viene tenuto premuto (lo [0] indica il tasto sinistro del mouse).
#         mouse_premuto = pygame.mouse.get_pressed()[0]
#         # Questa è una funzione che mi calcola quanto tempo, espresso in milliseondi (0,001 s), è passato dall'avvio di Pygame.
#         tempo_attuale = pygame.time.get_ticks()
        
        screen.fill("black")
        # Schermata d'entrata
        if schermata == "menù":
            screen.blit(immagine_sfondo, (0, 0))
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
            screen.blit(uscita_gioco, (250, 150))
            screen.blit(risposta_sì, (520, 417))
            screen.blit(risposta_no, (670, 417))
            
            # Questi sono i pulsanti della schermata di uscita (spiego che cos'è 'get_rect' nella parte del menù).
            pulsante_risposta_sì = risposta_sì.get_rect(topleft=(520, 417))
            pulsante_risposta_no = risposta_no.get_rect(topleft=(670, 417))
        
        # Schermata delle impostazioni
        elif schermata == "impostazioni":
            screen.blit(volume, (550, 200))
            screen.blit(salvataggio, (570, 350))
            screen.blit(uscita_impostazioni, (585, 500))
            
            pulsante_volume = volume.get_rect(topleft=(550, 200))
            pulsante_salvataggio = salvataggio.get_rect(topleft=(570, 350))
            pulsante_uscita_impostazioni = uscita_impostazioni.get_rect(topleft=(585, 500))
            
        # Schermata del volume
        elif schermata == "volume":
            screen.blit(regolazione_volume, (200, 200))
            screen.blit(meno_volume, (810, 200))
            screen.blit(più_volume, (980, 200))
            screen.blit(attivazione_volume, (200, 400))
            screen.blit(uscita_volume, (585, 600))
            
            # Creo nel ciclo la scritta del numero in modo che il gioco la cambi ogni volta che la modifica:
            # quando premi sul - o il +, il programma modifica la variabile volume_musica, toglie la scritta
            # del volume precedente e ci aggiunge quella nuova.
            quantità_volume = font_grande.render(f"{int(volume_musica * 100)}", True, "white")
            
            # Questa parte seve a creare le scritte per i pulsanti "ON" e "OFF" accanto alla scritta "Musica:".
            # " musica_attiva" è una variabile che ho messo fuori dal ciclo e che è uguale a True. Se è uguale a True,
            # il tasto ha scritto "ON", altimenti c'è scritto "OFF" (andare alla parte dei pulsanti su schermata ==
            # "volume" per il continuo).
            if musica_attiva:
                tasto_attivazione_musica = font_grande.render(f"ON", True, "white")
                screen.blit(tasto_attivazione_musica, (475, 400))
            
            else:
                tasto_attivazione_musica = font_grande.render(f"OFF", True, "white")
                screen.blit(tasto_attivazione_musica, (475, 400))

            # Questo pezzo serve per centrare il numero del volume quando è composto da 1, 2 o 3 cifre.
            if volume_musica == 1.00:
                screen.blit(quantità_volume, (850, 200))
            
            elif volume_musica >= 0 and volume_musica < 0.1:
                screen.blit(quantità_volume, (890, 200))
            
            else:
                screen.blit(quantità_volume, (875, 200))
            
            pulsante_uscita_volume = uscita_volume.get_rect(topleft=(585, 600))
            pulsante_meno_volume = meno_volume.get_rect(topleft=(810, 200))
            pulsante_più_volume = più_volume.get_rect(topleft=(980, 200))
            pulsante_tasto_attivazione_musica = tasto_attivazione_musica.get_rect(topleft=(475, 400))
            
#             if mouse_premuto and tempo_attuale - tempo_click > ritardo:
#                 if tempo_attuale - ultimo_scorrimento > intervallo:
# 
#                     if pulsante_meno_volume.collidepoint(mPos):
#                         volume_musica = max(0.0, round(volume_musica - 0.002, 3))
#                         pygame.mixer.music.set_volume(volume_musica)
# 
#                     elif pulsante_più_volume.collidepoint(mPos):
#                         volume_musica = min(1.0, round(volume_musica + 0.002, 3))
#                         pygame.mixer.music.set_volume(volume_musica)
# 
#                     ultimo_scorrimento = tempo_attuale
            
            # da mettere tutto il resto.
        
        # Schermata delle opzioni di salvataggio
        elif schermata == "salvataggio":
            screen.blit(creazione_nuovo_salvataggio, (200, 225))
            screen.blit(selezione_salvataggi, (200, 400))
            screen.blit(uscita_salvataggio, (585, 600))
            
            pulsante_creazione_nuovo_salvataggio = creazione_nuovo_salvataggio.get_rect(topleft=(200, 225))
            pulsante_selezione_salvataggi = selezione_salvataggi.get_rect(topleft=(200, 400))
            pulsante_uscita_salvataggio = uscita_salvataggio.get_rect(topleft=(585, 600))
        
        # Schermata della richiesta di conferma del salvataggio
        elif schermata == "conferma salvataggio":
            screen.blit(conferma_salvataggio, (175, 150))
            screen.blit(risposta_sì_salvataggio, (520, 417))
            screen.blit(risposta_no_salvataggio, (670, 417))
            
            pulsante_risposta_sì_salvataggio = risposta_sì_salvataggio.get_rect(topleft=(520, 417))
            pulsante_risposta_no_salvataggio = risposta_no_salvataggio.get_rect(topleft=(670, 417))
        
        # Schermata della selezione del salvataggio
        elif schermata == "selezione salvataggi":
            screen.blit(salvataggi_disponibili, (310, 100))
            screen.blit(uscita_selezione_salvataggi, (585, 600))
            
            pulsante_uscita_selezione_salvataggi = uscita_selezione_salvataggi.get_rect(topleft=(585, 600))
            
            salvataggi_esistenti = salvataggi.lista_salvataggi()
            
            pulsanti_salvataggi = []
            
            # Queste sono le coordinate per la tabella coi 4 salvataggi
            posizioni = [(300, 250), (700, 250), (300, 400), (700, 400)]
                
            for i in range(4):
                
                # if i < len(salvataggi_esistenti) vuol dire che controlla sei è già presente un salvataggio in quella posizione.
                if i < len(salvataggi_esistenti):
                    nome = salvataggi_esistenti[i]
                else:
                    nome = "Vuoto"

                txt = font_piccolo.render(nome, True, "white")

                x, y = posizioni[i]

                screen.blit(txt, (x, y))

                pulsanti_salvataggi.append(txt.get_rect(topleft=(x, y)))
            
        
        pygame.display.flip()
        # Questa parte del programma serve per le varie schermate: quando il videogiocatore preme un determinato tasto,
        # la variabile 'schermata' cambia valore e, in base a esso, cambia la schermata.
        # Per esempio, se premo il tasto esc (pygame.K_ESCAPE) e schermata = "menù", allora schermata diventa "uscita".
        
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                
            # Questa parte riguarda le reazioni del gioco quando premi un tasto della tastiera (l'unico tasto è esc).
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    if schermata == "menù":
                        schermata = "uscita"
                    
                    elif schermata == "uscita" or schermata == "impostazioni":
                        schermata = "menù"
                    
                    elif schermata == "volume" or schermata == "salvataggio":
                        schermata = "impostazioni"
                    
                    elif schermata == "conferma salvataggio" or schermata == "selezione salvataggi":
                        schermata = "salvataggio"
                    
                    elif gioco_effettivo == True:
                        gioco_effettivo = False
                        schermata = "menù"
            # Qua sono programmate tutte le reazioni del gioco quando premi i pulsanti.        
            if event.type == pygame.MOUSEBUTTONDOWN:

                if schermata == "menù":
                    
                    #  Qua inizia il gioco
                    if pulsante_inizio.collidepoint(mPos):
                        gioco_effettivo = True
                    
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
                    
                    if pulsante_volume.collidepoint(mPos):
                        schermata = "volume"
                    
                    elif pulsante_salvataggio.collidepoint(mPos):
                        schermata = "salvataggio"
                    
                    elif pulsante_uscita_impostazioni.collidepoint(mPos):
                        schermata = "menù"
                
                elif schermata == "volume":
                    # I pulsanti per aumentare o diminuire il volume funzionano solo se musica_attiva = True.
                    # Quando musica_attiva = False, questi non funzioneranno più perché la variabile "musica_
                    # attiva" non è nel ciclo, quindi i due pulsanti dipendono solo dal valore esterno (fisso).
                    
                    if audio_disponibile and musica_attiva:
                        if pulsante_meno_volume.collidepoint(mPos) and musica_attiva:
                            volume_musica = max(0.0, volume_musica - 0.01)
                            pygame.mixer.music.set_volume(volume_musica)
                            
                        elif pulsante_più_volume.collidepoint(mPos) and musica_attiva:
                            volume_musica = min(1.0, volume_musica + 0.01)
                            pygame.mixer.music.set_volume(volume_musica)
                                        
                    if pulsante_uscita_volume.collidepoint(mPos):
                        schermata = "impostazioni"
                    
                    elif pulsante_tasto_attivazione_musica.collidepoint(mPos):
                        musica_attiva = not musica_attiva
                        
                        if audio_disponibile:
                            if musica_attiva:
                                pygame.mixer.music.set_volume(volume_musica)
                            else:
                                pygame.mixer.music.set_volume(0.0)
                
                elif schermata == "salvataggio":
                    
                    if pulsante_creazione_nuovo_salvataggio.collidepoint(mPos):
                        schermata = "conferma salvataggio"
                    
                    elif pulsante_selezione_salvataggi.collidepoint(mPos):
                        schermata = "selezione salvataggi"
                    
                    elif pulsante_uscita_salvataggio.collidepoint(mPos):
                        schermata = "impostazioni"
                
                elif schermata == "conferma salvataggio":
                    # Quando premo ' Si ', il programma crea un percorso corrispondente al salvataggio appena fatto,
                    # il quale avrà come nome 'Salvataggio' + la lunghezza della lista salvataggi sommata a 1.
                    if pulsante_risposta_sì_salvataggio.collidepoint(mPos):
                        nomi_esistenti = salvataggi.lista_salvataggi()

                        # Hai 4 slot per i salvataggi (quando ne farai altri, li sovrascriverà al primo).
                        if len(nomi_esistenti) < 4:
                            nuovo_nome = f"Salvataggio{len(nomi_esistenti)+1}"
                        else:
                            nuovo_nome = nomi_esistenti[0]

                        salvataggi.crea_nuovo_salvataggio(nuovo_nome)

                        schermata = "salvataggio"
                    
                    if pulsante_risposta_no_salvataggio.collidepoint(mPos):
                        schermata = "salvataggio"
                
                elif schermata == "selezione salvataggi":
                    # La conferma del fatto che hai scelto un salvataggio la trovi sulla shell e non nel videogioco.
                    # enumerate è una funzione di Python che serve per scorrere sia gli elementi di una lista (nome) che i loro indici (i).
                    for i, rett in enumerate(pulsanti_salvataggi):

                        if rett.collidepoint(mPos):

                            if i < len(salvataggi_esistenti):
                                print(f"Hai selezionato il salvataggio: {salvataggi_esistenti[i]}")

                            schermata = "salvataggio"

                    
                    if pulsante_uscita_selezione_salvataggi.collidepoint(mPos):
                        schermata = "salvataggio"

#         clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
