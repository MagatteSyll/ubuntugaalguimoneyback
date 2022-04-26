from .models import Messages,NotificationAdmina
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
    Messages.objects.create(user=client,message=message,nature_transaction='payement',should_notify=True)
    #notif(client,message)

def notifpayement(client):
    message=' Retrait de 10000 CFA pour le renouvellevement de votre compte professionnel ,solde actuel:'+ str(client.solde)
    Messages.objects.create(user=client,message=message,nature_transaction='payement',should_notify=True,is_trans=True)
    #notif(client,message)
    
def depotNotif(depositaire,somme):
    message="Depot de " + " " +  str(somme) + " " + " francs ,solde actuel:" + " " + str(depositaire.solde)+" "+"CFA"
    Messages.objects.create(user=depositaire,message=message,nature_transaction='depot',
        montant=somme,should_notify=True,is_trans=True)
   # notif(depositaire,message)


def RetraitNotif(beneficiaire,somme):
    message=" Retrait  de " + " " + str(somme) +" " + " francs,solde actuel:"+ " " + str(beneficiaire.solde)+" "+"CFA"
    Messages.objects.create(user=beneficiaire,message=message,nature_transaction='retrait',montant=somme,should_notify=True,is_trans=True)
    #notif(beneficiaire,message)

def EnvoiDirectNotif(envoyeur,receveur,somme,frais,admina,total):
    messageSend="Envoi de " + " " + str(somme,) + " " +  " CFA a "+ " " + receveur.prenom + " " +  receveur.nom + " " + ",solde actuel:"+ " " + str(envoyeur.solde,)+" "+"CFA"
    messageGet=envoyeur.prenom + " " + envoyeur.nom + " " + "vous a envoyé" + " "  + str(somme,) + " " +  " francs ,solde actuel:"+ " " +  str(receveur.solde,)+" "+"CFA"
    beneficiaire=receveur.prenom+" "+ receveur.nom
    donnateur=envoyeur.prenom+" "+ envoyeur.nom
    Messages.objects.create(user=receveur,message=messageGet,nature_transaction='reception',montant=somme,
    donnateur=donnateur,should_notify=True,is_trans=True)
    Messages.objects.create(user=envoyeur,message=messageSend,nature_transaction='envoi direct',montant=somme,
        commission=frais,total=total,beneficiaire=beneficiaire,should_notify=False,is_trans=True)
    NotificationAdmina.objects.create(user=admina,somme=frais,nature='envoi direct')
    #notif(beneficiaire,messaget)


def EnvoiViaCodeNotif(envoyeur,somme,code,frais,receveur,admina,total):
    message="Envoi de " + " " + str(somme) +" "+ " francs par code "+ " " +str(code)+ " " +",solde actuel:"+ " "+ str(envoyeur.solde)+" "+"CFA"
    Messages.objects.create(user=envoyeur,message=message,nature_transaction='envoi via code',montant=somme,
        code=code,commission=frais,beneficiaire=receveur,total=total,should_notify=False,is_trans=True)
    NotificationAdmina.objects.create(user=admina,somme=frais,nature="envoi via code")


def CodePayementEGaalgui(client,code):
    message='Votre code de verification est:'+" " + str(code)
    Messages.objects.create(user=client,message=message,nature_transaction='code',should_notify=True,is_trans=True)
    notif(client,message)

def PayementEgaalgui(client,somme):
    message="Achat a  GaalguiShop de " + " " + str(somme) +" "+ " ,solde actuel:"+ " "+ str(client.solde)+" "+"CFA"
    Messages.objects.create(user=client,message=message,nature_transaction='payement',should_notify=True,
    is_trans=True)
    notif(client,message)


def AnnulationCommandeGaalguiShopNotif(client,somme,nom):
    message='Annulation de la commande  '+" "+ nom +" "+ "sur GaalguiShop + "+ " "+ str(somme)+ " "+ "solde actuel"+ " "+ str(client.solde)
    Messages.objects.create(user=client,message=message,nature_transaction="annulation commande",
should_notify=True,is_trans=False)
    notif(client,message)

def ActivationClientNotif(client):
    message="Votre compte a ete active avec succes,bienvenu dans la famille GaalguiMoney!"
    Messages.objects.create(user=client,message=message,nature_transaction="activation compte",should_notify=True,
    is_trans=False)
   # notif(client,message)







