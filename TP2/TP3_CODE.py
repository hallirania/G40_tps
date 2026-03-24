
#=========================#
#==========EXO1===========#             
def somme_nulle_deux(tab):
    vus = set()

    for x in tab:
        if -x in vus:
            return [x, -x]
        vus.add(x)

    return None


entree = input("EXO1 :Entrez des nombres séparés par des espaces : ")
tab = list(map(int, entree.split()))

resultat = somme_nulle_deux(tab)

if resultat:
    print("Couple trouvé :", resultat)
else:
    print("Aucun couple de somme nulle trouvé.")

#============================#
#==========EXO2==============# 

def somme_nulle_trois(tab):
    n = len(tab)

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if tab[i] + tab[j] + tab[k] == 0:
                    return [tab[i], tab[j], tab[k]]

    return None


entree = input("EXO2:Entrez des nombres séparés par des espaces : ")
tab = list(map(int, entree.split()))

resultat = somme_nulle_trois(tab)

if resultat:
    print("Triplet trouvé :", resultat)
else:
    print("Aucun triplet de somme nulle trouvé.")