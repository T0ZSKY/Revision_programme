import tkinter as tk
from tkinter import font


def on_button_click():
    label.config(text="Bonjour, " + entry.get())
    print("Bouton cliqué")

def open_music_page():
    # Créer une nouvelle fenêtre pour la page musique
    music_window = tk.Tk()
    
    # Configurer la fenêtre de la page musique
    music_window.title("Page Musique")
    music_window.geometry("800x600")
    music_window.configure(bg="gray")
    
    # Ajouter des éléments spécifiques à la page musique
    label = tk.Label(music_window, text="Page musique", font=("Helvetica", 16), bg="gray")
    label.pack(pady=20)
    
    # Initialiser le module audio de pygame
    mixer.init()
    
    # Bouton "Play" pour démarrer la musique
    def play_music():
        mixer.music.load("D:/logiciel_revision/musique.mp3")  # Charger le fichier audio
        mixer.music.play()  # Jouer la musique
    
    play_button = tk.Button(music_window, text="Play", font=("Helvetica", 16), command=play_music)
    play_button.pack(pady=10)
    
    # Lancer la boucle principale pour la fenêtre de la page musique
    music_window.mainloop()


# Créer la fenêtre principale
root = tk.Tk()
print("Fenêtre créée")

root.title("Logiciel Revision made by Tom")
root.geometry("800x600")
root.configure(bg="gray")

# Changer l'icône de la fenêtre
root.iconbitmap("D:/logiciel_revision/school.ico")

# Création de la police Helvetica en gras
helvetica_bold = font.Font(family="Helvetica", size=24, weight="bold")
print("Police créée")

# Titre Bienvenue centré en haut
title_label = tk.Label(root, text="Time To Study", font=helvetica_bold, bg="gray")
title_label.pack(pady=20)  # Espacement de 20 pixels en bas du titre
print("Label créé")

# Création des boutons avec bord arrondi
button1 = tk.Button(root, text="Musique", font=("Helvetica", 16), relief=tk.GROOVE, borderwidth=2, command=open_music_page)
button1.pack(pady=10)  # Espacement de 10 pixels après le bouton 1

button2 = tk.Button(root, text="Timer", font=("Helvetica", 16), relief=tk.GROOVE, borderwidth=2)
button2.pack(pady=10)  # Espacement de 10 pixels après le bouton 2

button3 = tk.Button(root, text="Fiches", font=("Helvetica", 16), relief=tk.GROOVE, borderwidth=2)
button3.pack(pady=10)  # Espacement de 10 pixels après le bouton 3

# Lancer la boucle principale
root.mainloop()
print("Boucle principale lancée")
