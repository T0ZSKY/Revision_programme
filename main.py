import tkinter as tk
from tkinter import font, filedialog, messagebox, simpledialog
from pygame import mixer
import threading
import time
import os
import shutil

mixer.init()

music_playing = False

base_path = os.path.dirname(__file__) 
alarm_sound_path = os.path.join(base_path, "alarme.mp3")
icon_path = os.path.join(base_path, "favicon.ico")

def play_alarm():
    mixer.music.load(alarm_sound_path)
    mixer.music.play()
    time.sleep(5)
    mixer.music.stop()

def add_file():
    documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
    revi_by_tom_path = os.path.join(documents_path, 'revi_by_tom')
    if not os.path.exists(revi_by_tom_path):
        os.makedirs(revi_by_tom_path)
        messagebox.showinfo("Dossier créé", "Le dossier 'revi_by_tom' a été créé avec succès.")

    file_path = filedialog.askopenfilename()
    if file_path:
        cours_nom = simpledialog.askstring("Nom du cours", "Entrez le nom du cours:")
        if cours_nom:
            matiere = simpledialog.askstring("Matière", "Entrez le nom de la matière:")
            if matiere:
                matiere_path = os.path.join(revi_by_tom_path, matiere)
                if not os.path.exists(matiere_path):
                    os.makedirs(matiere_path)
                shutil.copy(file_path, os.path.join(matiere_path, cours_nom + os.path.splitext(file_path)[1]))
                messagebox.showinfo("Fichier ajouté", f"Le fichier '{cours_nom}' a été ajouté dans le dossier '{matiere}'.")
                fiches_window.destroy()

def open_cours(matiere):
    documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
    revi_by_tom_path = os.path.join(documents_path, 'revi_by_tom')
    matiere_path = os.path.join(revi_by_tom_path, matiere)
    if os.path.exists(matiere_path):
        cours_list = "\n".join(os.listdir(matiere_path))
        cours_nom = simpledialog.askstring(matiere, cours_list)
        if cours_nom:
            cours_path = os.path.join(matiere_path, cours_nom)
            if os.path.exists(cours_path):
                os.startfile(cours_path)
                fiches_window.destroy()
            else:
                messagebox.showwarning("Fichier non trouvé", f"Le fichier '{cours_nom}' n'existe pas dans le dossier '{matiere}'.")
    else:
        messagebox.showwarning("Dossier non trouvé", f"Le dossier '{matiere}' n'existe pas.")

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
    for matiere in os.listdir(os.path.join(os.path.expanduser('~'), 'Documents', 'revi_by_tom')):
        matiere_button = tk.Button(fiches_window, text=matiere, font=("Helvetica", 16), command=lambda m=matiere: open_cours(m))
        matiere_button.pack(pady=5)
    fiches_window.mainloop()

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
