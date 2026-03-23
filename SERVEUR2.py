import socket

MAX_BYTES = 65535

def server(port):
    # Création de la socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Attache la socket au port donné
    sock.bind(('127.0.0.1', port))
    print('En ecoute sur {}'.format(sock.getsockname()))
    
    # Stocke les adresses des clients connectés
    clients = []
    
    while True:
        try:
            # Reçoit un message + l'adresse de l'expéditeur
            data, address = sock.recvfrom(MAX_BYTES)
            
            # Si le client n'est pas encore enregistré, on l'ajoute
            if address not in clients:
                clients.append(address)
                print('Nouveau client connecté : {}'.format(address))
            
            # Décode le message reçu
            text = data.decode('ascii')
            print('Le client {} dit : {!r}'.format(address, text))
            
            # Renvoie le message à tous les autres clients
            for client in clients:
                if client != address:
                    sock.sendto(data, client)
                    
        except ConnectionResetError:
            # Sur Windows, erreur levée quand un client ferme sa socket
            continue

if __name__ == '__main__':
    server(1060)