import socket
import threading

MAX_BYTES = 65535

def recevoir(sock):
    # Fonction qui tourne en arrière-plan pour recevoir les messages
    while True:
        try:
            data, address = sock.recvfrom(MAX_BYTES)
            text = data.decode('ascii')
            print('\nMessage reçu : {}'.format(text))
        except:
            break

def client(port, nom):
    # Création de la socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Envoie un message de connexion au serveur
    sock.sendto('{}  rejoint le chat'.format(nom).encode('ascii'), ('127.0.0.1', port))
    print('Connecté au serveur ! Vous pouvez écrire vos messages.')
    
    # Lance un thread pour recevoir les messages en arrière-plan
    thread = threading.Thread(target=recevoir, args=(sock,))
    thread.daemon = True
    thread.start()
    
    # Boucle pour envoyer des messages
    while True:
        text = input()
        if text.lower() == 'quit':
            break
        # Envoie le message au serveur avec le nom du client
        message = '{} : {}'.format(nom, text)
        sock.sendto(message.encode('ascii'), ('127.0.0.1', port))
    
    sock.close()

if __name__ == '__main__':
    # Demande le nom du client avant de se connecter
    nom = input('Entrez votre nom : ')
    client(1060, nom)