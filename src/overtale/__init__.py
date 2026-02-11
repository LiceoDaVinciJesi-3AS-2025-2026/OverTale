def main() -> None:
    import pygame
    
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("OverTale")
    
    font_grande = pygame.font.SysFont('Minecraft', 100)
    font_piccolo = pygame.font.SysFont('Minecraft', 67)
    
    # Questi sono tutti i titoli e le scritte (sono da finire).
    titolo = font_grande.render("OverTale", True, "white")
    uscita = font_grande.render("Vuoi uscire dal gioco?", True, "white")
    inizio = font_piccolo.render("Start", True, "white")

    clock = pygame.time.Clock()
    running = True
    
        running = True
    while running:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                screen.fill("black")
                # Devo mettere la richiesta di uscire sia su questo che su quello sotto.
                
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    pygame.quit()
