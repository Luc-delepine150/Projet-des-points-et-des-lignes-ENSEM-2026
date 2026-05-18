from Geometrie import Point


class TasMin():
    """
    classe modélisant un tas min 

    cf
    https://fr.wikipedia.org/wiki/Tas_binaire
    """

    def __init__(self,evaluator):
        """
        initialise un tas min vide avec evaluator
        comme évaluateur des valeurs de ses éléments
        """
        self.tas = []
        self.len = 0
        self.eval = evaluator

    def is_empty(self):
        """
        renvoi True si self est vide , False sinon
        """
        return self.len == 0
    
    def remonter(self,id):
        """
        implémentation de la monté d'un élément (percolation vers le haut)
        
        cf
        https://fr.wikipedia.org/wiki/Tas_binaire
        """
        if id >0:
            racine = (id-1)//2
            if self.eval(self.tas[racine]) > self.eval(self.tas[id]):
                self.tas[racine],self.tas[id] = self.tas[id],self.tas[racine]
                self.remonter(racine)

    def descendre(self,id):
        """
        implémentation de la descente d'un élément (percolation vers le bas)
        
        cf
        https://fr.wikipedia.org/wiki/Tas_binaire
        """
        if id*2+1 < self.len:
            

            if id*2+1 == self.len -1:
                filsmin = id*2+1
            else:
                filsg = id*2+1
                filsd = id*2+2
                if self.eval(self.tas[filsg]) < self.eval(self.tas[filsd]):
                    filsmin = filsg
                else:
                    filsmin = filsd
            if self.eval(self.tas[filsmin]) < self.eval(self.tas[id]):
                self.tas[id], self.tas[filsmin] = self.tas[filsmin], self.tas[id]
                self.descendre(filsmin)



    def append(self,obj):
        """
        ajoute obj à self
        """
        self.len += 1
        self.tas.append(obj)
        self.remonter(self.len-1)
    
    def pop(self):
        """
        retire et renvoie l'élément de self avec la plus faible valeur
        """
        if self.len < 1:
            raise IndexError
        else:
            self.len -= 1
            self.tas[0],self.tas[self.len] = self.tas[self.len], self.tas[0]
            retour = self.tas.pop()
            self.descendre(0)
            return retour



