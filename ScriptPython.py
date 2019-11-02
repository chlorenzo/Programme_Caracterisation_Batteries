#Ce script permet de récupérer une valeur sur le port série, de stocker cette valeur  dans un fichier texte et de renvoyer un nombre.
#Ce ficher texte est appelé batteryData2.txt et se situe dans le dossier PythonTests
#situé dans le répertoire C. Le path est à modifier si nécessaire.
#Deux librairies sont à télecharger, pyserial et binascii.
#La première permet la lecture sur le port série, la seconde permet de convertir la mesure en entier.
#Le port ici COM5 doit être modifié.

#Pour ce test : pyserial récupère la valeur envoyée sur le port série, l'incrémente de 1 et la renvoie.
#Au bout de 10 itérations le script s'arrête.


#Bibliothèques à importer.
#pyserial et binascii sont à installé. Os présent par défaut.
import serial
import os
import binascii
import time
from openpyxl import Workbook
os.chdir("C:/PythonTests")      #choix du répertoir de travail.

tension_Max = 4200
tension_Min = 3000
TensionShuntIntMin = 130
TensionShuntIntMax = -130



T_init = time.time()
wb = Workbook()
ws = wb.active
ws['A1'] = "Données de tension et de tension shunt "
ws['A2'] = "Time (s)"
ws['B2'] = "BusVoltage (V)"
ws['C2'] = "ShuntVoltage (V)"
ws['D2'] = "SourceCommande A"
ws['E2'] = "SourceCommande A"

i = 0
j = 0
ser = serial.Serial('COM12', baudrate = 115200)                                    #Definition du port serie à lire ainsi que de la vitesse de transmisson.

#On commence par charger la batterie à 1C. CourantCharge = 650 mAh

DAC_A = bytes([162])            #On convertit la valeur souhaitée en byte.
DAC_B = bytes([0])            #On convertit la valeur souhaitée en byte. 

while time.time() -  T_init < 3*3600 :                                                                      #Récupération de 10 données avant d'intérrompre le script

##########################        
#  Test de la reception  #
##########################

    i+=1
    donneeRecues = ser.read(4)                       #Lecture de la donnee recue sur le port série
    TensionBusByte = donneeRecues[:2]
    TensionShuntByte = donneeRecues[2:4]                      #Lecture de la donnee recue sur le port série

    TensionBusHexa = binascii.hexlify(TensionBusByte) #Conversion de la donnée recue d'ascii en hexa
    TensionShuntHexa = binascii.hexlify(TensionShuntByte)
    TensionBusInt = int(TensionBusHexa, 16)       #Conversion de la donnee recue en hexa en int.
    TensionShuntInt = int(TensionShuntHexa, 16)       #Conversion de la donnee recue en hexa en int.


    if TensionShuntInt > 32768 :
        TensionShuntInt = (TensionShuntInt - 65536)

    TensionBusInt -= TensionShuntInt*0.01
    
    TensionBus = str(TensionBusInt)
    TensionShunt = str(TensionShuntInt)            #Conversion en str pour pouvoir l'ecrire dans le fichier
    
    TempsInt = time.time()
    Temps = round(TempsInt - T_init, 2)
 
    print(TensionBus)
    print(TensionShunt)
     
      
    ser.write(DAC_A)                           #On envoit le byte qui a ete converti.
    ser.write(DAC_B)
    
	#Si la tension mesuree depasse la tensionSeuil max :  on réduit le courant.
    if TensionBusInt >= tension_Max :  
        if TensionShuntInt >= TensionShuntIntMin and int(binascii.hexlify(DAC_A),16) > 5:
            DAC_AHexa = binascii.hexlify(DAC_A)
            DAC_AInt = int(DAC_AHexa, 16)
            DAC_A = bytes([DAC_AInt - 5])
            DAC_B = bytes([0])
        #Si on depasse le seuil limite pour le courant : on passe a  la decharge.
        else :
            DAC_A = bytes([0])
            DAC_B = bytes([170])
	#En decharge 
		#Si on dépasse le seuil min de la tension : on augmente le courant.

    elif TensionBusInt <= tension_Min:
        if TensionShuntInt <= TensionShuntIntMax and int(binascii.hexlify(DAC_B),16) > 5 :
            DAC_BHexa = binascii.hexlify(DAC_B)
            DAC_BInt = int(DAC_BHexa, 16)
            DAC_B = bytes([DAC_BInt - 5])
            DAC_A = bytes([0])
	#Si on depasse le seuil min de courant : on passe a la charge.
        else :
            DAC_A = bytes([162])
            DAC_B = bytes([0])


    DAC_A_STR = str(int(binascii.hexlify(DAC_A),16))
    DAC_B_STR = str(int(binascii.hexlify(DAC_B),16))
    ws.append([Temps, TensionBus, TensionShunt, DAC_A_STR, DAC_B_STR])                            #Ecriture dans le fichier texte.

wb.save("DonneesBatteries.xlsx")
ser.close()                                         #a la fin de la boucle While, on ferme le fichier.


