## ## Projet : "Laïka"

#   Vocabulaire:
# LE         = Liste d'Etoiles Caractérisée
# triplet    = Triplet de 3 étoiles
# Couleur    = La couleur moyenne de l'ensemble des pixels qu'elle contient
# Barycentre = La position du centre de l'étoile dans le tableau
# Pixel      = couple associé à une position précise dans un array



## # Bibliothèque:

import matplotlib.image as mpimg
import numpy as np
from imageio import imread, imwrite
import matplotlib.pyplot as plt

#   Constantes du projet:
TRANSPARENT            = np.array([0 , 0 , 0 , 0])
VERT                   = np.array([0 ,255,59,255])
VIOLET                 = np.array([255,3,248,255])
BLEU                   = np.array([27 ,0,255,255])
ROUGE                  = np.array([255,2 ,0, 255])
JAUNE                  = np.array([255,234,0,255])
LCOULEURS              = [VERT,VIOLET,BLEU,ROUGE,JAUNE]
VALEUR_MIN_TRANS       = 0
NOIR                   = 0
VALEUR_MIN             = 100 #valeur au dessus de laquelle on considère un pixel
                             #(suffisamment coloré) appartenant à une étoile
TAILLE_MIN_MAP         = 50  #une étoile est composée au minimum de 50 pixels
TAILLE_MIN_PHOTO1      = 50
TAILLE_MIN_PHOTO2      = 25
Nom_des_constellations = ["La constellation du Cygne (VERTE) est présente","La constellation du Pégase (VIOLETTE) est présente","La constellation de Cassiopée (BLEU) est présente","La constellation de La Grande Ourse (ROUGE) est présente","La constellation d'Orion (JAUNE) est présente"]


## #  Photos sélectionnées

#Ciel de référence
plt.figure()
CIEL = imread("ciel.png")
CIEL_R = np.array(CIEL[:,:,0])
plt.title('CIEL')
plt.imshow(CIEL)
plt.show()

#Calque constellation : représente les constellations une fois tracée
plt.figure()
CALQUE_CONSTELLATION = imread("calque constellation.png")
plt.title('CALQUE_CONSTELLATION')
plt.imshow(CALQUE_CONSTELLATION)
plt.show()

#Ciel transparent où seules les étoiles sont pointées manuellement
plt.figure()
CALQUE_ETOILE = imread("calque etoile.png")
plt.title('CALQUE_ETOILE')
plt.imshow(CALQUE_ETOILE)
plt.show()

#Ciel transparent où seules 3 étoiles par constellation sont pointées
plt.figure()
CALQUE_TRIPLET = imread("calque triplet.png")
MAP            = np.array(CALQUE_TRIPLET[:,:,3])
plt.title('CALQUE_TRIPLET')
plt.imshow(CALQUE_TRIPLET)
plt.show()

#PHOTO 1
plt.figure()
PHOTO1 = imread("photo1.png")
PHOTO1_R = np.array(PHOTO1[:,:,0])
plt.title('PHOTO1')
plt.imshow(PHOTO1)
plt.show()

#PHOTO 2
plt.figure()
PHOTO2 = imread("photo2.png")
PHOTO2_R = np.array(PHOTO2[:,:,0])
plt.title('PHOTO2')
plt.imshow(PHOTO2)
plt.show()


## # I.   Recherche des étoiles dans une photographie

## Fonctions secondaires :


def voisins(pixel,ciel_array,valeur_min):
    """renvoie les voisins de couleur supérieure à COULEUR_MIN de notre pixel"""
    (i,j) = pixel
    voisins = []
    hauteur,longueur = ciel_array.shape
    # on teste les 4 voisins potentiels du pixel
    for delta in [-1,1]:
        if 0 <= i+delta < hauteur and ciel_array[i+delta,j] > valeur_min:
            voisins.append((i+delta,j))
        if 0 <= j+delta < longueur and ciel_array[i,j+delta] > valeur_min:
            voisins.append((i,j+delta))
    return voisins


def couleur_moy(etoile_ensemble_pixel,ciel_array):
    """renvoie la couleur moyenne d'une étoile"""
    C = np.array([0,0,0,0])
    for pixel in etoile_ensemble_pixel:
        C += ciel_array[pixel]
    return C/len(etoile_ensemble_pixel)


def barycentre(etoile_ensemble_pixel):
    """renvoie la position de l'étoile ramenée à son barycentre dans notre image"""
    S = np.zeros(2)
    for pixel in etoile_ensemble_pixel:
        S += np.array(pixel)
    F = (int(S[0]/len(etoile_ensemble_pixel)),int(S[1]/len(etoile_ensemble_pixel)))
    return F


