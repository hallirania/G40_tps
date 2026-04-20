# EXAMEN2025
# Question 1 — Classe LeChat + Constructeur
import socket
import threading

class LeChat:
    def __init__(self, max_client, max_message_len, ip_address, port):
        self.max_client = max_client
        self.max_message_len = max_message_len
        self.ip_address = ip_address
        self.port = port
        self.clients = []           # liste des sockets clients
        self.server_socket = None
        self.total_notes = 0        # somme des notes reçues
        self.nb_notes = 0           # nombre de notes reçues

# Question 2 — manage_connexions 

 def manage_connexions(self):
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.bind((self.ip_address, self.port))
    self.server_socket.listen(self.max_client)
    while len(self.clients) < self.max_client:
        client_socket, address = self.server_socket.accept()
        self.clients.append(client_socket)
 
  t = threading.Thread(target=self.handle_client, args=(client_socket,))
  t.start()

# Question 3 — tokenizer 
 def tokenizer(self, vocab, message):
    tokens = []
    words = message.split()
    for word in words:
        if word in vocab:
            tokens.append(vocab[word])
    return tokens

# Question 4 — handle_client 
 def handle_client(self, client_socket):
    while True:
        message = client_socket.recv(self.max_message_len).decode()


  if (not message.endswith("?") or
            len(message) > self.max_message_len or
            "merci" in message):
            send(client_socket, "Texte invalide")
            continue


   tokens = self.tokenizer(vocab, message)
        response = handle_llm(tokens)
        send(client_socket, response)

# Question 5 — Évaluation + get_evaluation 
Modifications dans handle_client après l'envoi de la réponse :
 def handle_client(self, client_socket):
    while True:
        message = client_socket.recv(self.max_message_len).decode()

  if (not message.endswith("?") or
            len(message) > self.max_message_len or
            "merci" in message):
            send(client_socket, "Texte invalide")
            continue

   tokens = self.tokenizer(vocab, message)
        response = handle_llm(tokens)
        send(client_socket, response)


  note = int(client_socket.recv(1024).decode())
        if 0 <= note <= 10:
            self.total_notes += note
            self.nb_notes += 1

def get_evaluation(self):
    if self.nb_notes == 0:
        return 0
    return self.total_notes / self.nb_notes
Ajouts au constructeur pour gérer l'évaluation :
 self.total_notes = 0
self.nb_notes = 0
