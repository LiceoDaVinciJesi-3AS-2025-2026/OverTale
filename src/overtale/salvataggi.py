# Librerie Standard
from pathlib import Path

# Librerie pip
from platformdirs import user_data_dir

# 1° funzione.
def percorso_salvataggi() -> Path:
    """ Questa funzione restituisce una variabile 'Path' che rappresenta la cartella dei salvataggi del videogiocatore. """
    
    cartella = Path(user_data_dir("OverTale", "TuoNome"))
    cartella.mkdir(parents=True, exist_ok=True)
    
    return cartella

# 2° funzione
def crea_nuovo_salvataggio(nome_file: str, dati: str = "Nuovo salvataggio") -> Path:
    """ Questa funzione prende due variabili "nome_file" e "dati" come parametri e ritorna il percorso corrispondente al nuovo salvataggio. """
    
    cartella = percorso_salvataggi()
    file_salvataggio = cartella / f"{nome_file}.txt"
    
    # Si può dedurre chi abbia consigliato questa scrittura per un file.
    with file_salvataggio.open("w", encoding="utf-8") as f:
        f.write(dati)
        
        f.close()
    
    return file_salvataggio

# 3° funzione
def lista_salvataggi() -> list[str]:
    """ Questa funzione ritorna la lista con tutti le stringhe dei salvataggi. """
    
    cartella = percorso_salvataggi()
    
    return [f.stem for f in cartella.glob("*.txt")]

# salvataggi.py - impostazioni di salvataggio del gioco

# In questo file sono contenute tutte le funzioni per la creazione e gestione dei salvataggi.
# L'abbiamo creato perché ci era stato richiesto di utilizzare i percorsi e la gestione dei files,
# anche se non ce n'è alcun bisogno vista la breve durata del nostro gioco.

# License: See LICENSE file in the project root for details.

# Authors: 
# Massimo Di Gaspare <massimo.digaspare09@gmail.com>
