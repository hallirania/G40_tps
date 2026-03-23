import socket

MAX_BYTES = 65535

def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))
    print('En ecoute sur {}'.format(sock.getsockname()))
    
    # Dictionnaire : nom du client → adresse
    clients = {}
    
    while True:
        try:
            data, address = sock.recvfrom(MAX_BYTES)
            text = data.decode('ascii')
            
            # Si le client s'enregistre : "REGISTER:Alice"
            if text.startswith('REGISTER:'):
                nom = text.split(':')[1]
                clients[nom] = address
                print('Nouveau client enregistré : {} → {}'.format(nom, address))
                sock.sendto('Connecté en tant que {}'.format(nom).encode('ascii'), address)
            
            # Si le client envoie un message : "TO:Bob:Bonjour !"
            elif text.startswith('TO:'):
                parties = text.split(':', 2)
                destinataire = parties[1]
                message = parties[2]
                
                # Vérifie si le destinataire existe
                if destinataire in clients:
                    sock.sendto(message.encode('ascii'), clients[destinataire])
                else:
                    sock.sendto('Client {} introuvable'.format(destinataire).encode('ascii'), address)
                    
        except ConnectionResetError:
            continue

if __name__ == '__main__':
    server(1060)