# EXAMEN2024
Question 1 — Constructeur de Game
*********************************

pythonclass Game(Object):
    def __init__(self, max_gamers, nbr_sticks) -> None:
        self.max_gamers = max_gamers
        self.nbr_sticks = nbr_sticks
        self.players = []

Question 2 — Méthode listen 
***************************

pythondef listen(self, port):
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.bind(('', port))
    self.server_socket.listen(self.max_gamers)
    while len(self.players) < self.max_gamers:
        client_socket, address = self.server_socket.accept()
        self.players.append(client_socket)
Ajout au constructeur : self.players = [] pour stocker les joueurs et limiter les connexions à max_gamers.


Question 3 — communicate_with_client
*************************************

pythondef communicate_with_client(self, client_id: int) -> None:
    send(client_id, "Choisissez 1, 2 ou 3 bâtonnets à retirer")
    response = read()
    if not response.isdigit() or int(response) < 1 or int(response) > 3:
        send(client_id, "erreur")
        return
    self.nbr_sticks -= int(response)
    if self.nbr_sticks > 0:
        send(client_id, "vous restez dans le jeu")
    else:
        send(client_id, "perdu")
        for i in range(len(self.players)):
            if i != client_id:
                send(i, "gagné")

                
Question 4 — Threads + Fonction principale 
******************************************
Modification de communicate_with_client : ajouter au début :
pythonsend(client_id, f"Il reste {self.nbr_sticks} bâtonnets")
Les threads sont nécessaires car sans eux, le serveur est bloqué sur read() en attendant la réponse d'un joueur, ce qui empêche les autres de jouer. Avec les threads, chaque joueur est géré en parallèle.
pythonimport threading

def main(self, port):
    self.listen(port)
    while self.nbr_sticks > 0:
        threads = []
        for i in range(len(self.players)):
            t = threading.Thread(target=self.communicate_with_client, args=(i,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

Question 5 — TCP vs UDP
***********************
Changements à apporter :
SOCK_STREAM → SOCK_DGRAM
Supprimer listen() et accept()
send(msg) → sendto(msg, adresse)
recv() → recvfrom() qui retourne (data, adresse)

Critère                      TCP                        UDP
Connexion                    Oui                        Non 
Fiabilité                    Garantie                 Non garantie
Ordre                        Respecté                 Non respecté
Vitesse                      Plus lent                Plus rapide
