# Funzioni varie

import pygame

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.play(-1)  # -1 = loop infinito

def set_volume(livello):
    """
    Imposta il volume della musica.
    livello: valore tra 0.0 e 1.0
    """
    if 0.0 <= livello <= 1.0:
        pygame.mixer.music.set_volume(livello)
    else:
        print("Errore: il volume deve essere tra 0.0 e 1.0")

volume_attuale = 1.0
audio_attivo = True

def toggle_audio():
    global audio_attivo, volume_attuale
    
    if audio_attivo:
        # Salviamo il volume corrente
        volume_attuale = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(0.0)
        audio_attivo = False
    else:
        pygame.mixer.music.set_volume(volume_attuale)
        audio_attivo = True