def get_separations(e_zones : list[list[int]]) -> list[tuple[list[Point],set[int]]]:
    """
    e_zones : le numéro de zone de chaque pixel de l'image 
    nbzones : le nombre de zones différentes de l'image
    
    détermine les limites de rattachement des zones (= les séparations) par propagation des zones 
    puis renvoie la listes des séparation.
    
    format :
    sortie : list[separation]
        separation : tuple[liste_points,zones_séparés]
            liste_points : la liste ordonnée des points formant cette séparation 
            zones_séparés : un set des 2 zones que sépare cette séparation

    """
    zones : list[list[int]] = e_zones.copy()
    
    points = []
    rattachements = []
    id_points = {}
    prioritee = TasMin((lambda x : x[0].dist_squared(x[1])))

    for x in range(len(zones)):
        for y in range(len(zones[0])):
            if zones[x][y] != 0:
                
                prioritee.append((Point(x,y),Point(x,y)))
    

    """
    principe du code de la propagation des zones :

    propagation des zones via une méthode inspiré de l'algorithme de Dijkstra

    on utilise un tasMin pour propager où chaque élément est un tuple (point_d'origine, point_à_visitee)
    et où la valeur de ses élément est la distance entre le point_d'origine et le point_à_visitee

    à chaque itération de la boucle on regarde si le point que l'on visite a déjà été visitée auparavant,
    
     si ce n'est pas le cas , 
        on rajoute ses voisins orthogonaux et diagonaux non visitées à la file de priorité (le tasMin) avec le même point de départ
        puis on le marque comme visité 
    
     si le point à déjà été visité:
        on retient ce point comme un point d'une séparation (un point limite)
        en l'ajoutant à un dictionnaire {cle = id_point : val = set(numéro des zones séparées par ce point)}  (ici rattachements)

    en pratique le programe est un peut plus sofistique pour pour réduire son temps de calcul (sa complexité)
    """ 

    while not prioritee.is_empty():
        curr_debut,curr_fin = prioritee.pop()
        if curr_fin in id_points:
            rattachements[id_points[curr_fin]].add(zones[curr_debut.x][curr_debut.y])

        else:
            for (dx,dy) in [(1,-1),(1,0),(1,1),(0,-1),(0,1),(-1,-1),(-1,0),(-1,1)]:

                new_fin = curr_fin+Point(dx,dy)

                if new_fin.x >= 0 and new_fin.x < len(zones) and new_fin.y >= 0 and new_fin.y < len(zones[0]):

                    if zones[new_fin.x][new_fin.y] ==0:
                        zones[new_fin.x][new_fin.y] = zones[curr_debut.x][curr_debut.y]
                        prioritee.append((curr_debut,Point(new_fin.x,new_fin.y)))

                    elif zones[new_fin.x][new_fin.y] != zones[curr_debut.x][curr_debut.y]:
                        if (new_fin) in id_points:
                            rattachements[id_points[new_fin]].add(zones[curr_debut.x][curr_debut.y])

                        else:
                            id_points[new_fin] = len(points)
                            points.append(new_fin)
                            rattachements.append(set([zones[curr_debut.x][curr_debut.y]]))
    
    """
    dans un second temps on identifit les "points critiques", ce sont les point séparent 3 zones ou plus (= les pixels qui seraient réellement identifiés comme des points du tracé par un humain)
    """
    points_critiques = [pt for pt in range(len(rattachements)) if len(rattachements[pt]) > 2]

    """
    puis on les utilise pour déterminer les séparations:
        pour chaque séparation il faut identifier quels sont les points qui la compose,
        l'ordre de ces points et les 2 zones que sépare cette séparation


    dû à notre méthode de propagation, chaque point d'une séparation à part ses 2 point critiques
    est voisin orthogonalement d'exactement 2 autre point de cette séparation
    et la séparation est orthogonalement connexe 


    donc on détermine les séparation par des parcours des points limites de proche en proche délimités par les points critiques
    """
    separations : list[tuple[list[any],dict[int]]] = []
    for critique in points_critiques:
        pile = [(critique,None)]
        del id_points[points[critique]]

        while pile != []:
            curr = pile.pop()
            pt = curr[0]

            for dx,dy in [(1,0),(0,-1),(0,1),(-1,0)]:
                new_pt = points[pt] + Point(dx,dy)

                if new_pt in id_points:
                    new_pt_id = id_points[new_pt]

                    if  len(rattachements[new_pt_id]) > 2:
                        separations.append( ( (new_pt_id,curr), ((rattachements[pt].copy())&(rattachements[new_pt_id].copy())) ) )

                    else:
                        pile.append((new_pt_id,curr))
                        del id_points[new_pt]

    #ici on gère les limites ne contenant aucun point critique
    while id_points != {}:
        pointdepart,id_pointdepart = id_points.popitem()
        pile = [(id_pointdepart,None)]

        while pile != []:
            curr = pile.pop()
            pt = curr[0]
            pt_exploree_id = None

            for dx,dy in [(1,0),(0,-1),(0,1),(-1,0)]:
                new_pt = points[pt] + Point(dx,dy)
                if new_pt in id_points:
                    pt_exploree_id = id_points[new_pt]

            if  pt_exploree_id == None:

                separations.append( ( (id_pointdepart,curr), (rattachements[pt].copy()) ) )

            else:
                pile.append((pt_exploree_id,curr))
                del id_points[points[pt_exploree_id]]
        


    """
    on transforme le résultat en le format de retour désiré
    """
    for sep in range(len(separations)):
        real_sep = []
        p = separations[sep][0]
        while p != None:
            real_sep.append(points[p[0]])
            p = p[1]
        separations[sep] = (real_sep,separations[sep][1])
        


    return  separations
