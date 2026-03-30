import socket
from _thread import start_new_thread
import threading
import json

class Serveur:
    def __init__(self, host="", port=12345):
        self.host = host
        self.port = port
        self.print_lock = threading.Lock()
        self.clients = {}  # {socket: nom_client}

   
    def envoyer_json(self, c, data):
        c.send(json.dumps(data).encode())

   
    def broadcast(self, data, expéditeur=None):
        for client_socket in list(self.clients.keys()):
            if client_socket != expéditeur:
                try:
                    client_socket.send(json.dumps(data).encode())
                except:
                    pass

    def communication_client(self, c):
        nom = None
        try:
            # ── Identification ──────────────────────────────
            data_json = c.recv(1024).decode().strip()
            msg = json.loads(data_json)

            if msg.get("type") != "identification":
                c.send("Erreur : premier message doit être identification.".encode())
                return

            nom            = msg["nom"]
            lieu           = msg["lieu"]
            date_connexion = msg["date_connexion"]
            print(f"[+] {nom} connecté depuis {lieu} le {date_connexion}")

            with self.print_lock:
                self.clients[c] = nom

                # Envoie le nombre de clients connectés
                self.envoyer_json(c, {
                    "type": "notification",
                    "evenement": "nb_clients",
                    "valeur": len(self.clients)
                })

                # Notifie les autres de la connexion
                self.broadcast({
                    "type": "notification",
                    "evenement": "connexion",
                    "nom": nom
                }, expéditeur=c)

            # ── Boucle messages ─────────────────────────────
            while True:
                data = c.recv(1024)
                if not data:
                    break

                message = data.decode().strip()

                if message.lower() == "quit":
                    break

                try:
                    msg = json.loads(message)
                except json.JSONDecodeError:
                    c.send("Erreur : message JSON invalide.".encode())
                    continue

                # ── Changement d'état ────────────────────────
                if msg.get("type") == "notification" and msg.get("evenement") == "etat":
                    etat = msg["etat"]
                    print(f"[~] {nom} est maintenant {etat}")
                    self.broadcast({
                        "type": "notification",
                        "evenement": "etat",
                        "nom": nom,
                        "etat": etat
                    }, expéditeur=c)

                # ── En train d'écrire ────────────────────────
                elif msg.get("type") == "notification" and msg.get("evenement") == "en_train_ecrire":
                    self.broadcast({
                        "type": "notification",
                        "evenement": "en_train_ecrire",
                        "nom": nom
                    }, expéditeur=c)

                # ── Message chat ─────────────────────────────
                elif msg.get("type") == "message":
                    destinataire = msg.get("destinataire")
                    contenu      = msg.get("contenu")
                    envoye = False
                    for client_socket, client_nom in list(self.clients.items()):
                        if client_nom == destinataire:
                            self.envoyer_json(client_socket, {
                                "type": "message",
                                "expediteur": nom,
                                "contenu": contenu
                            })
                            envoye = True
                            break
                    if not envoye:
                        self.envoyer_json(c, {
                            "type": "erreur",
                            "contenu": f"Client '{destinataire}' introuvable."
                        })

        except json.JSONDecodeError:
            print("Erreur : JSON invalide à la connexion.")
        except ConnectionResetError:
            print(f"Connexion coupée brutalement par {nom}.")
        except Exception as e:
            print(f"Erreur avec {nom} : {e}")
        finally:
            with self.print_lock:
                if c in self.clients:
                    del self.clients[c]
                    self.broadcast({
                        "type": "notification",
                        "evenement": "deconnexion",
                        "nom": nom
                    }, expéditeur=c)
                    print(f"[-] {nom} déconnecté.")
            c.close()

    def thread_ecoute(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        print("Socket bindée au port", self.port)
        s.listen(5)
        print("Le serveur est en écoute...")
        while True:
            c, addr = s.accept()
            print("Connecté au client :", addr[0], ":", addr[1])
            start_new_thread(self.communication_client, (c,))

if __name__ == '__main__':
    serveur = Serveur()
    serveur.thread_ecoute()