def swap_bits(n, i, j):
    bit_i = (n >> i) & 1
    bit_j = (n >> j) & 1

    if bit_i != bit_j:
        masque = (1 << i) | (1 << j)
        n = n ^ masque

    return n


n = int(input("Entrez n : "))
i = int(input("Entrez i : "))
j = int(input("Entrez j : "))

print("Résultat :", swap_bits(n, i, j))