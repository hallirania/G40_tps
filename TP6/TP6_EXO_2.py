def compter_mots(texte):
    mots = texte.split()
    return len(mots)


# test
texte = "Bonjour tout le monde, commencez à coder."
print(compter_mots(texte))