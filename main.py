import tkinter as tk
from tkinter import font, filedialog, messagebox, simpledialog
from pygame import mixer
import threading
import time
import os
import shutil
import json

# Initialiser le module audio de pygame
mixer.init()

# Définir une variable pour suivre l'état de la musique
music_playing = False

# Chemins relatifs vers les fichiers
base_path = os.path.dirname(__file__)
alarm_sound_path = os.path.join(base_path, "alarme.mp3")
icon_path = os.path.join(base_path, "favicon.ico")
recent_files_path = os.path.join(base_path, "recent_files.json")

# Liste pour stocker les cours ouverts récemment
recently_opened = []

# Charger les fichiers récemment ouverts à partir du fichier JSON s'il existe
if os.path.exists(recent_files_path):
    with open(recent_files_path, 'r') as file:
        recently_opened = json.load(file)

# Fonction pour sauvegarder les fichiers récemment ouverts dans le fichier JSON
def save_recent_files():
    with open(recent_files_path, 'w') as file:
        json.dump(recently_opened, file)

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
        # Demander le nom du cours
        cours_nom = simpledialog.askstring("Nom du cours", "Entrez le nom du cours:")
        if cours_nom:
            # Demander la matière
            matiere = simpledialog.askstring("Matière", "Entrez le nom de la matière:")
            if matiere:
                # Chemin du dossier de la matière
                matiere_path = os.path.join(revi_by_tom_path, matiere)
                # Créer le dossier de la matière s'il n'existe pas
                if not os.path.exists(matiere_path):
                    os.makedirs(matiere_path)
                # Copier le fichier dans le dossier de la matière
                shutil.copy(file_path, os.path.join(matiere_path, cours_nom + os.path.splitext(file_path)[1]))
                messagebox.showinfo("Fichier ajouté", f"Le fichier '{cours_nom}' a été ajouté dans le dossier '{matiere}'.")
                fiches_window.destroy()  # Fermer la fenêtre "Fiches" après avoir ajouté un fichier

# Fonction pour lister les cours d'une matière
def lister_cours(matiere):
    # Chemin du répertoire "Documents"
    documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
    # Chemin du répertoire "revi_by_tom" dans le répertoire "Documents"
    revi_by_tom_path = os.path.join(documents_path, 'revi_by_tom')
    # Chemin du dossier de la matière
    matiere_path = os.path.join(revi_by_tom_path, matiere)
    if os.path.exists(matiere_path):
        cours_list = os.listdir(matiere_path)
        if cours_list:
            return cours_list
        else:
            messagebox.showwarning("Aucun cours trouvé", f"Aucun cours trouvé dans le dossier '{matiere}'.")
    else:
        messagebox.showwarning("Dossier non trouvé", f"Le dossier '{matiere}' n'existe pas.")

# Fonction pour ouvrir un cours
def open_cours(matiere, cours_nom):
    # Chemin du répertoire "Documents"
    documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
    # Chemin du répertoire "revi_by_tom" dans le répertoire "Documents"
    revi_by_tom_path = os.path.join(documents_path, 'revi_by_tom')
    # Chemin du dossier de la matière
    matiere_path = os.path.join(revi_by_tom_path, matiere)
    if os.path.exists(matiere_path):
        cours_path = os.path.join(matiere_path, cours_nom)
        if os.path.exists(cours_path):
            os.startfile(cours_path)
            recently_opened.insert(0, cours_nom)
            if len(recently_opened) > 3:
                recently_opened.pop()
            save_recent_files()
            update_recently_opened()
            matiere_window.destroy()  # Fermer la fenêtre qui liste les cours une fois qu'un cours est sélectionné
        else:
            messagebox.showwarning("Fichier non trouvé", f"Le fichier '{cours_nom}' n'existe pas dans le dossier '{matiere}'.")
    else:
        messagebox.showwarning("Dossier non trouvé", f"Le dossier '{matiere}' n'existe pas.")

# Fonction pour mettre à jour la section "Ouvert récemment"
def update_recently_opened():
    global recently_frame
    recently_frame.destroy()
    recently_frame = tk.Frame(fiches_window, bg="gray")
    recently_frame.pack(pady=10)

    title = tk.Label(recently_frame, text="Ouvert récemment", font=("Helvetica", 16, "bold"), bg="gray")
    title.pack(pady=5)

    for i, cours in enumerate(recently_opened):
        label = tk.Label(recently_frame, text=f"{i+1}. {cours}", font=("Helvetica", 12), bg="gray")
        label.bind("<Button-1>", lambda event, course=cours: open_recent_file(course))
        label.pack()

    fiches_window.mainloop()

