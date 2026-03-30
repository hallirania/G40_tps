import socket
import threading
import json
import xml.etree.ElementTree as ET
from datetime import date

class Client:
    def __init__(self, host='127.0.0.1', port=12345, format="json"):
        self.host = host
        self.port = port
        self.format = format  # ✅ "json" ou "xml"

    # ✅ Crée le message d'identification dans le bon format
    def creer_identification(self):
        if self.format == "json":
            return json.dumps({
                "type": "identification",
                "nom": "client1",
                "date_connexion": str(date.today()),
                "lieu": "Paris"
            }).encode()
        else:
            return f"""<identification>
    <nom>client1</nom>
    <date_connexion>{str(date.today())}</date_connexion>
    <lieu>Paris</lieu>
</identification>""".encode()

    # ✅ Crée un message chat dans le bon format
    def creer_message(self, destinataire, contenu):
        if self.format == "json":
            return json.dumps({
                "type": "message",
                "destinataire": destinataire,
                "contenu": contenu
            }).encode()
        else:
            return f"""<message>
    <destinataire>{destinataire}</destinataire>
    <contenu>{contenu}</contenu>
</message>""".encode()

    # ✅ Crée une notification d'état dans le bon format
    def creer_etat(self, etat):
        if self.format == "json":
            return json.dumps({
                "type": "notification",
                "evenement": "etat",
                "etat": etat
            }).encode()
        else:
            return f"""<notification>
    <evenement>etat</evenement>
    <etat>{etat}</etat>
</notification>""".encode()

    # ✅ Crée une notification "en train d'écrire"
    def creer_en_train_ecrire(self):
        if self.format == "json":
            return json.dumps({
                "type": "notification",
                "evenement": "en_train_ecrire"
            }).encode()
        else:
            return b"""<notification>
    <evenement>en_train_ecrire</evenement>
</notification>"""

    # ✅ Affiche les messages reçus (toujours en JSON côté serveur)
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
                msg = json.loads(data)  # le serveur répond toujours en JSON
                self.afficher_message(msg)
            except:
                break

    def main(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))

        # ── Identification (XML ou JSON selon self.format) ───
        s.send(self.creer_identification())

        thread = threading.Thread(target=self.recevoir_messages, args=(s,))
        thread.daemon = True
        thread.start()

        print(f"Format utilisé : {self.format.upper()}")
        print("Commandes disponibles :")
        print("  destinataire:message       → envoyer un message")
        print("  /etat LIBRE|OCCUPE|INACTIF → changer d'état")
        print("  quit                       → quitter\n")

        while True:
            message = input()

            if message.lower() == "quit":
                s.send("quit".encode())
                break

            elif message.startswith("/etat "):
                etat = message.split(" ", 1)[1].upper()
                s.send(self.creer_etat(etat))

            elif ":" in message:
                s.send(self.creer_en_train_ecrire())
                destinataire, contenu = message.split(":", 1)
                s.send(self.creer_message(destinataire.strip(), contenu.strip()))

            else:
                print("Format invalide. Utilisez 'destinataire:message'")

        s.close()

if __name__ == '__main__':
    # ✅ Change "json" par "xml" pour tester l'autre format !
    client = Client(format="json")
    client.main()