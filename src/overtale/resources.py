# Librerie pip
from importlib.resources import files
from pathlib import Path

# eventualmente aggiungere tutte le funzioni relative alle cartelle che avete creato in src.
def get_sound(filename: str) -> Path:
    return files(__package__) / "sounds" / filename

def get_image(filename: str):
    return files(__package__) / "images" / filename

# resources.py - gestione dei files nel gioco

# In questo file sono presenti le funzioni per la gestione e l'utilizzo di files come le immagini e le musiche nei codici.

# License: See LICENSE file in the project root for details.

# Authors: 
# Manuel Canonici <manuelcanonici09@gmail.com>
# Massimo Di Gaspare <massimo.digaspare09@gmail.com>
# Alessandro Meschini <ale.meschini5@gmail.com>
