from user.models import*
import json
#from channels.layers import get_channel_layer
#from asgiref.sync import async_to_sync





def depot(staff,client,somme):
	notifcation="Depot de " +" " + str(somme) + " " +" CFA par " + " " + client.prenom + " " + client.nom 
	NotificationStaff.objects.create(user=staff,notification=notifcation) 


def retrait(staff,client,somme):
	notifcation="retrait de " +" " + str(somme) + " " +" CFA par "+ " " +  client.prenom + " " + client.nom 
	NotificationStaff.objects.create(user=staff,notification=notifcation) 

def retraitcode(staff,receveur,somme):
	notifcation="retrait par code de  " +" " + str(somme) + " " +" CFA par " + " " + receveur
	NotificationStaff.objects.create(user=staff,notification=notifcation) 

def envoicode(staff,envoyeur,somme,code):
	notifcation="envoi via code:" +" " + str(code) + " "+"de" + " " + str(somme) + " " +" CFA par " + " "+ envoyeur
	NotificationStaff.objects.create(user=staff,notification=notifcation) 

def comptepro(staff,prenom,nom):
	notifcation="Creation du compte professionnel de " +" " +prenom + " " + nom
	NotificationStaff.objects.create(user=staff,notification=notifcation) 

	




	
	