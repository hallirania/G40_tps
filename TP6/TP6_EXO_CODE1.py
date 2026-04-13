def nb_facons(n):
    if n == 0 or n == 1:
        return 1

    return nb_facons(n-1) + nb_facons(n-2)


# test
print(nb_facons(4))  