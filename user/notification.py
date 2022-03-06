from .models import Messages
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync




def notif(user,data):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(user.group, {
    'type': 'notify',
    'value': data
    })
def notifcode(client):
    message=' Retrait de 10000 CFA pour le renouvellevement de votre compte professionnel ,solde actuel:'+ str(client.solde)
    Messages.objects.create(user=client,message=message,nature_transaction='payement')
    #notif(client,message)

def notifpayement(client):
    message=' Retrait de 10000 CFA pour le renouvellevement de votre compte professionnel ,solde actuel:'+ str(client.solde)
    Messages.objects.create(user=client,message=message,nature_transaction='payement')
    #notif(client,message)
    
def depotNotif(depositaire,somme):
    message="Depot de " + " " +  str(somme) + " " + " francs ,solde actuel:" + " " + str(depositaire.solde)+" "+"CFA"
    Messages.objects.create(user=depositaire,message=message,nature_transaction='depot',
        montant=somme)
   # notif(depositaire,message)


def RetraitNotif(beneficiaire,somme):
    message=" Retrait  de " + " " + str(somme) +" " + " francs,solde actuel:"+ " " + str(beneficiaire.solde)+" "+"CFA"
    Messages.objects.create(user=beneficiaire,message=message,nature_transaction='retrait',montant=somme)
    #notif(beneficiaire,message)

def EnvoiDirectNotif(envoyeur,receveur,somme,frais):
    messageSend="Envoi de " + " " + str(somme) + " " +  " francs a "+ " " + receveur.prenom + " " +  receveur.nom + " " + ",solde actuel:"+ " " + str(envoyeur.solde)+" "+"CFA"
    messageGet=envoyeur.prenom + " " + envoyeur.nom + " " + "vous a envoyé" + " "  + str(somme) + " " +  " francs ,solde actuel:"+ " " +  str(receveur.solde)+" "+"CFA"
    Messages.objects.create(user=receveur,message=messageGet,nature_transaction='reception',montant=somme)
    Messages.objects.create(user=envoyeur,message=messageSend,nature_transaction='envoi direct',montant=somme,
        commission=frais)


def EnvoiViaCodeNotif(envoyeur,somme,code,frais,receveur):
    message="Envoi de " + " " + str(somme) +" "+ " francs par code "+ " " +str(code)+ " " +",solde actuel:"+ " "+ str(envoyeur.solde)+" "+"CFA"
    Messages.objects.create(user=envoyeur,message=message,nature_transaction='envoi via code',montant=somme,
        code=code,commission=frais,beneficiaire=receveur)


def CodePayementEGaalgui(client,code):
    message='Votre code de verification est:'+" " + str(code)
    Messages.objects.create(user=client,message=message,nature_transaction='code')
    notif(client,message)

def PayementEgaalgui(client,somme):
    message="Achat a  Gaalgui de " + " " + str(somme) +" "+ " ,solde actuel:"+ " "+ str(client.solde)+" "+"CFA"
    Messages.objects.create(user=client,message=message,nature_transaction='payement')
    notif(client,message)







