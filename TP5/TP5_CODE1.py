def compter_bits_a_1(n):
    compteur = 0

    while n > 0:
        compteur += n & 1
        n = n >> 1

    return compteur


n = int(input("Entrez un entier : "))
print("Nombre de bits à 1 :", compter_bits_a_1(n))