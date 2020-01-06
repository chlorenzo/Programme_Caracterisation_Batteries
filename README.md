# Programme_Caracterisation_Batteries
Dans ce dossier sont partagés le dossier CCS et l'interface python pour caractériser les éléments de stockage éléctrochimique.

Le programme ScriptPython.py permet de communiquer avec le port série et de récupérer les informations transmises par le micro-controleur. 
Après traitement et stockage des données, il envoie deux octets au micro controleur. 
Ce programme est écrit pour la version 3 de Python. Plusieurs bibliothèques doivent être installées : 
La bibliothèque "serial" qui permet la communication avec le port série. La bibliothèque "binascii" qui permet de convertir facilement les données reçues. La bibliothèque "time" qui permet d'intégrer le temps dans le programme
La bibliothèque "Workbook" qui permet d'écrire des données dans des fichiers excel.

Le dossier ProjetBatterie_SCI_I2C_DAC contient le code c à téléverser sur le micro-controleur et toutes ses dépendance. Le programme a été réalisé dans le fichier "ProjetBatterie.c" . Ce fichier est à téléverser sur le micro-controleur.

Une fois le montage hardware réalisé (non alimenté) : 
1. Téléverser sur le microcontrôleur le programme "ProjetBatterie.c".
2. Une fois le téléversement terminé, lancer le script ScriptPython.py.
3. Alimenter le circuit éléctrique. 
