# outilsGeometrie.py
import math

def distance_point_segment(p, a, b):
    """
    Calcule la distance minimale entre un point et un segment.

    Paramètres
    ----------
    p : Point
        Point dont on calcule la distance.
    a : Point
        Premier point du segment.
    b : Point
        Second point du segment.

    Retour
    ------
    float
        Distance minimale entre p et le segment [a, b].
    """
    ax, ay = a.x, a.y
    bx, by = b.x, b.y
    px, py = p.x, p.y

    dx = bx - ax
    dy = by - ay

    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)

    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))

    cx = ax + t * dx
    cy = ay + t * dy

    return math.hypot(px - cx, py - cy)
