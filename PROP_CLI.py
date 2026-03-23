import socket
import threading

MAX_BYTES = 65535

def recevoir(sock):
    while True:
        try:
            data, address = sock.recvfrom(MAX_BYTES)
            print('\nMessage reçu : {}'.format(data.decode('ascii')))
        except:
            break

def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Demande le nom et s'enregistre auprès du serveur
    nom = input('Entrez votre nom : ')
    sock.sendto('REGISTER:{}'.format(nom).encode('ascii'), ('127.0.0.1', port))
    
    # Lance le thread de réception
    thread = threading.Thread(target=recevoir, args=(sock,))
    thread.daemon = True
    thread.start()
    
    print('Pour envoyer un message : TO:destinataire:message')
    print('Pour quitter : quit')
    
    while True:
        text = input()
        if text.lower() == 'quit':
            break
        # Format : "TO:Bob:Bonjour !"
        sock.sendto(text.encode('ascii'), ('127.0.0.1', port))
    
    sock.close()

if __name__ == '__main__':
    client(1060)


