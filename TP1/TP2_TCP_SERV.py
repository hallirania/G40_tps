import socket
import threading

def handle_client(sc, address, clients):
    nom = None
    try:
        while True:
            data = sc.recv(1024)
            if not data:
                break
            
            # On sépare les messages par '\n' au cas où plusieurs
            # messages arrivent dans le même paquet
            messages = data.decode('utf-8').split('\n')
            
            for text in messages:
                text = text.strip()
                if not text:
                    continue
                    
                if text.startswith('REGISTER:'):
                    nom = text.split(':')[1]
                    clients[nom] = sc
                    print('Nouveau client enregistré : {} → {}'.format(nom, address))
                    sc.sendall('Connecté en tant que {}\n'.format(nom).encode('utf-8'))
                
                elif text.startswith('TO:'):
                    parties = text.split(':', 2)
                    destinataire = parties[1]
                    message = parties[2]
                    print('{} → {} : {}'.format(nom, destinataire, message))
                    
                    if destinataire in clients:
                        clients[destinataire].sendall(
                            '{} : {}\n'.format(nom, message).encode('utf-8')
                        )
                    else:
                        sc.sendall(
                            'Client {} introuvable\n'.format(destinataire).encode('utf-8')
                        )
                        
    except ConnectionResetError:
        pass
    finally:
        if nom and nom in clients:
            del clients[nom]
            print('Client déconnecté : {}'.format(nom))
        sc.close()


def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', port))
    sock.listen(5)  # On accepte jusqu'à 5 connexions en attente
    print('En ecoute sur {}'.format(sock.getsockname()))
    
    # Dictionnaire partagé : nom du client → socket
    clients = {}
    
    while True:
        # On attend qu'un client se connecte
        sc, address = sock.accept()
        print('Nouvelle connexion de {}'.format(address))
        
        # On crée un thread pour gérer ce client indépendamment des autres
        thread = threading.Thread(target=handle_client, args=(sc, address, clients))
        thread.daemon = True
        thread.start()


if __name__ == '__main__':
    server(1060)