# Fonction pour ouvrir la page fiches
def fiches_pages(icon):
    global fiches_window
    fiches_window = tk.Toplevel()
    
    fiches_window.title("Page Fiches")
    fiches_window.geometry("800x600")
    fiches_window.configure(bg="gray")
    
    fiches_window.iconbitmap(icon_path)
    
    label = tk.Label(fiches_window, text="Page Fiches", font=("Helvetica", 16), bg="gray")
    label.pack(pady=20)
    
    add_file_button = tk.Button(fiches_window, text="Ajouter un fichier", font=("Helvetica", 16), command=add_file)
    add_file_button.pack(pady=10)

    global recently_frame
    recently_frame = tk.Frame(fiches_window, bg="gray")
    recently_frame.pack(pady=10)

    title = tk.Label(recently_frame, text="Ouvert récemment", font=("Helvetica", 16, "bold"), bg="gray")
    title.pack(pady=5)

    for i, cours in enumerate(recently_opened):
        label = tk.Label(recently_frame, text=f"{i+1}. {cours}", font=("Helvetica", 12), bg="gray")
        label.bind("<Button-1>", lambda event, course=cours: open_recent_file(course))
        label.pack()

    for matiere in os.listdir(os.path.join(os.path.expanduser('~'), 'Documents', 'revi_by_tom')):
        matiere_button = tk.Button(fiches_window, text=matiere, font=("Helvetica", 16), command=lambda m=matiere: open_cours_list(m))
        matiere_button.pack(pady=5)

    fiches_window.mainloop()

# Fonction pour ouvrir la liste des cours d'une matière
def open_cours_list(matiere):
    cours_list = lister_cours(matiere)
    if cours_list:
        global matiere_window
        matiere_window = tk.Toplevel()
        matiere_window.title(f"Cours de {matiere}")
        matiere_window.geometry("600x400")
        matiere_window.iconbitmap(icon_path)
        
        title_label = tk.Label(matiere_window, text=f"Cours de {matiere}", font=("Helvetica", 16))
        title_label.pack(pady=20)

        for cours in cours_list:
            cours_button = tk.Button(matiere_window, text=cours, font=("Helvetica", 12), command=lambda c=cours: open_cours(matiere, c))
            cours_button.pack(pady=5)
        
    else:
        messagebox.showwarning("Aucun cours trouvé", f"Aucun cours trouvé dans le dossier '{matiere}'.")

# Fonction pour démarrer le minuteur
def start_timer():
    try:
        time_entry = simpledialog.askstring("Temps en minutes", "Entrez le temps en minutes:")
        if time_entry:
            time_in_minutes = int(time_entry)
            time_in_seconds = time_in_minutes * 60
            
            def update_time():
                nonlocal time_in_seconds
                while time_in_seconds > 0:
                    minutes, seconds = divmod(time_in_seconds, 60)
                    time_label.config(text=f"Temps restant : {minutes:02d}:{seconds:02d}")
                    time.sleep(1)
                    time_in_seconds -= 1
                print("Temps écoulé!")
                threading.Thread(target=play_alarm).start()
                time_label.config(text="")
            
            global time_label
            time_label = tk.Label(root, text="", font=("Helvetica", 16), bg="gray")
            time_label.pack(pady=10)
            
            threading.Thread(target=update_time).start()
        
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un temps valide (nombre entier).")

# Fonction pour ouvrir la page musique
def open_music_page():
    music_window = tk.Toplevel()
    
    music_window.title("Page Musique")
    music_window.geometry("800x600")
    music_window.configure(bg="gray")
    
    music_window.iconbitmap(icon_path)
    
    label = tk.Label(music_window, text="Page musique", font=("Helvetica", 16), bg="gray")
    label.pack(pady=20)
    
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
    
    initial_button_text = "Stop" if music_playing else "Play lofi"
    play_button = tk.Button(music_window, text=initial_button_text, font=("Helvetica", 16), command=play_music)
    play_button.pack(pady=10)
    
    music_window.mainloop()

# Créer la fenêtre principale
root = tk.Tk()
root.title("Logiciel Revision made by Tom")
root.geometry("800x600")
root.configure(bg="gray")
root.iconbitmap(icon_path)

helvetica_bold = font.Font(family="Helvetica", size=24, weight="bold")

title_label = tk.Label(root, text="Time To Study", font=helvetica_bold, bg="gray")
title_label.pack(pady=20)

button1 = tk.Button(root, text="Musique", font=("Helvetica", 16), relief=tk.GROOVE, borderwidth=2, command=open_music_page)
button1.pack(pady=10)

button2 = tk.Button(root, text="Timer", font=("Helvetica", 16), relief=tk.GROOVE, borderwidth=2, command=start_timer)
button2.pack(pady=10)

button3 = tk.Button(root, text="Fiches", font=("Helvetica", 16), relief=tk.GROOVE, borderwidth=2, command=lambda: fiches_pages(icon_path))
button3.pack(pady=10)

root.mainloop()
