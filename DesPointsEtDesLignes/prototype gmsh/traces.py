

""" Dans un 1er temps , définissons les différents types de tracés . 
"""
""" La classe mère , 
Entrée : Numéro des 2 zones , point du début et de la fin 

"""
import math
from outilsGeometrie import distance_point_segment

class Trace:
    def __init__(self, zone1, zone2, p_start, p_end):
        self.zone1 = zone1
        self.zone2 = zone2
        self.p_start = p_start
        self.p_end = p_end

    #@abstractmethod
    def erreur(self, points):
        """
         Calcule l'erreur d'approximation du tracé par rapport aux points
        issus de l'image.
        L'erreur est définie comme la distance maximale entre les points
        du tracé réel et le modèle géométrique représenté par l'objet.
        Docstring for erreur
        
        :param self: Description
        :param points: Liste de points du tracé extrait de l’image.
        """
        raise NotImplementedError

    def export_gmsh(self):
        raise NotImplementedError
    
    def get_points(self):
        """
        Retourne la liste des points nécessaires à l'export Gmsh.
        """
        raise NotImplementedError

# un point 

#Ligne droite 
class Ligne(Trace):
    def __init__(self, zone1, zone2, p_start, p_end):
        super().__init__(zone1, zone2, p_start, p_end)
    
    def erreur(self, points):
        x1, y1 = self.p_start.x, self.p_start.y
        x2, y2 = self.p_end.x, self.p_end.y

        dx = x2 - x1
        dy = y2 - y1
        norm = math.hypot(dx, dy)

        if norm == 0:
            return float("inf")

        erreur_max = 0.0

        for p in points:
            num = abs(dy * p.x - dx * p.y + x2*y1 - y2*x1)
            d = num / norm
            erreur_max = max(erreur_max, d)

        return erreur_max

    def export_gmsh(self, ctx):
        """
        Exporte une ligne droite au format Gmsh.

        Paramètres
        ----------
        ctx : GmshContext
            Contexte global d'export Gmsh.

        Retour
        ------
        str
            Code Gmsh correspondant à la ligne.
        """
        p1 = ctx.get_point_id(self.p_start)
        p2 = ctx.get_point_id(self.p_end)
        cid = ctx.get_curve_id()

        return f"Line({cid}) = {{{p1}, {p2}}};\n"

    def get_points(self):
        return [self.p_start, self.p_end]

# Arc de cercle 
class ArcCercle(Trace):
    def __init__(self, zone1, zone2, centre, rayon, angle_debut, angle_fin):
        self.zone1 = zone1
        self.zone2 = zone2
        self.centre = centre
        self.rayon = rayon
        self.angle_debut = angle_debut
        self.angle_fin = angle_fin

    def erreur(self, points):
        cx, cy = self.centre.x, self.centre.y

        erreur_max = 0.0

        for p in points:
            d = math.hypot(p.x - cx, p.y - cy)
            erreur = abs(d - self.rayon)
            erreur_max = max(erreur_max, erreur)

        return erreur_max
    
    def export_gmsh(self, ctx):
        """
        Exporte un arc de cercle au format Gmsh.

        Paramètres
        ----------
        ctx : GmshContext
            Contexte global d'export Gmsh.

        Retour
        ------
        str
            Code Gmsh correspondant à l'arc de cercle.
        """
        p1 = ctx.get_point_id(self.p_start)
        pc = ctx.get_point_id(self.centre)
        p2 = ctx.get_point_id(self.p_end)
        cid = ctx.get_curve_id()

        return f"Circle({cid}) = {{{p1}, {pc}, {p2}}};\n"

    def get_points(self):
        return [self.p_start, self.centre, self.p_end]
# Courbe 
"""Une courbe n est pas définie par tous ses points, 
mais par quelques points de contrôle qui pilotent sa forme.
points_controle : liste de points 
"""
class Courbe(Trace):
    def __init__(self, zone1, zone2, points_controle):
        self.zone1 = zone1
        self.zone2 = zone2
        self.points_controle = points_controle
        self.p_start = points_controle[0]
        self.p_end = points_controle[-1]

    def erreur(self, points):
        erreur_max = 0.0

        for p in points:
            d_min = float("inf")
            for i in range(len(self.points_controle) - 1):
                a = self.points_controle[i]
                b = self.points_controle[i + 1]
                d = distance_point_segment(p, a, b)
                d_min = min(d_min, d)

            erreur_max = max(erreur_max, d_min)

        return erreur_max
    
    def export_gmsh(self, ctx):
        """
        Exporte une courbe libre (spline) au format Gmsh.

        Paramètres
        ----------
        ctx : GmshContext
            Contexte global d'export Gmsh.

        Retour
        ------
        str
            Code Gmsh correspondant à la spline.
        """
        point_ids = [
            ctx.get_point_id(p) for p in self.points_controle
        ]
        cid = ctx.get_curve_id()

        points_str = ", ".join(map(str, point_ids))
        return f"Spline({cid}) = {{{points_str}}};\n"
    
    def get_points(self):
        return self.points_controle