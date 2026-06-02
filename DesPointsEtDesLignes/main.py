import tkinter as tk
from tkinter import messagebox
import os
import matplotlib.pyplot as plt
from gmsh_export import exportAllGmsh
from Transcription_Image import transcription_image,etendre
from Determination_zones import zones_depuis_image
from get_separations import get_separations
from utilitaires_main import simplifier_separations,nb_points_separations,affiche_scatter
from traces import Ligne
import cycles as cyc
import Geometrie as geom

def run_program(image_path : str, gmsh_path : str, seuil_gris : int, extention_tracee : int, taille_min_zone : int, epsilon : float):
    """
    image_path  le chemin vers l'image à transformer en maillage
    gmsh_path   le chemin du fichier où écrire le maillage final
    seuil_gris  le seuil de niveau de gris sur l'image de départ séparent les pixels noir et les pixels blancs
    extention_tracee   les zones de pixels noir seront épaissit de extention_tracee pixels
    taille_min_zone    la taille minimale que dois avoir une zone pour être enregistré
    epsilon     distance maximal autorisé entre les pixels des limites brutes et les segments des limites simplifiées
    
    traduit l'image à la position image_path en un maillage .geo à la position gmsh_path
    en utilisant la méthode aire
    """
    print("=== PARAMÈTRES ===")
    print("Image :", image_path)
    print("Fichier gmsh :", gmsh_path)
    print("Seuil de gris :", seuil_gris)
    print("Taille min zone :", taille_min_zone)
    print("Epsilon :", epsilon)

    image1 : list[list[bool]] = transcription_image(image_path,seuil_gris) 

    for _ in range(extention_tracee):
        image1 = etendre(image1)
    
    
    zones1 = zones_depuis_image(image1, seuil=taille_min_zone)
    n = max(map(max,zones1))
    
    
    separations1,bonus = get_separations(zones1)
    lsty = [-pt.x for pt in bonus]
    lstx = [pt.y for pt in bonus]
    simple_separations1 = simplifier_separations(separations1,epsilon)
    plt.title("avec "+str(nb_points_separations(simple_separations1))+" points (epsilon="+str(epsilon)+")")

    for separation in simple_separations1:
        plt.plot([pt.y for pt in separation[0]],[-pt.x for pt in separation[0]])
    
    plt.scatter(lstx,lsty, s=16)
    plt.show()

    traces = []
    for separation in simple_separations1:
        zones = list(separation[1])
        for x in range(len(separation[0])-1):
            traces.append(Ligne(zones[0], zones[-1], separation[0][x], separation[0][x+1]))
    
    gmsh_code = exportAllGmsh(traces)

    with open(gmsh_path, "w") as f:
        f.write(gmsh_code)

    print("Programme exécuté !")

def lancer():
    """
    lance la traduction de l'image avec la méthode aire avec les paramètre rentré dans l'interface tkinter
    affiche des messages d'erreurs lorsque les chemins de fichiers n'existent pas
    """
    try:
        image_path = entry_image.get()
        gmsh_path = entry_gmsh.get()
        seuil_gris = int(entry_seuil.get())
        extention_tracee = int(entry_extention_tracee.get())
        taille_min = int(entry_taille.get())
        epsilon = float(entry_epsilon.get())

        if not os.path.exists(image_path):
            messagebox.showerror("Erreur", "L'image n'existe pas.")
            return

        run_program(image_path, gmsh_path, seuil_gris, extention_tracee, taille_min, epsilon)

        messagebox.showinfo("Succès", "Le modèle Gmsh a été généré !")

    except ValueError:
        messagebox.showerror("Erreur", "Vérifie les paramètres numériques.")

def lancer_cycles():
  sommets,mat_adj=cyc.run(entry_image.get())
  sommets=[geom.Point(pt.x,pt.y) for pt in sommets]
  traces=[]
  for i in range(len(mat_adj)):
    for j in range(len(mat_adj)):
      if mat_adj[i][j]:
        traces.append(Ligne(None,None,sommets[i],sommets[j]))

  gmsh_code = exportAllGmsh(traces)
  
  with open(entry_gmsh.get(), "w") as f:
      f.write(gmsh_code)
  
  print("Programme exécuté !")



def set_method():
  global method,method_win
  for slave in method_win.grid_slaves():slave.destroy()
  if method=='areas':
    
    #Methode
    tk.Label(method_win,text='Méthode actuelle : aires').grid(row=0,column=0,columnspan=2)
      
    # Seuil de gris
    tk.Label(method_win, text="Seuil de gris :").grid(row=1,column=0)
    global entry_seuil
    entry_seuil = tk.Entry(method_win)
    entry_seuil.grid(row=1,column=1)
    
    # Seuil de gris
    tk.Label(method_win, text="Extention du tracée :").grid(row=2,column=0)
    global entry_extention_tracee
    entry_extention_tracee = tk.Entry(method_win)
    entry_extention_tracee.grid(row=2,column=1)
    
    # Taille minimale zone
    tk.Label(method_win, text="Taille minimale d'une zone :").grid(row=3,column=0)
    global entry_taille
    entry_taille = tk.Entry(method_win)
    entry_taille.grid(row=3,column=1)
    
    # Epsilon (Douglas-Peucker)
    tk.Label(method_win, text="Epsilon:").grid(row=4,column=0)
    global entry_epsilon
    entry_epsilon = tk.Entry(method_win)
    entry_epsilon.grid(row=4,column=1)
    
    run_but.config(command=lancer)
    
    method='cycles'
    
  else:
    
    #Methode
    tk.Label(method_win,text='Méthode actuelle : cycles').grid(row=0,column=0,columnspan=2)
    
    run_but.config(command=lancer_cycles)
    
    method='areas'
        

# ======================
# INTERFACE
# ======================


root = tk.Tk()
root.title("Projet points et lignes ")
root.geometry("500x400")

# Image
tk.Label(root, text="Adresse de l'image :").grid(row=1,column=0)
entry_image = tk.Entry(root, width=60)
entry_image.grid(row=2,column=0)
# Fichier gmsh
tk.Label(root, text="Adresse + nom du fichier Gmsh (.geo) :").grid(row=3,column=0)
entry_gmsh = tk.Entry(root, width=60)
entry_gmsh.grid(row=4,column=0)

# Fenêtre méthode
method_win=tk.Frame(root)
method_win.grid(row=5,column=0)

# Bouton méthode
tk.Button(root,text='Changer méthode',command=set_method).grid(row=6,column=0)

# Bouton lancer
run_but=tk.Button(root, text="Lancer le programme", command=lancer, bg="green", fg="white")
run_but.grid(row=7,column=0)


method='areas'
set_method()



root.mainloop()
