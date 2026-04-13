def format_http_request(method, url, version, headers, body):
    methodes_autorisees = ["GET", "POST", "PUT", "DELETE", "HEAD"]

    if method not in methodes_autorisees:
        raise ValueError("Méthode HTTP invalide")

    if version == 1:
        http_version = "HTTP/1.1"
    elif version == 2:
        http_version = "HTTP/2.0"
    else:
        raise ValueError("Version HTTP invalide")

    requete = f"{method} {url} {http_version}\n"

    for cle, valeur in headers.items():
        requete += f"{cle}: {valeur}\n"

    requete += "\n"
    requete += body

    return requete


def format_http_response(version, status_code, info, headers, body):
    if version == 1:
        http_version = "HTTP/1.1"
    elif version == 2:
        http_version = "HTTP/2.0"
    else:
        raise ValueError("Version HTTP invalide")

    reponse = f"{http_version} {status_code} {info}\n"

    for cle, valeur in headers.items():
        reponse += f"{cle}: {valeur}\n"

    reponse += "\n"
    reponse += body

    return reponse


# =========================
# Test exercice 1 : requête HTTP
# =========================
headers_requete = {
    "Host": "localhost:8000",
    "User-Agent": "PythonTest",
    "Accept": "text/html"
}

body_requete = "Bonjour"

requete = format_http_request("GET", "/index.html", 1, headers_requete, body_requete)

print("===== REQUETE HTTP =====")
print(requete)


# =========================
# Test exercice 2 : réponse HTTP
# =========================
headers_reponse = {
    "Server": "PythonTPServer",
    "Connection": "Closed"
}

body_reponse = """<html>
<body>
<h1>Bienvenue</h1>
<p>La page a bien été trouvée.</p>
</body>
</html>"""

reponse = format_http_response(1, 200, "OK", headers_reponse, body_reponse)
print(reponse)