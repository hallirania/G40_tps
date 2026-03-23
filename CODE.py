def produit_autres_elements(tableau):
    n = len(tableau)
    resultat = [1] * n
    
    # Etape 1 : calcule le produit de tous les éléments à GAUCHE de i
    gauche = 1
    for i in range(n):
        resultat[i] = gauche
        gauche *= tableau[i]
    
    # Etape 2 : calcule le produit de tous les éléments à DROITE de i
    droite = 1
    for i in range(n - 1, -1, -1):
        resultat[i] *= droite
        droite *= tableau[i]
    
    return resultat


def test_unitaire():
    # Test 1 : [1, 2, 3, 4, 5] → [120, 60, 40, 30, 24]
    assert produit_autres_elements([1, 2, 3, 4, 5]) == [120, 60, 40, 30, 24], "Test 1 échoué"
    print("Test 1 réussi : [1, 2, 3, 4, 5] → {}".format(produit_autres_elements([1, 2, 3, 4, 5])))
    
    # Test 2 : [3, 2, 1] → [2, 3, 6]
    assert produit_autres_elements([3, 2, 1]) == [2, 3, 6], "Test 2 échoué"
    print("Test 2 réussi : [3, 2, 1] → {}".format(produit_autres_elements([3, 2, 1])))
    
    # Test 3 : [2, 3, 4] → [12, 8, 6]
    assert produit_autres_elements([2, 3, 4]) == [12, 8, 6], "Test 3 échoué"
    print("Test 3 réussi : [2, 3, 4] → {}".format(produit_autres_elements([2, 3, 4])))
    
    print("\nTous les tests sont réussis !")


if __name__ == '__main__':
    test_unitaire()