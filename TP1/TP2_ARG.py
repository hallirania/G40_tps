import socket
import argparse
from abc import ABC, abstractmethod

HOST = '127.0.0.1'
PORT = 1060

class SocketBase(ABC):
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def recv_all(self, sock, length):
       
        data = b''
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError('la socket a ete fermee')
            data += more
        return data

    @abstractmethod
    def run(self):
        pass


class Server(SocketBase):
    
    def run(self):
        # SO_REUSEADDR permet de réutiliser le port immédiatement
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))
        self.sock.listen(1)
        
        while True:
            print('Le serveur ecoute a cette adresse ', self.sock.getsockname())
            sc, sockname = self.sock.accept()
            print('Le serveur a accepte une connection de ', sockname)
            message = self.recv_all(sc, 9)
            print('Message recu : ', message.decode('utf-8'))
            sc.sendall(b'Au revoir !')
            sc.close()
            print("Reponse envoyee, socket fermee")


class Client(SocketBase):
    
    def run(self):
        self.sock.connect((HOST, PORT))
        print('Connecte depuis ', self.sock.getsockname())
        self.sock.sendall(b'Bonjour !')
        reply = self.recv_all(self.sock, 11)
        print('Le serveur a repondu : ', reply.decode('utf-8'))
        self.sock.close()


if __name__ == '__main__':
    # On crée le parser argparse avec une description du programme
    parser = argparse.ArgumentParser(description='Programme TCP - Serveur ou Client')
    
    # On ajoute un argument 'role' qui peut valoir 'server' ou 'client'
    # C'est un argument obligatoire
    parser.add_argument('role', choices=['server', 'client'], 
                        help='Choisir le role : server ou client')
    
    # On parse les arguments donnés en ligne de commande
    args = parser.parse_args()
    
    # Selon le role choisi, on instancie la bonne classe
    if args.role == 'server':
        node = Server()
    else:
        node = Client()
    
   
    node.run()