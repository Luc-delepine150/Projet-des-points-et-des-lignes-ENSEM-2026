class Point():
    pass

class Point():
    """
    Modélise un point selon ses coordonnées dans le plan
    """

    def __init__(self,x : int, y : int) -> None:
        """
        initialise un objet Point
        self.x = x
        self.y = y
        """
        self.x = x
        self.y = y
    
    def dist_squared(self, p : Point) -> int:
        """
        renvoi la (distance euclidienne entre self et p) au carré
        """
        return (self.x-p.x)**2+(self.y-p.y)**2
    
    def dist(self, p : Point) -> float:
        """
        renvoi la distance euclidienne entre self et p
        """
        return (self.dist_squared(p))**0.5
    

    def norme_squared(self, p : Point) -> int:
        """
        renvoi la (norme de p) au carré
        """
        return (p.x)**2+(p.y)**2
    
    def norme(self, p : Point) -> float:
        """
        renvoi la norme de p
        """
        return self.norme_squared(p)**0.5
    
    def prod_scalaire(self, p : Point) -> int:
        """
        renvoi le produit scalaire (self scal p)
        """
        return self.x*p.x + self.y*p.y
    
    def prod_vectoriel(self, p : Point) -> int:
        """
        renvoi le produit vectoriel (self vect p)
        """
        return self.x*p.y - self.y*p.x
    
    def tuple_from_point(self) -> tuple[int,int]:
        """
        renvoi le tuple (sel.x,self.y)
        """
        return (self.x,self.y)
    
    def point_from_tuple(self, tp : tuple[int,int]) -> Point:
        """
        renvoi l'objet point défini par le tuple (x,y)
        """
        return Point(tp[0],tp[1])
    
    def __eq__(self, other) -> bool:
        """
        self == p
        """
        if not isinstance(other, Point):
            return False
        return self.tuple_from_point() == other.tuple_from_point()
    
    def __ne__(self, other) -> bool:
        """
        self != p
        """
        if not isinstance(other, Point):
            return True
        return self.tuple_from_point() != other.tuple_from_point()
    
    def __lt__(self, p: Point) -> bool:
        """
        self > p
        """
        return NotImplementedError
    
    def __le__(self, p: Point) -> bool:
        """
        self <= p
        """
        return NotImplementedError
    
    def __gt__(self, p: Point) -> bool:
        """
        self > p
        """
        return NotImplementedError
    
    def __ge__(self, p: Point) -> bool:
        """
        self >= p
        """
        return NotImplementedError

    def __hash__(self) -> int:
        """
        'Called by built-in function hash() and for operations on members of hashed collections including set, frozenset, and dict.
        The __hash__() method should return an integer.
        The only required property is that objects which compare equal have the same hash value.'
        
        utilise le hash des tuples pour les points 
        """
        return hash(self.tuple_from_point())
    
    def __add__(self, p : Point) -> Point:
        """
        renvoi self+p
        """
        return Point(self.x+p.x,self.y+p.y)
    
    def __sub__(self, p : Point) -> Point:
        """
        renvoi self-p
        """
        return Point(self.x-p.x,self.y-p.y)
    
    def __repr__(self):
        return self.tuple_from_point().__repr__()