## Fonctions principales


def liste_etoile(ciel_array_rouge,valeur_min):
    """retourne la liste des étoiles présentes dans notre ciel étudié.
    Chaque étoile est définie comme la liste des pixels qui la constituent"""
    copie_ciel_array = np.array(ciel_array_rouge)
    hauteur,longueur = copie_ciel_array.shape
    liste_etoiles_ensemble_pixels = []
    for i in range(hauteur):
        for j in range(longueur):
            #Si on rencontre une étoile
            if copie_ciel_array[i,j] > valeur_min:
                etoile_ensemble_pixels =[]
                #Frontière correspond à l'ensemble des pixels qui appartiennent
                #à l'étoile et qui doivent être traités
                frontiere = [(i,j)]
                while frontiere != [] :
                    pixel = frontiere.pop(0)
                    #Les pixels une fois traités sont mis en NOIR(=0) afin de ne
                    #pas les re-rencontrer
                    copie_ciel_array[pixel] = NOIR
                    etoile_ensemble_pixels.append(pixel)
                    for v in voisins(pixel,copie_ciel_array,valeur_min):
                        if not v in frontiere :
                            frontiere.append(v)
                liste_etoiles_ensemble_pixels.append(etoile_ensemble_pixels)
    return(liste_etoiles_ensemble_pixels)


def caracterisation_liste_etoile(LE,ciel_array,taille_min):
    """redéfinit les étoiles d'une liste non plus comme un ensemble de pixels
    mais comme: leur barycentre et leur couleur moyenne"""
    LEC = []
    for etoile in LE:
        if len(etoile) > taille_min:
            etoile = [barycentre(etoile),couleur_moy(etoile,ciel_array)]
            LEC += [etoile]
    return LEC


#   Exemples

# #Avec PHOTO1:
# L1  = liste_etoile(PHOTO1_R,VALEUR_MIN)
# LE1 = caracterisation_liste_etoile(L1,PHOTO1,TAILLE_MIN_PHOTO1)
#
# # Avec PHOTO2:
# L2  = liste_etoile(PHOTO2_R,VALEUR_MIN)
# LE2 = caracterisation_liste_etoile(L2,PHOTO2,TAILLE_MIN_PHOTO1)
#Nous nous sommes rendus compte que la taille minimale d'une étoile devait
#être de 25 dans la seconde photographie si nous voulions pouvoir faire
#tourner notre programme


## # II.   Définition et construction des constellations

## II.1.  Identification des étoiles appartenant aux différentes constellations

## Fonctions secondaires :


def Distance(x,y):
    """renvoie la distance entre les vecteurs x et y """
    distance = 0
    X = np.array(x)
    Y = np.array(y)
    return np.sqrt(sum((X-Y)**2))


def Vrai_couleur(couleurmoy):
    """renvoie une numéro entre 0, 1, 2,3,4 où chaque position est définie par
    LCOULEURS (couleurmoy est un array)"""
    #On impose un minimum volontairement trop grand afin d'être sûr
    #de trouver un autre minimum
    min = 10**10
    #Indice de la position de la couleur la plus proche de couleurmoy
    I   = 0
    for k in range(len(LCOULEURS)):
        D = Distance(LCOULEURS[k],couleurmoy)
        if min > D:
            min = D
            I   = k
    return I


## Fonction principale :


def RangeTonCiel(LEC):
    """range les étoiles en fonction de leur couleur"""
    LC = [ [] ]*len(LCOULEURS)
    for e in LE:
        position = Vrai_couleur(e[1])
        LC[position] = LC[position] + [e]
        e[1] = LCOULEURS[position]
    return LC


## II.2. Caractérisation des constellations:

## Fonction secondaire :


def Rapport(triplet):
    """ retourne les rapports des distances associées à un triplet d'étoiles.
    On rappelle que la définition d'une étoile est une liste contenant dans
    cet ordre : son barycentre, sa couleur moyenne sous forme d'un array"""
    d1 = Distance(triplet[0][0],triplet[1][0])
    d2 = Distance(triplet[1][0],triplet[2][0])
    d3 = Distance(triplet[2][0],triplet[0][0])
    distance = [d1,d2,d3]
    rapport= min(distance)/max(distance)
    return(rapport)


## Fonction principale :


def caracterisation_constellation(LC_etoile):
    """Retourne une liste de constellation telle que chaque constellation soit
    définie par un scalaire : son rapport"""
    LC_caractérisées = []
    for c in LC_etoile:
        C = [Rapport(c),c]
        LC_caractérisées += [C]
    return(LC_caractérisées)


