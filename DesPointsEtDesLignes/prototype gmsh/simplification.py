
"""
Docstring for simplification
Dans cette partie , le but est de simplifier le nombre de points critiques 
dans un type de tracé .  
On va utiliser l'algorithme de Douglas-Peucker qui sert à simplifier un polygone 
ou une ligne brisée en supprimant des points.

Module de simplification des tracés.

Ce module contient l'implémentation de l'algorithme de Douglas-Peucker,
utilisé pour réduire le nombre de points d'un tracé tout en conservant
sa forme géométrique globale.
"""

from outilsGeometrie import distance_point_segment


def douglas_peucker(points, epsilon):
    """
    Simplifie un tracé à l'aide de l'algorithme de Douglas-Peucker.

    L'algorithme réduit le nombre de points en supprimant ceux dont la
    distance au segment reliant les extrémités est inférieure à un seuil
    donné, tout en conservant la forme globale du tracé.

    Paramètres
    ----------
    points : list[Point]
        Liste ordonnée de points représentant le tracé.
    epsilon : float
        Seuil de distance maximal autorisé (en pixels).

    Retour
    ------
    list[Point]
        Liste de points simplifiés.
    """
    if len(points) < 3:
        return points

    a = points[0]
    b = points[-1]

    dmax = 0.0
    index = 0

    for i in range(1, len(points) - 1):
        d = distance_point_segment(points[i], a, b)
        if d > dmax:
            dmax = d
            index = i

    if dmax > epsilon:
        left = douglas_peucker(points[:index + 1], epsilon) #sous-trace gauche
        right = douglas_peucker(points[index:], epsilon) #sous-trace droit
        return left[:-1] + right
    else:
        return [a, b]
