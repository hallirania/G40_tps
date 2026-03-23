import socket

MAX_BYTES = 65535

class Server:
    def __init__(self, port):
        # Création de la socket UDP (AF_INET = IPv4, SOCK_DGRAM = UDP)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Attache la socket à l'adresse locale et au port donné
        self.sock.bind(('127.0.0.1', port))
        
        print('En ecoute sur {}'.format(self.sock.getsockname()))
    
    def run(self):
        # Boucle infinie pour écouter les messages
        while True:
            try:
                # Attend et reçoit un message + l'adresse de l'expéditeur
                data, address = self.sock.recvfrom(MAX_BYTES)
                
                # Décode les bytes reçus en texte ASCII
                text = data.decode('ascii')
                print('Le client {} dit {!r}'.format(address, text))
                
                # Prépare la réponse avec la taille du message reçu
                text = 'les donnees ont une taille de {} octets'.format(len(data))
                
                # Encode la réponse en bytes ASCII avant envoi
                data = text.encode('ascii')
                
                # Envoie la réponse au client
                self.sock.sendto(data, address)
                
            except ConnectionResetError:
                # Sur Windows, erreur levée quand le client ferme sa socket
                continue

if __name__ == '__main__':
    # Création de l'objet Server et lancement de l'écoute
    s = Server(1061)
    s.run()