#   Exécution
#
# L          = liste_etoile(MAP,VALEUR_MIN)
# LE         = caracterisation_liste_etoile(L,CALQUE_TRIPLET,TAILLE_MIN_MAP)
# LEC_rangee = RangeTonCiel(LE)
# LC         = caracterisation_constellation(LEC_rangee)


#Nous obtenons alors LC = la liste de constellations caractérisées :
Liste_constellations_caracterisees = [[0.23093184972414788, [[(205, 774), np.array([  0, 255,  59, 255])], [(208, 825), np.array([  0, 255,  59, 255])], [(335, 953), np.array([  0, 255,  59, 255])]]], [0.14627049769726974, [[(460, 1068), np.array([255,   3, 248, 255])], [(581, 777), np.array([255,   3, 248, 255])], [(584, 823), np.array([255,   3, 248, 255])]]], [0.776449890641863, [[(430, 729), np.array([ 27,   0, 255, 255])], [(449, 698), np.array([ 27,   0, 255, 255])], [(460, 724), np.array([ 27,   0, 255, 255])]]], [0.2675013514651141, [[(190, 400), np.array([255,   2,   0, 255])], [(310, 389), np.array([255,   2,   0, 255])], [(313, 354), np.array([255,   2,   0, 255])]]], [0.4090712294996334, [[(786, 407), np.array([255, 234,   0, 255])], [(803, 453), np.array([255, 234,   0, 255])], [(892, 463), np.array([255, 234,   0, 255])]]]]


## # III.  Recherche des constellations dans la photographie à étudier

## Fonctions secondaires :


def plus_proche(E,liste_etoile):
    """retourne la liste des 10 étoiles, autre que E, les plus proches de E"""
    D = [1000000]*10
    liste_des_10_plus_proche = [10]*10
    for e in liste_etoile:
        d = Distance(E[0],e[0])
        if d <= D[9]:
            for k in range(len(D)):
                if d <= D[k]:
                    D[k:k] = [d]
                    liste_des_10_plus_proche[k:k] = [e]
                    del(liste_des_10_plus_proche[10])
                    del(D[10])
                    break
    return(liste_des_10_plus_proche)


def couple(L):
    """retourne l'ensemble des couples qu'il est possible d'effectuer dans
    une liste de vecteurs"""
    L_copie = list(L)
    LC = []
    for l in L:
        L_copie.pop(0)
        for c in L_copie:
            LC += [ [l,c] ]
    return(LC)


## Fonction principale :


# VOCABULAIRE:
# PPE = liste des 10 étoiles les plus proches de E
# LC  = liste des couples qu'il est possible de faire dans PPE
# LR  = Liste des rapports
# E   = étoile
# LT  = liste des rapports


def recherche_constellation(liste_etoiles_photo):
    """ retourne, si elles existent, toutes les constellations présentes
    dans notre ciel étoilé inconnu"""
    LR = []
    LT = []
    Liste_constellations_photo = []
    LE_copie = list(liste_etoiles_photo)
    #On fabrique des triplets, et on calcule les rapports associés à chacun d'eux
    for E in LE_copie :
        LE_copie.pop(0)
        PPE = plus_proche(E,LE_copie)
        LC  = couple(PPE)
        for C in LC :
            T   = list(C) + [E]
            LR += [Rapport(T)]
            LT += [T]
    #Et on regarde s'ils correspondent à une constellation
    for r in range (len(LR)) :
        for k in range(5):
            if np.abs(LR[r] - Liste_constellations_caracterisees[k][0]) <= 10**(-8):
                Liste_constellations_photo += [[k,LT[r]]]
                break
    return Liste_constellations_photo


#   Exemples

# #Avec PHOTO1:
# R1 = recherche_constellation(LE1)
#
# # Avec PHOTO2:
# R2 = recherche_constellation(LE2)


def NomConstellationPresente(L):
    """associe le numéro de la constellation (qui correspond à sa position
    dans LCOULEUR, à son nom"""
    V = []
    if L == []:
        return("Il n'y a pas de constellation dans l'image.")
    else :
        for l in L :
            V += [Nom_des_constellations[l[0]]]
        return(V)


#   Exemples

# #Avec PHOTO1:
# R1 = recherche_constellation(LE1)
# Il_y_a_t_il_des_constellations_PHOTO1 = NomConstellationPresente(R1)
# print(Il_y_a_t_il_des_constellations_PHOTO1)
#
# # Avec PHOTO2:
# R2 = recherche_constellation(LE2)
# Il_y_a_t_il_des_constellations_PHOTO2 = NomConstellationPresente(R2)
# print(Il_y_a_t_il_des_constellations_PHOTO2)


