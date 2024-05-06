import tkinter as tk
from tkinter import font, filedialog, messagebox, simpledialog
from pygame import mixer
import threading
import time
import os
import shutil

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

# Fonction pour ajouter un fichier
def add_file():
    # Chemin du répertoire "Documents"
    documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
    
    # Chemin du répertoire "revi_by_tom" dans le répertoire "Documents"
    revi_by_tom_path = os.path.join(documents_path, 'revi_by_tom')
    
    # Vérifier si le répertoire "revi_by_tom" existe, sinon le créer
    if not os.path.exists(revi_by_tom_path):
        os.makedirs(revi_by_tom_path)
        messagebox.showinfo("Dossier créé", "Le dossier 'revi_by_tom' a été créé avec succès.")

    # Maintenant, nous pouvons procéder à la sélection du fichier
    file_path = filedialog.askopenfilename()
    if file_path:
        # Demander le nom de la matière
        matiere = simpledialog.askstring("Nom de la matière", "Entrez le nom de la matière :")
        if matiere:
            # Chemin du dossier de la matière
            matiere_path = os.path.join(revi_by_tom_path, matiere)
            # Vérifier si le dossier de la matière existe, sinon le créer
            if not os.path.exists(matiere_path):
                os.makedirs(matiere_path)
                messagebox.showinfo("Dossier créé", f"Le dossier '{matiere}' a été créé avec succès.")
            # Demander le nom du cours
            cours_nom = simpledialog.askstring("Nom du cours", "Entrez le nom du cours :")
            if cours_nom:
                # Copier le fichier dans le dossier de la matière avec le nom du cours
                file_name = os.path.basename(file_path)
                destination_path = os.path.join(matiere_path, cours_nom + os.path.splitext(file_name)[1])
                shutil.copy(file_path, destination_path)
                messagebox.showinfo("Fichier ajouté", f"Le fichier a été ajouté dans le dossier '{matiere}'.")
            else:
                messagebox.showwarning("Nom du cours non spécifié", "Vous devez spécifier un nom de cours.")
        else:
            messagebox.showwarning("Matière non spécifiée", "Vous devez spécifier un nom de matière.")

def fiches_pages(icon):
    # Créer une nouvelle fenêtre pour la page fiches
    fiches_window = tk.Toplevel()
    
    # Configurer la fenêtre de la page fiches
    fiches_window.title("Page Fiches")
    fiches_window.geometry("800x600")
    fiches_window.configure(bg="gray")
    
    # Utiliser l'icône fournie pour la fenêtre de la page fiches
    fiches_window.iconbitmap(icon_path)
    
    # Ajouter des éléments spécifiques à la page fiches
    label = tk.Label(fiches_window, text="Page Fiches", font=("Helvetica", 16), bg="gray")
    label.pack(pady=20)
    
    # Bouton pour ajouter un fichier
    add_file_button = tk.Button(fiches_window, text="Ajouter un fichier", font=("Helvetica", 16), command=add_file)
    add_file_button.pack(pady=10)
    
    # Lancer la boucle principale pour la fenêtre de la page fiches
    fiches_window.mainloop()

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

# Fonction pour ouvrir la page musique
def open_music_page():
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
root.title("Logiciel Revision made by Tom")
root.geometry("800x600")
root.configure(bg="gray")
root.iconbitmap(icon_path)

# Création de la police Helvetica en gras
helvetica_bold = font.Font(family="Helvetica", size=24, weight="bold")

# Titre Bienvenue centré en haut
title_label = tk.Label(root, text="Time To Study", font=helvetica_bold, bg="gray")
title_label.pack(pady=20)  # Espacement de 20 pixels en bas du titre

# Création des boutons avec bord arrondi
button1 = tk.Button(root, text="Musique", font=("Helvetica", 16), relief=tk.GROOVE, borderwidth=2, command=open_music_page)
button1.pack(pady=10)  # Espacement de 10 pixels après le bouton 1

button2 = tk.Button(root, text="Timer", font=("Helvetica", 16), relief=tk.GROOVE, borderwidth=2, command=start_timer)
button2.pack(pady=10)  # Espacement de 10 pixels après le bouton 2

button3 = tk.Button(root, text="Fiches", font=("Helvetica", 16), relief=tk.GROOVE, borderwidth=2, command=lambda: fiches_pages(icon_path))
button3.pack(pady=10)  # Espacement de 10 pixels après le bouton 3

# Lancer la boucle principale
root.mainloop()
