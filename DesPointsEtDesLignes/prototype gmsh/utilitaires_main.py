import matplotlib.pyplot as plt
from simplification import douglas_peucker
from Geometrie import Point


def simplifier_separations(seps : list[tuple[list[Point],set[int]]],epsilon : float) -> list[tuple[list[Point],set[int]]]:
    """
    seps: la liste des séparations
    epsilon: la distance maximale en pixel autorisé aux simplification 

    simplifie chaque séparation avec l'aide d'un algorithme de douglas_peucker de paramètre epsilon
    
    """
    return [(douglas_peucker(seps[x][0],epsilon),seps[x][1]) for x in range(len(seps))]
                    
def nb_points_separations(seps : list[tuple[list[Point],set[int]]]) -> int:
    """
    seps: la liste des séparations

    renvoie le nombre de points distincs présents dans la maille finale
    """
    return len(set([pt for sep in seps for pt in sep[0] ]))

def affiche_scatter(im : list[list[any]],val : any,s=2) -> None:
    """
    im : une grille d'éléments
    val : un élément
    écrit tout les points de im valant val sur la fenètre de matplotlib.pyplot avec l'aide de plt.scatter 
    """
    plt.scatter([x for y in range(len(im)) for x in range(len(im[y])) if im[y][x] == val],[-y for y in range(len(im)) for x in range(len(im[y])) if im[y][x] == val],s=s)
    
