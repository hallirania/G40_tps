# TP0
1.1-Le script server.py :

Import de la librairie socket

Création de la socket UDP

Bind sur 127.0.0.1:1060 → Le serveur réserve ce port pour écouter

Affiche "En ecoute sur ('127.0.0.1', 1060)"

Boucle infinie :

Attend un message du client
↓
Reçoit les bytes + adresse du client
↓
Décode les bytes → texte ASCII
↓
Affiche : "Le client X dit 'message'"
↓
Calcule la taille du message en octets
↓
Encode la réponse en bytes
↓
Envoie la réponse au client

1.2 Le script client.py :

Import de la librairie socket et datetime

Création de la socket UDP

Prépare le message : → "Le temps est 2026-03-23 15:30:02.422067"

Encode le message en bytes ASCII

Envoie le message au serveur sur 127.0.0.1:1060

Affiche son adresse locale : "mon adresse est ('0.0.0.0', XXXXX)"

Attend la réponse du serveur

Reçoit et décode la réponse : → "les donnees ont une taille de 39 octets"

La communication entre eux se présente comme suit :

CLIENT SERVEUR │ │ │ "Le temps est 2026-03-23" │ │ ─────────────────────────────► │ │ │ Affiche le message │ │ Calcule la taille │ "les donnees ont une │ │ taille de 39 octets" │ │ ◄───────────────────────────── │ │ │ FIN Continue à écouter

Les différentes fonctions utilisées sont : socket.socket() => Crée la socket UDP sock.bind() => Attache la socket à une adresse et un port sock.recvfrom() => Reçoit un message + l'adresse de l'expéditeur sock.sendto() => Envoie un message vers une adresse sock.getsockname() => Retourne l'adresse locale de la socket .encode() => Convertit un string en bytes avant envoi .decode() => Convertit les bytes reçus en string

Les inconvenients de l'architecture Communication via client :

Le serveur est un point central de défaillance : Si le serveur tombe, tous les clients perdent la connexion Aucune communication n'est possible sans le serveur

Le serveur est un goulot d'étranglement: Tous les messages passent par le serveur Avec beaucoup de clients, le serveur peut être surchargé

Pas de communication directe entre clients: L s clients ne se parlent pas directement Chaque message fait un aller-retour inutile par le serveur

Pas de sécurité: Les messages ne sont pas chiffrés Le serveur peut lire tous les messages N'importe qui peut se connecter

UDP n'est pas fiable: Les messages peuvent être perdus Les messages peuvent arriver dans le désordre Pas de confirmation de réception
