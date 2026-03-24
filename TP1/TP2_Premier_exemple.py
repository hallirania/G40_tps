import socket
from abc import ABC, abstractmethod

# On définit l'hôte et le port sur lesquels le serveur va écouter
HOST = '127.0.0.1'
PORT = 1060

# ABC (Abstract Base Class) permet de créer des classes abstraites
# Une classe abstraite est une classe qui ne peut pas être instanciée directement
# Elle sert de "modèle" pour les classes qui en héritent
class SocketBase(ABC):
    
    def __init__(self):
        # On crée une socket TCP (SOCK_STREAM) pour chaque instance
        # AF_INET = on utilise IPv4
        # SOCK_STREAM = on utilise TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def recv_all(self, sock, length):
        
        #Méthode commune au serveur et au client.
        #Elle permet de recevoir exactement 'length' octets depuis la socket.
        #On boucle jusqu'à avoir reçu tous les octets attendus car TCP
        #peut fragmenter les données en plusieurs paquets.
        
        data = b''  # On initialise un buffer vide en bytes
        while len(data) < length:
            # On reçoit les octets manquants
            more = sock.recv(length - len(data))
            if not more:
                # Si on ne reçoit rien, la socket a été fermée
                raise EOFError('la socket a ete fermee')
            data += more                                             # On ajoute les octets reçus au buffer
        return data

    @abstractmethod                                                  #C'est ici qu'intervient le POLYMORPHISME :
                                                                     #Server et Client ont chacun leur propre version de run(),
    def run(self):                                                   #mais on peut appeler node.run() sans savoir si c'est un serveur ou un client                       
        pass


                                        
                                       
class Server(SocketBase):                                                # La classe Server hérite de SocketBase
                                                                         # Elle redéfinit la méthode run() pour implémenter le comportement du serveur
    def run(self):
                                                                         # SO_REUSEADDR permet de réutiliser le port immédiatement
         self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # après la fermeture du serveur (évite l'erreur "Address already in use")
        
         self.sock.bind((HOST, PORT))
        
        
         self.sock.listen(1)                                                                 # On met la socket en écoute, 1 = taille de la file d'attente de connexions
        
         while True:
            print('Le serveur ecoute a cette adresse ', self.sock.getsockname())
            
            sc, sockname = self.sock.accept()                                                   # On attend qu'un client se connecte
            print('Le serveur a accepte une connection de ', sockname)                          # accept() est bloquant : il attend jusqu'à recevoir une connexion
                                                                                                # sc = socket de communication avec le client
                                                                                                # sockname = adresse du client
           
            
            
            # On reçoit exactement 9 octets (taille de "Bonjour !")
            message = self.recv_all(sc, 9)
            print('Message recu : ', message.decode('utf-8'))
            
            # On envoie la réponse au client en bytes (b'...')
            sc.sendall(b'Au revoir !')
            
            # On ferme la socket de communication avec ce client
            sc.close()
            print("Reponse envoyee, socket fermee")


# La classe Client hérite de SocketBase
# Elle redéfinit la méthode run() pour implémenter le comportement du client
class Client(SocketBase):
    
    def run(self):
        # On se connecte au serveur via son adresse et son port
        self.sock.connect((HOST, PORT))
        print('Connecte depuis ', self.sock.getsockname())
        
        # On envoie le message au serveur en bytes (b'...')
        self.sock.sendall(b'Bonjour !')
        
        # On reçoit exactement 11 octets (taille de "Au revoir !")
        reply = self.recv_all(self.sock, 11)
        print('Le serveur a repondu : ', reply.decode('utf-8'))
        
        # Fermeture de la socket
        self.sock.close()


if __name__ == '__main__':
  #Dans cette partie on peut voir le polymorphisme 
    node = Client()      #Le node peut etre soit client soit serveur et pour appeler le serveur il suffit de modifier cette commande en mettant node = Serveur () 
                         #et ensuite le mettre en client et ça nous donnera le resultat sans a avoir changer de fichier mais juste les lancer dans deux powershells differents
    node.run()