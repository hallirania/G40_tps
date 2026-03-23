# G40_tps

1.1-Le script server.py :
  1. Import de la librairie socket

  2. Création de la socket UDP
  
  3. Bind sur 127.0.0.1:1060
     → Le serveur réserve ce port pour écouter
  
  4. Affiche "En ecoute sur ('127.0.0.1', 1060)"
  
  5. Boucle infinie :
     
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
  1. Import de la librairie socket et datetime

  2. Création de la socket UDP
  
  3. Prépare le message :
     → "Le temps est 2026-03-23 15:30:02.422067"
  
  4. Encode le message en bytes ASCII
  
  5. Envoie le message au serveur sur 127.0.0.1:1060
  
  6. Affiche son adresse locale : "mon adresse est ('0.0.0.0', XXXXX)"
  
  7. Attend la réponse du serveur
  
  8. Reçoit et décode la réponse :
     → "les donnees ont une taille de 39 octets"

La communication entre eux se présente comme suit : 

CLIENT                          SERVEUR
  │                                │
  │  "Le temps est 2026-03-23"       │
  │ ─────────────────────────────► │
  │                                │ Affiche le message
  │                                │ Calcule la taille
  │  "les donnees ont une          │
  │   taille de 39 octets"         │
  │ ◄───────────────────────────── │
  │                                │
 FIN                          Continue à écouter








 
     
