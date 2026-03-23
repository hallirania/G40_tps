import socket
from datetime import datetime

MAX_BYTES = 65535

class Client:
    def __init__(self, port):
        # Création de la socket UDP (AF_INET = IPv4, SOCK_DGRAM = UDP)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Stocke le port du serveur
        self.port = port
    
    def run(self):
        # Prépare le message à envoyer (heure actuelle)
        text = 'Le temps est {}'.format(datetime.now())
        
        # Encode le texte en bytes ASCII avant envoi
        data = text.encode('ascii')
        
        # Envoie le message au serveur sur 127.0.0.1:port
        self.sock.sendto(data, ('127.0.0.1', self.port))
        print('mon adresse est {}'.format(self.sock.getsockname()))
        
        # Attend et reçoit la réponse du serveur
        data, address = self.sock.recvfrom(MAX_BYTES)
        
        # Décode la réponse en texte ASCII
        text = data.decode('ascii')
        print('Reponse du serveur : {}'.format(text))

if __name__ == '__main__':
    # Création de l'objet Client et envoi du message
    c = Client(1061)
    c.run()