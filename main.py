import tkinter as tk
from tkinter import font, messagebox
from pygame import mixer
import threading
import time
import os

def on_button_click():
    label.config(text="Bonjour, " + entry.get())
    print("Bouton cliqué")

# Initialiser le module audio de pygame
mixer.init()

# Définir une variable pour suivre l'état de la musique
music_playing = False

# Chemins relatifs vers les fichiers
base_path = os.path.dirname(__file__)
alarm_sound_path = os.path.join(base_path, "alarme.mp3")
icon_path = os.path.join(base_path, "favicon.ico")

# Fonction pour jouer une sonnerie
def play_alarm():
    mixer.music.load(alarm_sound_path)
    mixer.music.play()
    time.sleep(5)  # Jouer la sonnerie pendant 5 secondes
    mixer.music.stop()


def timer_page(icon):
    # Créer une nouvelle fenêtre pour la page timer
    timer_window = tk.Toplevel()
    
    # Configurer la fenêtre de la page timer
    timer_window.title("Page Timer")
    timer_window.geometry("800x600")
    timer_window.configure(bg="gray")
    
    # Utiliser l'icône fournie pour la fenêtre de la page timer
    timer_window.iconbitmap(icon_path)
    
    # Ajouter des éléments spécifiques à la page timer
    label = tk.Label(timer_window, text="Page Timer", font=("Helvetica", 16), bg="gray")
    label.pack(pady=20)
    
    # Entrée pour définir le temps du minuteur
    time_entry = tk.Entry(timer_window, font=("Helvetica", 16))
    time_entry.pack(pady=10)
    
    # Étiquette pour afficher le temps restant
    time_label = tk.Label(timer_window, text="", font=("Helvetica", 16), bg="gray")
    time_label.pack(pady=10)
    
    # Fonction pour démarrer le minuteur
    def start_timer():
        try:
            time_in_minutes = int(time_entry.get())  # Convertir le temps entré en minutes
            time_in_seconds = time_in_minutes * 60  # Convertir les minutes en secondes
            
            # Fonction pour mettre à jour le temps restant
            def update_time():
                nonlocal time_in_seconds
                while time_in_seconds > 0:
                    minutes, seconds = divmod(time_in_seconds, 60)
                    time_label.config(text=f"Temps restant : {minutes:02d}:{seconds:02d}")
                    time.sleep(1)  # Attendre une seconde
                    time_in_seconds -= 1
                print("Temps écoulé!")
                threading.Thread(target=play_alarm).start()  # Démarrer la sonnerie dans un thread séparé
                time_label.config(text="")  # Réinitialiser l'affichage du temps restant
            
            # Démarrer la mise à jour du temps dans un thread séparé
            threading.Thread(target=update_time).start()
            
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un temps valide (nombre entier).")
    
    start_button = tk.Button(timer_window, text="Start", font=("Helvetica", 16), command=start_timer)
    start_button.pack(pady=10)
    
    # Lancer la boucle principale pour la fenêtre de la page timer
    timer_window.mainloop()


def open_music_page(icon):
    # Créer une nouvelle fenêtre pour la page musique
    music_window = tk.Toplevel()
    
    # Configurer la fenêtre de la page musique
    music_window.title("Page Musique")
    music_window.geometry("800x600")
    music_window.configure(bg="gray")
    
    # Utiliser l'icône fournie pour la fenêtre de la page musique
    music_window.iconbitmap(icon_path)
    
    # Ajouter des éléments spécifiques à la page musique
    label = tk.Label(music_window, text="Page musique", font=("Helvetica", 16), bg="gray")
    label.pack(pady=20)
    
    # Bouton "Play" pour démarrer ou arrêter la musique
    def play_music():
        global music_playing
        if music_playing:
            mixer.music.stop()
            music_playing = False
            play_button.config(text="Play lofi")
        else:
            mixer.music.load(os.path.join(base_path, "musique.mp3"))
            mixer.music.play()
            music_playing = True
            play_button.config(text="Stop")
    
    # Utiliser l'état de lecture actuel pour définir le texte du bouton
    initial_button_text = "Stop" if music_playing else "Play lofi"
    play_button = tk.Button(music_window, text=initial_button_text, font=("Helvetica", 16), command=play_music)
    play_button.pack(pady=10)
    
    # Lancer la boucle principale pour la fenêtre de la page musique
    music_window.mainloop()


# Créer la fenêtre principale
root = tk.Tk()
print("Fenêtre principale créée")

root.title("Logiciel Revision made by Tom")
root.geometry("800x600")
root.configure(bg="gray")
root.iconbitmap(icon_path)


# Création de la police Helvetica en gras
helvetica_bold = font.Font(family="Helvetica", size=24, weight="bold")
print("Police créée")

# Titre Bienvenue centré en haut
title_label = tk.Label(root, text="Time To Study", font=helvetica_bold, bg="gray")
title_label.pack(pady=20)  # Espacement de 20 pixels en bas du titre
print("Label créé")

# Création des boutons avec bord arrondi
button1 = tk.Button(root, text="Musique", font=("Helvetica", 16), relief=tk.GROOVE, borderwidth=2, command=lambda: open_music_page(icon_path))
button1.pack(pady=10)  # Espacement de 10 pixels après le bouton 1

button2 = tk.Button(root, text="Timer", font=("Helvetica", 16), relief=tk.GROOVE, borderwidth=2, command=lambda: timer_page(icon_path))
button2.pack(pady=10)  # Espacement de 10 pixels après le bouton 2

button3 = tk.Button(root, text="Fiches", font=("Helvetica", 16), relief=tk.GROOVE, borderwidth=2)
button3.pack(pady=10)  # Espacement de 10 pixels après le bouton 3

# Lancer la boucle principale
root.mainloop()
print("Boucle principale lancée")
