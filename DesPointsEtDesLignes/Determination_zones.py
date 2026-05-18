## Importations
import sys
from collections import deque
import matplotlib.pyplot as plt

def affiche_scatter(im,val,s=2):
    plt.scatter([x for y in range(len(im)) for x in range(len(im[y])) if im[y][x] == val],[-y for y in range(len(im)) for x in range(len(im[y])) if im[y][x] == val],s=s)
    


## Implementation de notre algorithme de determination des zones (parcours en largeur itératif) :
def parcours_zones(zones : list[list[int]], image : list[list[bool]], i : int, j : int, k : int) -> tuple[ int, list[int] ] :
    """
    effectue un parcours en largeur d une zone blanche, numerotee k, a partir du noeud (x,y).

    """
    # Extraction de la taille de l'image :
    n1 = len(image)
    assert (n1 > 0)
    n2 = len(image[0])

    # Parcours en largeur de la zone
    t = 0
    dq = deque()
    dq.append((i,j))
    while dq :
        x,y = dq.popleft()
        for (dx,dy) in [(1,0),(-1,0),(0,1),(0,-1)]:
            newx,newy = x+dx,y+dy
            if newx>=0 and newy>=0 and newx < n1 and newy < n2 and image[newx][newy] and zones[newx][newy] != k:
                dq.append((newx,newy))
                zones[newx][newy] = k
        t += 1
    return t


def zones_depuis_image(image : list[list[bool]], seuil = 0) -> list[list[int]] :
    """
    renvoie un tableau des zones blanches, numerotees par 1 a la bordure, et 2... au centre. Ainsi que le nombre total de zone blanche.
    """
    # Extraction de la taille de l'image :
    n1 = len(image)
    assert (n1 > 0)
    n2 = len(image[0])
    # Initialisation de l'algorithme :
    zones = [[-1 for j in range(n2)] for i in range(n1)]

    # Iteration de l'algorithme :
    # au niveau de la bordure :
    bordure = []
    bordure.extend([(0,j) for j in range(n2)])
    bordure.extend([(i,0) for i in range(1,n1)])
    bordure.extend([(n1-1,j) for j in range(1,n2)])
    bordure.extend([(i,n2-1) for i in range(1,n1-1)])
    for i,j in bordure :
        if (image[i][j] and zones[i][j] == -1) :
            taille = parcours_zones(zones,image,i,j,1)
            if taille <= seuil :
                parcours_zones(zones,image,i,j,0)

    # a l'interieur :
    nb_zones = 1
    for i in range(1,n1-1):
        for j in range(1,n2-1):
            if (image[i][j] and zones[i][j] == -1) :
                nb_zones += 1
                taille = parcours_zones(zones,image,i,j,nb_zones)
                if taille <= seuil :
                    t = parcours_zones(zones,image,i,j,0)
    
    for i in range(0,n1):
        for j in range(0,n2):
            if zones[i][j] == -1:
                zones[i][j] = 0

    return zones


sys.setrecursionlimit(5000000)

