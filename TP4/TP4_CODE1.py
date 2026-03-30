def romain_vers_entier(s):
    valeurs = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    resultat = 0

    for i in range(len(s)):
        valeur_actuelle = valeurs[s[i]]

        # Si ce n'est pas le dernier symbole et que le suivant est plus grand
        if i + 1 < len(s) and valeurs[s[i + 1]] > valeur_actuelle:
            resultat -= valeur_actuelle  
        else:
            resultat += valeur_actuelle 
    return resultat


def entier_vers_romain(n):

    valeurs = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90,  'XC'),
        (50,  'L'),
        (40,  'XL'),
        (10,  'X'),
        (9,   'IX'),
        (5,   'V'),
        (4,   'IV'),
        (1,   'I')
    ]

    resultat = ""

    for valeur, symbole in valeurs:
        while n >= valeur:   
            resultat += symbole 
            n -= valeur         

    return resultat


def main():
    print("=== Convertisseur de nombres romains ===")
    print("1 - Romain → Entier")
    print("2 - Entier → Romain")

    choix = input("\nVotre choix (1 ou 2) : ")

    if choix == "1":
        romain = input("Entrez un nombre romain : ").upper()
        print(f"Résultat : {romain_vers_entier(romain)}")

    elif choix == "2":
        entier = int(input("Entrez un entier : "))
        print(f"Résultat : {entier_vers_romain(entier)}")

    else:
        print("Choix invalide !")

main()