import socket
from datetime import datetime

MAX_BYTES = 65535

def client(port):
    # Création de la socket UDP (AF_INET = IPv4, SOCK_DGRAM = UDP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Prépare le message à envoyer (heure actuelle)
    text = 'Le temps est {}'.format(datetime.now())
    
    # Encode le texte en bytes ASCII avant envoi
    data = text.encode('ascii')
    
    # Envoie le message au serveur sur 127.0.0.1:port
    sock.sendto(data, ('127.0.0.1', port))
    print('mon adresse est {}'.format(sock.getsockname()))
    
    # Attend et reçoit la réponse du serveur
    data, address = sock.recvfrom(MAX_BYTES)
    
    # Décode la réponse en texte ASCII
    text = data.decode('ascii')

if __name__ == '__main__':
    client(1060)