import socket
import threading

def recevoir(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print('\nMessage reçu : {}'.format(data.decode('ascii')))
        except:
            break


def client(port):
    # On crée une socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # On se connecte au serveur
    sock.connect(('127.0.0.1', port))
    
    # On s'enregistre auprès du serveur
    nom = input('Entrez votre nom : ')
    sock.sendall('REGISTER:{}\n'.format(nom).encode('ascii'))
    
    # On lance le thread de réception en arrière-plan
    thread = threading.Thread(target=recevoir, args=(sock,))
    thread.daemon = True
    thread.start()
    
    print('Pour envoyer un message : TO:destinataire:message')
    print('Pour quitter : quit')
    
    while True:
        text = input()
        if text.lower() == 'quit':
            break
        sock.sendall(text.encode('ascii') + b'\n')
    
    sock.close()


if __name__ == '__main__':
    client(1060)