## # IV.  Tracer les constellations sur la photographie

## Fonctions secondaires :


def Repere(triplet):
    """range un triplet d'étoiles dans une liste telle que : la première est
    l'étoile à l'origine de l'axe définie par ces 3 étoiles, la 2nd est celle
    définissant l'axe des abscisse, et la dernière celle des ordonnées"""
    d1 = Distance(triplet[0][0],triplet[1][0])
    d2 = Distance(triplet[1][0],triplet[2][0])
    d3 = Distance(triplet[2][0],triplet[0][0])
    distance = [d1,d2,d3]
    dmin = min(distance)
    dmax = max(distance)
    if (dmin,dmax) == (d1,d2) :
        C = [triplet[1][0],triplet[0][0],triplet[2][0]]
    if (dmin,dmax) == (d2,d1) :
        C = [triplet[1][0],triplet[2][0],triplet[0][0]]
    if (dmin,dmax) == (d1,d3) :
        C = [triplet[0][0],triplet[1][0],triplet[2][0]]
    if (dmin,dmax) == (d3,d1) :
        C = [triplet[0][0],triplet[2][0],triplet[1][0]]
    if (dmin,dmax) == (d2,d3) :
        C = [triplet[2][0],triplet[1][0],triplet[0][0]]
    if (dmin,dmax) == (d3,d2) :
        C = [triplet[2][0],triplet[0][0],triplet[1][0]]
    xo,yo = C[0]
    xa,ya = C[1]
    xb,yb = C[2]
    OA = [ xa - xo , ya - yo ]
    OB = [ xb - xo , yb - yo ]
    return OA,OB,C


def det2(u,v) :
    """retourne le determinant entre deux vecteurs u et v. u et v sont
    des listes"""
    return u[0]*v[1]-u[1]*v[0]


#   Exemple

# #Avec PHOTO1:
# T = Liste_constellations_caracterisees[0][1]
# print(Repere)


## Fonction principale :


def Tracer(photo,calque,LC_photo):
    """Trace sur une photographie les constellations qui y sont présente"""
    calque_copie        = np.array(calque[:,:,3])
    photo_copie         = np.array(photo[:,:,:])
    OA_P,OB_P,RP        = Repere(LC_photo[0][1])
    xo_P,yo_P           = RP[0]
    constellation       = Liste_constellations_caracterisees[LC_photo[0][0]]
    triplet             = constellation[1]
    OA_C,OB_C,RC        = Repere(triplet)
    xo_C,yo_C           = RC[0]
    hauteur,longueur,d  = photo.shape
    for i in range (hauteur):
        for j in range (longueur):
            #On détermine les coordonnées de notre pixel dans le repère de la photo
            OP_P   = [ i - xo_P , j - yo_P ]
            x_P    = det2(OP_P,OB_P)/det2(OA_P,OB_P)
            y_P    = det2(OP_P,OA_P)/det2(OA_P,OB_P)
            #On en déduit les coordonnées dans le repère du calque
            OP_C   = [x_P*OA_C[0]+y_P*OB_C[0],x_P*OA_C[1]+y_P*OB_C[1]]
            i2     = hauteur - int(OP_C[0] + xo_C)
            j2     = int(OP_C[1] + yo_C)
            if calque_copie[i2,j2] > 0:
                photo_copie[i,j] = calque[i2,j2]
    return(photo_copie)



#   Exécution

# #Avec PHOTO1:
# photo_tracée = Tracer(PHOTO1,CALQUE_CONSTELLATION,R1)
# plt.imshow(photo_tracée)
# plt.show()


## # V.  Exécution finale de Laïka


def Laika(photo,taille_min):
    """retourne, s'il y en a, les noms des constellations présentes dans la
    photographie, ainsi que le tracé de ces constellations sur la photographie"""
    photo_R = np.array(photo[:,:,0])
    L       = liste_etoile(photo_R,VALEUR_MIN)
    LE      = caracterisation_liste_etoile(L,photo,taille_min)
    R       = recherche_constellation(LE)
    N       = NomConstellationPresente(R)
    if R != []:
        plt.figure()
        photo_tracée = Tracer(photo,CALQUE_CONSTELLATION,R)
        plt.title('Tracé des constellations sur la photographie')
        plt.imshow(photo_tracée)
        plt.show()
    else :
        plt.figure()
        plt.title('Il n y a pas de constellation à tracer dans la photographie')
        plt.imshow(photo)
        plt.show()
    print(N)
    return


#   Exemples

# #Avec PHOTO1:
Laika(PHOTO1,50)

# #Avec PHOTO1:
Laika(PHOTO2,25)


