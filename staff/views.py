from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from user.serializer import*
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import  permissions
from random import randint
from datetime import datetime
from user.models import*
from user.notification import depotNotif,RetraitNotif
import decimal
from .notif import depot,retrait,retraitcode,envoicode,comptepro
#from user.payement import actionperiodique
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from datetime import datetime, timedelta
from django.utils import timezone
import time, threading
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

#from django_celery_beat.models import PeriodicTask, IntervalSchedule



#Identification de l utilisateur
class IsStaff(APIView): 
	def get(self,request):
		staf=request.user
		if staf.is_staff==True:
			return Response(True)
		else:
			return Response(False)

#commission envoi code non inlus
class CommissionEnvoiCode(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		somme=decimal.Decimal(data['somme'])
		frais=somme/decimal.Decimal(100)
		vraifrai=round(frais,2)
		total=somme+vraifrai
		return Response({'frais':vraifrai,'total':total})

#Commission incluse
class CommissionEnvoiCodeInclus(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		somme=decimal.Decimal(data['somme'])
		frais=somme/decimal.Decimal(100)
		vraifrai=round(frais,2)
		newsomme=somme-vraifrai
		newfrais=round(newsomme/decimal.Decimal(100),2)
		total=newsomme+newfrais
		return Response({'frais':newfrais,'somme':newsomme,'total':total})

	
	
#Envoi par code 		
class EnvoiViaCodeAgence(APIView):


	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		somme=decimal.Decimal(data['somme'])
		receveur=data['Nom_complet_du_receveur']
		envoyeur=data['Nom_complet_de_l_envoyeur']
		frais=decimal.Decimal(data['frais'])
		code=randint(100000000,999999999)
		admina=User.objects.get(phone='+79649642176')
		serializer=ViaCodeSerializer(data=data)
		if serializer.is_valid():
			action='envoi  de '+ " " + str(somme )+' a ' + receveur + "par" + envoyeur + " viacode:" + str(code) 
			identifiant=request.user
			ActionStaff.objects.create(action=action,identifiant=identifiant)
			envoicode(identifiant,envoyeur,somme,code)
			admina.solde+=frais
			serializer.save(active=True,code=code)
			return Response(serializer.data)
		return Response(serializer.errors)

#Recu envoi code
class RecuViaCode(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		id=data['id']
		viacode=ViaCode.objects.get(id=id)
		frais=viacode.somme/decimal.Decimal(100)
		vraifrai=round(frais,2)
		serializer=ViaCodeSerializer(viacode)
		return Response({'viacode':serializer.data,'frais':vraifrai})



#Verification des donnees du client lors du depot
class GetClient(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		phone=request.data.get('phone')
		client=User.objects.get(phone=phone,active=True)
		serializer=UserSerializer(client)
		return Response(serializer.data)

#Depot 		
class Deposer(APIView):
	permission_classes = [permissions.IsAdminUser] 
	def post(self,request):
		data=request.data
		phone=data['phone']
		somme=decimal.Decimal(data['somme'])
		depositaire=User.objects.get(phone=phone,active=True)
		if depositaire is not None:
			serializer=DepotSerializer(data=data)
			if serializer.is_valid():
				depositaire.solde+=somme
				depositaire.save()
				action='depot de '+ " " + str(somme) +' ' + " par" + depositaire.prenom +" " + depositaire.nom
				notification='une notification'
				identifiant=request.user
				ActionStaff.objects.create(action=action,identifiant=identifiant)
				#depotNotif(depositaire,somme)
				depot(identifiant,depositaire,somme)
				depotNotif(depositaire,somme)
				serializer.save(depositaire=depositaire)
				return Response(serializer.data)

class RecuDepot(APIView):
	permission_classes = [permissions.IsAdminUser] 

	def post(self,request):
		data=request.data
		id=data['id']
		depot=Depot.objects.get(id=id)
		serializer=DepotSerializer(depot)
		return Response(serializer.data)


#Identification du client lors du retrait
class VerificationCredentialsRetrait(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		phone=request.data.get('phone')
		somme=decimal.Decimal(request.data.get('somme'))
		client=User.objects.get(phone=phone,active=True)
		if client.solde>=somme:
			serializer=UserSerializer(client)
			return Response(serializer.data)

#Retrait
class Retirer(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		phone=data['phone']
		somme=decimal.Decimal(data['somme'])
		beneficiaire=User.objects.get(phone=phone,active=True)
		if beneficiaire is not None:
			if beneficiaire.solde>=somme:
				serializer=RetraitSerializer(data=data)
				if serializer.is_valid():
					beneficiaire.solde-=somme
					beneficiaire.save()
					action='retrait  de '+ " " + str(somme) +' ' + " par" + beneficiaire.prenom +""+ beneficiaire.nom
					identifiant=request.user
					ActionStaff.objects.create(action=action,identifiant=identifiant)
					RetraitNotif(beneficiaire,somme)
					retrait(identifiant,beneficiaire,somme)
					serializer.save(beneficiaire=beneficiaire)
					return Response(serializer.data)
		

class RecuRetrait(APIView):
	permission_classes = [permissions.IsAdminUser] 

	def post(self,request):
		data=request.data
		id=data['id']
		retrait=Retrait.objects.get(id=id)
		serializer=RetraitSerializer(retrait)
		return Response(serializer.data)

#Retrait avec code 
class RetraitViaCode(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		code=data['code']
		transfert=ViaCode.objects.get(code=code,active=True)
		serializer=ViaCodeSerializer(transfert)
		return Response(serializer.data)

#Confirmation retrait avec code 
class CompletRetrait(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		id=request.data.get('id')
		transfert=ViaCode.objects.get(id=id,active=True)
		transfert.active=False
		transfert.save()
		receveur=transfert.Nom_complet_du_receveur
		somme=transfert.somme
		action='retrait par code   de '+ " " + str(transfert.somme) +"par"+ transfert.Nom_complet_du_receveur
		identifiant=request.user
		ActionStaff.objects.create(action=action,identifiant=identifiant)
		retraitcode(identifiant,receveur,somme)
		return Response({'id':id})

#Recu retrait avec code
class RecuRetraitCode(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		id=data['id']
		viacode=ViaCode.objects.get(id=id,active=False)
		serializer=ViaCodeSerializer(viacode)
		return Response(serializer.data)

#Dernieres operations staff
class LastMessageStaf(APIView):

	def get(self,request):
		messages=NotificationStaff.objects.filter(user=request.user).order_by('-id')[:5]
		serializer=NotificationStaffSerializer(messages,many=True)
		return Response(serializer.data)

	


#Annulation commande gaalguishop
class AnnulationCommandeGaaalgui(APIView):
	permission_classes=[permissions.AllowAny]
	def post(self,request):
		data=request.data
		phone=data['phone']
		admina=User.objects.get(phone='+79649642176')
		somme=decimal.Decimal(data['somme'])
		#numero=data['no']
		livraison=decimal.Decimal(data['livraison'])
		client=User.objects.get(phone=phone,active=True)
		client.solde+=somme
		client.save()
		admina.solde-=livraison
		admina.save()
		#action='Annulation commande Numero'+ " " + str(numero) 
		#identifiant=request.user
		#ActionStaff.objects.create(action=action,identifiant=identifiant)
		#notif push
		return Response({'message':'commande annulee'})


#Historique des transactions du personnel
class NotifStaff(APIView):
	permission_classes = [permissions.IsAdminUser]
	def get(self,request):
		user=request.user
		notif=NotificationStaff.objects.filter(user=user).order_by('-id')
		serializer=NotificationStaffSerializer(notif,many=True)
		return Response(serializer.data)

#Identification du personnel du bureau
class IsBureaucrate(APIView):
	permission_classes = [permissions.IsAdminUser]
	def get(self,request):
		user=request.user
		if user.bureaucrate==True:
			return Response(True)
		return  Response(False)

#Les adresses de point d acces 
class Adressage(APIView):
	def get(self,request):
		adress=Region.objects.all()
		serializer=RegionSerializer(adress,many=True)
		return Response(serializer.data)
	
		

#Inscripption d un compte professionnel
class ProfessionnelRegistrationView(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self, request):
		data=request.data
		phone=data['phone']
		user=User.objects.get(phone=phone)
		admina=User.objects.get(phone='+79649642176')
		region_id=data['region_id']
		region=Region.objects.get(id=region_id)
		serializer=CompteProfessionnelSerializer(data=data)
		if serializer.is_valid():
			schedule, created = IntervalSchedule.objects.get_or_create(every=5, period=IntervalSchedule.MINUTES,)
			start=timezone.now() 
			#timedelta(minutes=1)
			name= 'renouvellement du compte professionnel de '+ " " + user.prenom + str(user.id)
			PeriodicTask.objects.create(interval=schedule, name=name,task='user.views.payement',
				args=json.dumps((user.id, admina.id)),start_time=start)
			user.professionnel=True
			user.save()
			action='Creation du compte professionnel  '+ " " + str(phone) 
			identifiant=request.user
			ActionStaff.objects.create(action=action,identifiant=identifiant)
			serializer.save(user=user,active=True,adress=region)
			return Response(serializer.data)
		

class GetProfessionnels(APIView):
	permission_classes = [permissions.IsAdminUser]
	def get(self,request):
		professionnel=CompteProfessionnel.objects.all()
		serializer=CompteProfessionnelSerializer(professionnel,many=True)
		return Response(serializer.data)
	

class PayementProfessionnel(ModelViewSet):
	queryset = User.objects.filter(professionnel=True)
	serializer_class=UserSerializer
	@action(methods=["put"], detail=False, url_path='payer')
	def payement(self,request,*args,**kwargs):
		comptes=User.objects.filter(professionnel=True)
		for c in comptes:
			professionnel=CompteProfessionnel.objects.get(user=c)
			print(c.solde)
			if professionnel.created==datetime.now() - timedelta(minutes=70):
				c.solde-=100
				c.created=datetime.now()
				c.save()
			return Response({'message':'payement effectue'})
			#return Response({'message':'aucun payement'})




		
	
		

	





