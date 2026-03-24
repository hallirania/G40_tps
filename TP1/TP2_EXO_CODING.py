# =====================
#      DOUBLONS
# =====================

def contient_doublons(t):
    return len(t) != len(set(t))

# L'utilisateur entre le tableau
entree = input("Entrez les entiers séparés par des virgules : ")
t = [int(x) for x in entree.split(',')]
print("Contient des doublons :", contient_doublons(t))


# ========================
#       ANAGRAMME
# ========================

def est_anagramme(s, t):
    return sorted(s) == sorted(t)

# L'utilisateur entre les deux chaînes
s = input("\nEntrez la première chaîne : ")
t = input("Entrez la deuxième chaîne : ")
print("Est un anagramme :", est_anagramme(s, t))