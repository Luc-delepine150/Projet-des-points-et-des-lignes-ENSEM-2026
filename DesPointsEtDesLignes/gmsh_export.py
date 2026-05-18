
"""
Module d'export global vers le format Gmsh.
"""
from traces import Trace,Ligne,ArcCercle,Courbe

class GmshContext:
    """
    Contexte global d'export Gmsh.

    Gère les identifiants des points et des courbes
    afin d'assurer l'unicité des entités Gmsh.
    """
    def __init__(self):
        self.next_point_id = 1
        self.next_curve_id = 1
        self.point_ids = {}

    def get_point_id(self, p):
        """
        Retourne l'identifiant Gmsh associé à un point,
        en le créant si nécessaire.
        """
        if p not in self.point_ids:
            self.point_ids[p] = self.next_point_id
            self.next_point_id += 1
        return self.point_ids[p]

    def get_curve_id(self):
        """
        Retourne un nouvel identifiant Gmsh pour une courbe.
        """
        cid = self.next_curve_id
        self.next_curve_id += 1
        return cid

def exportAllGmsh(traces):
    """
    Exporte l'ensemble des tracés géométriques vers du code Gmsh.

    Paramètres
    ----------
    traces : list[Trace]
        Liste des tracés géométriques représentant les séparations.

    Retour
    ------
    str
        Code Gmsh complet correspondant à l'ensemble des tracés.
    """
    ctx = GmshContext()

    code_curves = ""

    # 1) Forcer l'enregistrement de tous les points
    for trace in traces:
        for p in trace.get_points():
            ctx.get_point_id(p)

    # 2) Exporter les points UNE SEULE FOIS
    code_points = ""
    for p, pid in ctx.point_ids.items():
        code_points += f"Point({pid}) = {{{p.x}, {p.y}, 0}};\n"

    # 3) Exporter les courbes
    for trace in traces:
        code_curves += trace.export_gmsh(ctx)

    return code_points + "\n" + code_curves


