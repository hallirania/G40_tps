import socket
from _thread import start_new_thread
import threading
import xml.etree.ElementTree as ET  

class Serveur:
    def __init__(self, host="", port=12345):
        self.host = host
        self.port = port
        self.print_lock = threading.Lock()
        self.clients = {}  # {socket: nom_client}

    def envoyer_liste_clients(self, c):
        if self.clients:
            liste = "Clients connectés : " + ", ".join(self.clients.values())
        else:
            liste = "Aucun client connecté pour le moment"
        c.send(liste.encode())

    def notifier_connexion(self, nom):
        message = f"{nom} a rejoint le chat !"
        for client_socket, client_nom in list(self.clients.items()):
            if client_nom != nom:
                try:
                    client_socket.send(message.encode())
                except:
                    pass

    def notifier_deconnexion(self, nom, socket_deconnectee):
        message = f"{nom} s'est déconnecté."
        for client_socket, client_nom in list(self.clients.items()):
            if client_socket != socket_deconnectee:
                try:
                    client_socket.send(message.encode())
                except:
                    pass

    def communication_client(self, c):
        nom = None
        try:
           
            c.send("Connectez-vous en envoyant votre XML.".encode())

          
            data_xml = c.recv(1024).decode().strip()
            root = ET.fromstring(data_xml)
            nom  = root.find("nom").text
            lieu = root.find("lieu").text
            date_connexion = root.find("date_connexion").text

            
            print(f"Nouveau client connecté : {nom} depuis {lieu} le {date_connexion}")

            with self.print_lock:
                self.clients[c] = nom
                self.envoyer_liste_clients(c)
                self.notifier_connexion(nom)

            while True:
                data = c.recv(1024)
                if not data:
                    break

                message = data.decode().strip()

                if message.lower() == "quit":
                    break

                if ":" in message:
                    destinataire, contenu = message.split(":", 1)
                    destinataire = destinataire.strip()
                    contenu = contenu.strip()

                    envoye = False
                    for client_socket, client_nom in list(self.clients.items()):
                        if client_nom == destinataire:
                            try:
                                client_socket.send(f"[{nom}] : {contenu}".encode())
                                envoye = True
                            except:
                                pass
                            break

                    if not envoye:
                        c.send(f"Client '{destinataire}' introuvable.".encode())
                else:
                    c.send("Format invalide. Utilisez 'destinataire:message'".encode())

        except ET.ParseError:
            
            print("Erreur : XML invalide reçu à la connexion.")
            c.send("Erreur : XML invalide.".encode())
        except ConnectionResetError:
            print(f"Connexion coupée brutalement par {nom}.")
        except Exception as e:
            print(f"Erreur avec le client {nom} : {e}")
        finally:
            with self.print_lock:
                if c in self.clients:
                    nom_client = self.clients[c]
                    del self.clients[c]
                    self.notifier_deconnexion(nom_client, c)
                    print(f"{nom_client} s'est déconnecté.")
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