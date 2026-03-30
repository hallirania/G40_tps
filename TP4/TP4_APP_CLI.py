import socket
import threading
import json
from datetime import date

class Client:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port

    def afficher_message(self, msg):
        t = msg.get("type")

        if t == "notification":
            ev = msg.get("evenement")
            if ev == "nb_clients":
                print(f"[INFO] Clients connectés : {msg['valeur']}")
            elif ev == "connexion":
                print(f"[+] {msg['nom']} a rejoint le chat !")
            elif ev == "deconnexion":
                print(f"[-] {msg['nom']} s'est déconnecté.")
            elif ev == "en_train_ecrire":
                print(f"[...] {msg['nom']} est en train d'écrire")
            elif ev == "etat":
                print(f"[~] {msg['nom']} est {msg['etat']}")

        elif t == "message":
            print(f"\n[{msg['expediteur']}] : {msg['contenu']}")

        elif t == "erreur":
            print(f"[ERREUR] {msg['contenu']}")

    def recevoir_messages(self, s):
        while True:
            try:
                data = s.recv(1024).decode()
                if not data:
                    break
                msg = json.loads(data)
                self.afficher_message(msg)
            except:
                break

    def main(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))

        # ── Identification ───────────────────────────────────
        s.send(json.dumps({
            "type": "identification",
            "nom": "client1",
            "date_connexion": str(date.today()),
            "lieu": "Paris"
        }).encode())

        thread = threading.Thread(target=self.recevoir_messages, args=(s,))
        thread.daemon = True
        thread.start()

        print("Commandes disponibles :")
        print("  destinataire:message  → envoyer un message")
        print("  /etat LIBRE|OCCUPE|INACTIF → changer d'état")
        print("  quit → quitter\n")

        while True:
            message = input()

            if message.lower() == "quit":
                s.send("quit".encode())
                break

            # ── Changement d'état ────────────────────────────
            elif message.startswith("/etat "):
                etat = message.split(" ", 1)[1].upper()
                s.send(json.dumps({
                    "type": "notification",
                    "evenement": "etat",
                    "etat": etat
                }).encode())

            # ── Message chat ─────────────────────────────────
            elif ":" in message:
                # Notifie qu'on est en train d'écrire
                s.send(json.dumps({
                    "type": "notification",
                    "evenement": "en_train_ecrire"
                }).encode())

                destinataire, contenu = message.split(":", 1)
                s.send(json.dumps({
                    "type": "message",
                    "destinataire": destinataire.strip(),
                    "contenu": contenu.strip()
                }).encode())

            else:
                print("Format invalide. Utilisez 'destinataire:message'")

        s.close()

if __name__ == '__main__':
    client = Client()
    client.main()