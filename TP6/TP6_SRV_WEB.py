import socket

# Cette fonction sert à construire une réponse HTTP propre
def format_http_response(version, status_code, info, headers, body):
    # On transforme le numéro de version en vrai format HTTP
    if version == 1:
        http_version = "HTTP/1.1"
    elif version == 2:
        http_version = "HTTP/2.0"
    else:
        raise ValueError("Version HTTP invalide")

    # Première ligne de la réponse HTTP
    reponse = f"{http_version} {status_code} {info}\n"

    # On ajoute les headers un par un
    for cle, valeur in headers.items():
        reponse += f"{cle}: {valeur}\n"

    # Ligne vide pour séparer les headers du body
    reponse += "\n"

    # On ajoute ensuite le contenu de la page
    reponse += body

    return reponse


# Création de la socket du serveur
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# On lie le serveur à l'adresse locale et au port 8000
serveur.bind(("127.0.0.1", 8000))

# Le serveur se met en attente de connexions
serveur.listen(1)

print("Le serveur tourne sur http://127.0.0.1:8000")


# Boucle infinie pour laisser le serveur actif
while True:
    # Le serveur accepte une connexion venant d'un client
    client_socket, client_address = serveur.accept()
    print("Connexion reçue de :", client_address)

    # On récupère la requête envoyée par le client
    requete = client_socket.recv(1024).decode()
    print("Requête reçue :")
    print(requete)

    # On récupère seulement la première ligne de la requête
    premiere_ligne = requete.split("\n")[0]

    # On découpe cette ligne en plusieurs morceaux
    morceaux = premiere_ligne.split()

    # Par sécurité, on vérifie qu'il y a bien au moins une méthode et une URL
    if len(morceaux) >= 2:
        methode = morceaux[0]
        url = morceaux[1]
    else:
        methode = ""
        url = ""

    # Cas où le client demande bien la page index.html avec GET
    if methode == "GET" and url == "/index.html":
        body = """<html>
<body>
<h1>Bienvenue</h1>
<p>Ceci est la page index.</p>
</body>
</html>"""

        headers = {
            "Server": "PythonTPServer",
            "Connection": "Closed",
            "Content-Type": "text/html"
        }

        reponse = format_http_response(1, 200, "OK", headers, body)

    # Tous les autres cas : on renvoie une erreur 404
    else:
        body = """<html>
<body>
<h1>404 Not Found</h1>
<p>Votre correspondant est injoignable pour le moment l'appareil doit etre eteint ou en dehors de la zone de couverture veuillez reessayer ulterieurement MERCI .</p>
</body>
</html>"""

        headers = {
            "Server": "PythonTPServer",
            "Connection": "Closed",
            "Content-Type": "text/html"
        }

        reponse = format_http_response(1, 404, "Not Found", headers, body)

    # On envoie la réponse au client
    client_socket.send(reponse.encode())

    # On ferme la connexion avec ce client
    client_socket.close()
    