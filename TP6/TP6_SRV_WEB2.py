from http.server import BaseHTTPRequestHandler, HTTPServer

# Cette classe sert à définir comment le serveur doit répondre aux requêtes HTTP
class MonServeurHTTP(BaseHTTPRequestHandler):

    # Cette méthode est appelée automatiquement quand le client envoie une requête GET
    def do_GET(self):

        # Si le client demande bien /index.html
        if self.path == "/index.html":

            # Contenu de la page HTML à renvoyer
            body = """<html>
<body>
<h1>Bienvenue</h1>
<p>Ceci est la page index.</p>
</body>
</html>"""

            # On envoie le code de réponse 200 OK
            self.send_response(200)

            # On envoie les headers
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # On envoie le contenu de la page
            self.wfile.write(body.encode())

        # Tous les autres cas : on renvoie une erreur 404
        else:
            body = """<html>
<body>
<h1>404 Not Found</h1>
<p>Toujours pas dispo en cas d'urgence veullez contacter le service client.</p>
</body>
</html>"""

            # On envoie le code de réponse 404
            self.send_response(404)

            # On envoie les headers
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # On envoie la page d'erreur
            self.wfile.write(body.encode())


# Adresse locale et port du serveur
adresse = ("127.0.0.1", 8000)

# Création du serveur HTTP
serveur = HTTPServer(adresse, MonServeurHTTP)

print("Le serveur tourne sur http://127.0.0.1:8000")

# Le serveur reste actif et attend les connexions
serveur.serve_forever()