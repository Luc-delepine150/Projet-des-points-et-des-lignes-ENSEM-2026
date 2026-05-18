import cv2
import numpy as np
import matplotlib.pyplot as plt


# ==========================================================
# CLASSE POINT
# ==========================================================

class Point:
    def __init__(self, idx, x, y, contour_id):
        self.idx = idx
        self.x = float(x)
        self.y = float(y)
        self.contour_id = contour_id

    def tuple(self):
        return (int(self.x), int(self.y))


# ==========================================================
# PRÉ-TRAITEMENT DE L’IMAGE
# ==========================================================

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, binary = cv2.threshold(
        blur, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = np.ones((3,3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    return binary


# ==========================================================
# EXTRACTION DES POINTS PAR CONTOUR (TOUS LES CONTOURS)
# ==========================================================

def extract_points(binary):
    contours, hierarchy = cv2.findContours(
        binary,
        cv2.RETR_TREE,        # <<< ICI : TOUS LES CONTOURS (externes + internes)
        cv2.CHAIN_APPROX_NONE
    )

    all_contours_points = []
    point_index = 1

    for contour_id, contour in enumerate(contours):

        # se quiseres mesmo TUDO, comenta esta linha:
        if cv2.contourArea(contour) < 10:
            continue

        contour_points = []
        for p in contour:
            x, y = p[0]
            pt = Point(point_index, x, y, contour_id)
            contour_points.append(pt)
            point_index += 1

        all_contours_points.append(contour_points)

    return all_contours_points


# ==========================================================
# DESSIN DES POINTS
# ==========================================================

def draw_points(img_shape, all_contours_points):
    canvas = np.ones((img_shape[0], img_shape[1], 3), dtype=np.uint8) * 255

    colors = [(255,0,0), (0,255,0), (0,0,255),
              (255,128,0), (128,0,255), (0,255,255)]

    for i, contour_points in enumerate(all_contours_points):
        color = colors[i % len(colors)]
        for pt in contour_points:
            cv2.circle(canvas, pt.tuple(), 2, color, -1)

    return canvas


# ==========================================================
# DESSIN DES CONTOURS (LIGNES ENTRE POINTS)
# ==========================================================

def draw_contours(img_shape, all_contours_points):
    canvas = np.ones((img_shape[0], img_shape[1], 3), dtype=np.uint8) * 255

    colors = [(255,0,0), (0,255,0), (0,0,255),
              (255,128,0), (128,0,255), (0,255,255)]

    for i, contour_points in enumerate(all_contours_points):
        color = colors[i % len(colors)]

        if len(contour_points) < 2:
            continue

        pts = np.array([pt.tuple() for pt in contour_points], dtype=np.int32)
        cv2.polylines(canvas, [pts], isClosed=True, color=color, thickness=2)

    return canvas

def construire_aretes(sommets):
    n = len(sommets)
    aretes = set()
    for i in range(n):
        a = sommets[i]
        b = sommets[(i+1)%n]  # lien dernier -> premier
        aretes.add(frozenset((a, b)))  # AB = BA
    return aretes

def aretes_communes(liste1, liste2):
    return construire_aretes(liste1) & construire_aretes(liste2)

def Somme(c1, c2, c3):  # Est ce que c1 + c2 = c3 ?
    # Trouver l'arête commune
    communes = list(aretes_communes(c1, c2))
    if len(communes) != 1:
        return False

    u, v = tuple(communes[0])  # extrémités de l'arête commune

    # Choisir un sommet de départ (idéalement pas sur l'arête commune)
    start = None
    for x in c1:
        if x != u and x != v:
            start = x
            break

    # index de départ dans c1
    i1 = c1.index(start)
    i2 = 0  # sera défini au moment du switch
    in_c1 = True
    union = [start]

    # sécurité anti-boucle infinie
    max_steps = len(c1) + len(c2) + len(c3) + 20
    steps = 0

    while steps < max_steps:
        steps += 1

        if in_c1:
            n1 = len(c1)
            nxt = c1[(i1 + 1) % n1]

            # avancer normalement sur c1
            i1 = (i1 + 1) % n1

            # si on revient au start -> fin du contour
            if nxt == start:
                break

            union.append(nxt)

            # si on arrive sur u ou v, on switch dans c2
            if nxt == u or nxt == v:
                cur = nxt
                other = v if cur == u else u

                n2 = len(c2)
                j = c2.index(cur)

                # voisins dans c2
                nxt2 = c2[(j + 1) % n2]
                prv2 = c2[(j - 1) % n2]

                # choisir le sens qui NE prend PAS directement l'arête commune
                if nxt2 == other and prv2 != other:
                    direction = -1
                elif prv2 == other and nxt2 != other:
                    direction = +1
                else:
                    # si les deux sont possibles , on prend +1
                    direction = +1

                # se positionner sur c2
                in_c1 = False
                i2 = j
                dir2 = direction

        else:
            # on avance sur c2 jusqu'à atteindre l'autre extrémité
            n2 = len(c2)
            i2 = (i2 + dir2) % n2
            nxt = c2[i2]

            # éviter de rajouter deux fois le même sommet d'affilée
            if union[-1] != nxt:
                union.append(nxt)

            # si on atteint l'autre extrémité, retour sur c1
            if nxt == u or nxt == v:
                # on revient sur c1 à partir de ce sommet
                i1 = c1.index(nxt)
                in_c1 = True

    # retirer une éventuelle répétition
    if len(union) >= 2 and union[0] == union[-1]:
        union.pop()

    # Vérification finale
    return construire_aretes(union) == construire_aretes(c3)

def isIn(extCyc,intCyc): #Détermine si intCyc est à l’intérieur de extCyc
  for lmt in intCyc:
    if lmt in extCyc:return False
  sub0,sub1,sub2=intCyc[0],extCyc[0],extCyc[1]
  return Somme([sub1,sub0]+extCyc[1:],[sub1,sub0,sub2],extCyc)

def filterCycles(): #Filtre les cycles élémentaires des cycles superflus
  global cyc_lst
  keep=True
  while keep:
    try:
      for i1 in range(cyc_nb):
        for i2 in range(cyc_nb):
          for i3 in range(cyc_nb):
            if i1!=i2 and i1!=i3 and i2!=i3:
              assert not Somme(cyc_lst[i1],cyc_lst[i2],cyc_lst[i3])
      keep=False
    except:
      del cyc_lst[i3]

def findSurfaces(): #Modélise les surfaces du graphe
  global surf_lst,cyc_nb
  surf_lst=[[cyc,[]] for cyc in cyc_lst]
  incl_mat=[[isIn(cyc_lst[i],cyc_lst[j]) for j in range(cyc_nb)] for i in range(cyc_nb)]
  done={}
  while True:
    incl_count_lst=[0]*cyc_nb
    for i in range(cyc_nb):
      for j in range(cyc_nb):
        if j not in done:
          incl_count_lst[i]+=incl_mat[i][j]
    if incl_count_lst!=[0]*cyc_nb:
      for i in range(cyc_nb):
        if incl_count_lst[i]==1:
          j=incl_mat[i].index(1)
          surf_lst[j][1].append(cyc_lst[i])
          done[j]=None
    else:break
  for lst in surf_lst:print(lst)

def same_cyc(cyc1,cyc2): #Détermine si cyc1 et cyc2 décrivent un même cycle
  l=len(cyc2)
  if len(cyc1)!=l:return False
  i0=0
  for i in range(l):
    if cyc2[i]==cyc1[0]:
      i0=i
  if sum([cyc1[i]==cyc2[(i0+i)%l] for i in range(l)])==l:
    return True
  else:
    return (sum([cyc1[i]==cyc2[(i0-i)%l] for i in range(l)])==l)

def new_cycle(): #Détecte de nouveaux cycles pendant le parcours du graphe
  global cyc_lst
  for l in range(1,len(pile)+1):
    if mat_adj[sommets.index(pile[-1])][sommets.index(pile[-l])]:
      if not sum([same_cyc(pile[-l:],cyc) for cyc in cyc_lst]):
        cyc_lst.append(pile[-l:])

def explore(): #Explore le sommet suivant pendant le parcours du graphe
  global pile,seen,sommets,mat_adj
  current=pile[-1]
  seen.add(current)
  j=sommets.index(current)
  for i in range(len(sommets)):
    if mat_adj[i][j] and sommets[i] not in pile:
      pile.append(sommets[i])
      new_cycle()
      explore()
  del pile[-1]


# ==========================================================
# PROGRAMME PRINCIPAL
# ==========================================================

def run(path):

    img = cv2.imread(path)  ### pour l'image

    binary = preprocess(img)
    all_contours_points = extract_points(binary)

    points_img = draw_points(img.shape, all_contours_points)
    contours_img = draw_contours(img.shape, all_contours_points)

    fig, ax = plt.subplots(1, 4, figsize=(22,6))

    ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax[0].set_title("Image Originale")

    ax[1].imshow(binary, cmap="gray")
    ax[1].set_title("Image Binaire")

    ax[2].imshow(cv2.cvtColor(points_img, cv2.COLOR_BGR2RGB))
    ax[2].set_title("Points Extraits (tous les contours)")

    ax[3].imshow(cv2.cvtColor(contours_img, cv2.COLOR_BGR2RGB))
    ax[3].set_title("Contours (tous les contours)")

    for a in ax:
        a.axis("off")

    plt.show()
    
    global sommets,length,aretes,mat_adj
    sommets=all_contours_points[0]
    length=len(sommets)

    aretes=construire_aretes(sommets)
    mat_adj=[]
    for _ in range(length):
      mat_adj.append([0]*length)
    for i in range(length):
      for j in range(length):
        if frozenset((sommets[i],sommets[j])) in aretes:
          mat_adj[i][j]=1
          mat_adj[j][i]=1
    
    global cyc_lst,set_cyc_lst,seen,cyc_nb,pile
    cyc_lst=[]
    set_cyc_lst=[]
    seen=set()
    i=0
    pile=[sommets[i]]
    explore()
    while len(seen)!=length:
      i+=1
      if sommets[i] not in seen:
        pile=[sommets[i]]
        explore()
    
    cyc_nb=len(cyc_lst)

        
        

        
    findSurfaces()
    return sommets,mat_adj
