import socket
import argparse
import sys
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
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))
        self.sock.listen(1)
        
        while True:
            print('Le serveur ecoute a cette adresse ', self.sock.getsockname())
            sc, sockname = self.sock.accept()
            print('Le serveur a accepte une connection de ', sockname)
            
            # On reçoit le message du client (on ne connait pas sa taille à l'avance)
            message = sc.recv(1024)
            print('Message recu : ', message.decode('utf-8'))
            
            sc.sendall(b'Au revoir !')
            sc.close()
            print("Reponse envoyee, socket fermee")


class Client(SocketBase):
    
    def run(self):
        self.sock.connect((HOST, PORT))
        print('Connecte depuis ', self.sock.getsockname())
        
        # On demande à l'utilisateur de taper son message avec sys.stdin
        sys.stdout.write("Entrez votre message : ")
        sys.stdout.flush()
        message = sys.stdin.readline().strip()
        
        # On encode le message en bytes avant de l'envoyer
        self.sock.sendall(message.encode('utf-8'))
        
        reply = self.recv_all(self.sock, 11)
        print('Le serveur a repondu : ', reply.decode('utf-8'))
        self.sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Programme TCP - Serveur ou Client')
    parser.add_argument('role', choices=['server', 'client'],
                        help='Choisir le role : server ou client')
    args = parser.parse_args()

    if args.role == 'server':
        node = Server()
    else:
        node = Client()
    
    node.run()