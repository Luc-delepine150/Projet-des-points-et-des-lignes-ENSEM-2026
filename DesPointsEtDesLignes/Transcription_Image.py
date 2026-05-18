## Importations
import matplotlib.image as mpimg
import numpy as np

## Recuperation d'une image

def transcription_image(nom_fichier,seuil_gris = 127)->list[list[bool]] :

    # Lecture du fichier contenant l'image :
    img = mpimg.imread(nom_fichier)
    if img.dtype == np.float32: # Si le résultat n'est pas un tableau d'entiers
        img = (img * 255).astype(np.uint8)
    img = img[:,:,:3]
    d1,d2,d3 = img.shape

    # Convertir l'image sous la forme voulue :
    image = [[True for j in range(d2)] for i in range(d1)]
    for i in range(d1):
        for j in range(d2):
            r,v,b = img[i,j,0], img[i,j,1], img[i,j,2]
            gris = int(0.2126*r+0.7152*v+0.0722*b)
            if gris <= seuil_gris :
                image[i][j] = False

    return image

def etendre(image):
    long = len(image)
    larg = len(image[0])
    new = [ligne.copy() for ligne in image]
    for x in range(long):
        for y in range(larg):
            if image[x][y]:
                for (dx,dy) in [(1,0),(0,1),(-1,0),(0,-1)]:
                    newx,newy = x+dx,y+dy
                    if (newx >= 0 and newx< long and newy >= 0 and newy < larg):
                        voisin_noir = not image[newx][newy]
                    
                    if voisin_noir:
                        new[x][y] = False
    return new
