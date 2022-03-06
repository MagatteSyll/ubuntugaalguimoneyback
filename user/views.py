from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import*
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import  permissions
from random import randint
from .models import User
from .notification import EnvoiDirectNotif,EnvoiViaCodeNotif ,PayementEgaalgui,CodePayementEGaalgui,notifpayement
from rest_framework import filters
#import requests
import decimal
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
#from .payement import foo
from rest_framework_simplejwt.views import TokenObtainPairView
#from celery import shared_task
from django.http import HttpResponse


 




'''@shared_task
def payement(upk,adpk):
	user=User.objects.get(id=upk)
	admina=User.objects.get(id=adpk)
	user.solde-=10000
	user.save()
	admina.solde+=10000
	admina.save()
	notifpayement(user)'''

def index(request):
	return HttpResponse('hello')
	

class MyTokenObtainPairView(TokenObtainPairView):
	serializer_class = MyTokenObtainPairSerializer



#Verifiation du numero avant inscription
class ValidNumber(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		phone=data['phone']
		try:
			user=User.objects.get(phone=phone)
		except User.DoesNotExist:
			code=randint(10000,99999)
			phoneconfir=PhoneConfirmation.objects.create(phone=phone,code=code)
			id=phoneconfir.id
			#code telephone
			return Response({'id':id})

	

#Inscription
class RegistrationView(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self, request):
		data=request.data
		id=data['id']
		code=int(data['code'])
		verif=PhoneConfirmation.objects.get(id=id)
		if verif.code==code:
			serializer =UserSerializer(data=data)
			if serializer.is_valid():
				user=serializer.save()
				return Response({'message':'utilisateur bien cree'})
			return Response(serializer.errors)



#Verification du numero de telephone en cas d oubli du mot de passe
class ResetVerification(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		phone=request.data['phone']
		client=User.objects.get(phone=phone,active=True)
		if client is not None:
			code=randint(10000,99999)
			verif=PhoneVerificationCode.objects.create(user=client,code=code,active=True)
			id=verif.id
			#SMS send a phone
			return Response({'id':id})

#Confiramtion du telephone lors du reset password
class VerificationCodeReset(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		code=int(data['code'])
		id=data['id']
		verif=PhoneVerificationCode.objects.get(id=id)
		if verif.code==code:
			return Response({'message':'verification faite'})
			

class ResetPassword(ModelViewSet):
	permission_classes = [permissions.AllowAny]
	queryset = User.objects.filter(active=True)
	serializer_class=UserSerializer
	@action(methods=["put"], detail=False, url_path='reseter')
	def modif_password(self,request,*args,**kwargs):
		data=request.data
		phone=data['phone']
		password=data['password']
		user=User.objects.get(phone=phone)
		user.set_password(password)
		#serializer.save(password=user.password)
		user.save()
		return Response({'message':'donnee bien modifiee'})

class BlacklistTokenUpdateView(APIView):
	permission_classes = [permissions.AllowAny]
	authentication_classes = ()
	def post(self, request):
		try:
			refresh_token = request.data["refresh_token"]
			token = RefreshToken(refresh_token)
			token.blacklist()
			return Response({'message':'deconnexion '})
		except Exception as e:
			return Response({'message':'erreur'})
	

class Authent(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		if request.user.is_authenticated:
			return Response(True)
		else:
			return Response(False)

#Identifier l utilisateur connecte
class GetUser(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		serializer=UserSerializer(request.user)
		return Response(serializer.data)
		
#Verification de l existence du beneficiaire lors de l envoi
class VerificationCredentialsEnvoi(APIView):
	def post(self,request):
		envoyeur=request.user
		if envoyeur.active==True:
			data=request.data
			phone_receveur=data['phone']
			somme=decimal.Decimal(data['somme'])
			frais=somme/decimal.Decimal(100)
			vraifrai=round(frais,2)
			debit=somme+vraifrai
			if phone_receveur!=envoyeur.phone:
				if envoyeur.solde>=debit:
					receveur=User.objects.get(phone=phone_receveur,active=True)
					if receveur is not None:
						serializer=UserSerializer(receveur)
						return Response({'receveur':serializer.data,'frais':vraifrai})
		
#L envoi direct en lui meme			
class EnvoyerDirect(APIView):
	def post(self,request):
		envoyeur=request.user
		if envoyeur.active==True:
			data=request.data
			admina=User.objects.get(phone='+79649642176')
			phone_receveur=data['phone_receveur']
			receveur=User.objects.get(phone=phone_receveur,active=True)
			if receveur is not None:
				somm=decimal.Decimal(data['somme'])
				frais=somm/decimal.Decimal(100)
				vraifrai=round(frais,2)
				somme=vraifrai+decimal.Decimal(somm)
				if envoyeur.solde>=somme:
					serializer=EnvoirSerializer(data=data)
					if serializer.is_valid():
						envoyeur.solde=envoyeur.solde-somme
						envoyeur.save()
						receveur.solde=receveur.solde+somm
						receveur.save()
						admina.solde=admina.solde+vraifrai
						admina.save()
						EnvoiDirectNotif(envoyeur,receveur,somm,vraifrai)
						serializer.save(envoyeur=envoyeur)
						return Response(serializer.data)

#Recu d envoi direct 
class RecuDirect(APIView):
	def post(self,request):
		data=request.data 
		id=data['id']
		envoi=Envoi.objects.get(id=id)
		receveur=User.objects.get(phone=envoi.phone_receveur)
		receveurserializer=UserSerializer(receveur)
		commission=round(envoi.somme/100,2)
		if request.user==envoi.envoyeur:
			serializer=EnvoirSerializer(envoi)
			return Response({'envoi':serializer.data,'commission':commission,'receveur':receveurserializer.data})



#Verification somme lors de l envoi par code
class VerificationSomme(APIView):
	def post(self,request):
		envoyeur=request.user
		data=request.data
		if envoyeur.active==True:
			somme=decimal.Decimal(data['somme'])
			frais=somme/decimal.Decimal(100)
			vraifrai=round(frais,2)
			debit=somme+vraifrai
			if envoyeur.solde>=debit:
				return Response({vraifrai})


#Envoi avec code directement sur son compte			
class EnvoiViaCodeDirect(APIView):
	def post(self,request):
		data=request.data
		client=request.user
		if client.active==True:
			somm=decimal.Decimal(data['somme'])
			receveur=data['Nom_complet_du_receveur']
			frais=somm/decimal.Decimal(100)
			vraifrai=round(frais,2)
			code=randint(100000000,999999999)
			admina=User.objects.get(phone='+79649642176')
			somme=decimal.Decimal(somm)+vraifrai
			if client.solde>=somme:
				serializer=ViaCodeSerializer(data=data)
				if serializer.is_valid():
					client.solde=client.solde-somme
					client.save()
					admina.solde=admina.solde+vraifrai
					admina.save()
					EnvoiViaCodeNotif(client,somm,code,vraifrai,receveur)
					serializer.save(client=client,active=True,code=code)
					return Response(serializer.data)

#Recu envoi par code
class RecuCode(APIView):
	def post(self,request):
		data=request.data
		id=data['id']
		envoicode=ViaCode.objects.get(id=id)
		commission=round(envoicode.somme/100,2)
		if request.user==envoicode.client:
			serializer=ViaCodeSerializer(envoicode)
			return Response({'envoi':serializer.data,'commission':commission})

#un recu specifique
class RecuDonne(APIView):
	def post(self,request):
		data=request.data
		id=data['id']
		message=Messages.objects.get(id=id)
		if request.user==message.user:
			serializer=MessageSerializer(message)
			return Response(serializer.data)
		
		
#les transactions de l utilisateur
class UserMessages(APIView):
	def get(self,request):
		messages=Messages.objects.filter(user=request.user).order_by('-id')
		serializer=MessageSerializer(messages,many=True)
		return Response(serializer.data)

#filtration transaction
class RechercheMessage(generics.ListAPIView):
	permission_classes = [permissions.AllowAny]
	#queryset = Messages.objects.filter(user=request.user)
	serializer_class = MessageSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = search_fields = ['^message']

	def get_queryset(self):
		user = self.request.user
		return Messages.objects.filter(user=user)
	

#Verification en cas d achat sur gaalguishop
class VerificationPhonePourPayement(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		phone=data['phone']
		somme=decimal.Decimal(data['total'])
		client=User.objects.get(phone=phone,active=True)
		if client is not None:
			if client.solde>=somme:
				code=randint(10000,99999)
				verif=PhoneVerificationCode.objects.create(user=client,code=code,active=True)
				id=verif.id
				#CodePayementEGaalgui(client,code) 
				return Response({'id':id})
	
#Payement gaalguishop		
class Payementgaalgui(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		somme=decimal.Decimal(data['total'])
		phone=data['phonegaalgui']
		code=int(data['code'])
		livraison=decimal.Decimal(data['livraison'])
		commission=decimal.Decimal(data['commission'])
		id=data['id']
		verif=PhoneVerificationCode.objects.get(id=id)
		if verif.code==code:
			verif.active=False
			verif.save()
			client=User.objects.get(phone=phone,active=True)
			if client.solde>=(somme+livraison):
				client.solde-=(somme+livraison)
				client.save()
				admina=User.objects.get(phone='+79649642176')
				admina.solde+=(livraison+commission)
				admina.save()
				PayementGaalgui.objects.create(user=client,livraison=livraison)
				#PayementEgaalgui(client,somme)
				return Response({'message':'payement reussi'})


#Annulation d une commande GaalguiShop
class AnnulationCommandeGaalgui(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		phone=data['phone']
		montant=data['montant']
		livraison=data['livraison']
		commission=data['commission']
		client=User.objects.get(phone=phone)
		client.solde+=montant
		client.save()
		admina=User.objects.get(phone='+79649642176')
		admina.solde-=(livraison+commission)
		admina.save()
		#Notification au user sur le remboursement
		return Response({'message':'Annulation a succes'})


#Les dernieres transactions 
class LastMessages(APIView):
	def get(self,request):
		messages=Messages.objects.filter(user=request.user).order_by('-id')[:5]
		serializer=MessageSerializer(messages,many=True)
		return Response(serializer.data)

#Historique d envoi direct
class HistoryEnvoiDirect(APIView):
	def get(self,request):
		messages=Messages.objects.filter(nature_transaction='envoi direct',user=request.user).order_by('-id')
		serializer=MessageSerializer(messages,many=True)
		return Response(serializer.data)

#Historique d envoi par code
class HistoryEnvoiCode(APIView):
	def get(self,request):
		messages=Messages.objects.filter(nature_transaction='envoi via code',user=request.user).order_by('-id')
		serializer=MessageSerializer(messages,many=True)
		return Response(serializer.data) 

#Historique de reception
class HistoryReception(APIView):
	def get(self,request):
		messages=Messages.objects.filter(nature_transaction='reception',user=request.user).order_by('-id')
		serializer=MessageSerializer(messages,many=True)
		return Response(serializer.data)

#Historique de payement
class HistoryPayement(APIView):
	def get(self,request):
		messages=Messages.objects.filter(nature_transaction='payement',user=request.user).order_by('-id')
		serializer=MessageSerializer(messages,many=True)
		return Response(serializer.data)

#Historique de depot
class HistoryDepot(APIView):
	def get(self,request):
		messages=Messages.objects.filter(nature_transaction='depot',user=request.user).order_by('-id')
		serializer=MessageSerializer(messages,many=True)
		return Response(serializer.data)

#Historique de retrait
class HistoryRetrait(APIView):
	def get(self,request):
		messages=Messages.objects.filter(nature_transaction='retrait',user=request.user).order_by('-id')
		serializer=MessageSerializer(messages,many=True)
		return Response(serializer.data)


#Verification du numero de telephone en cas de moification des donnees 
class VerificationPhone(APIView):
	def post(self,request):
		#phone=request.data['phone']
		client=request.user
		code=randint(10000,99999)
		verif=PhoneVerificationCode.objects.create(user=client,code=code,active=True)
		serializer=PhoneVerificationCodeSerializer(verif)
		#SMS send a phone
		return Response(serializer.data)

#Modification des donnees personnelles 
class ModificationCredential(ModelViewSet):
	queryset = User.objects.filter(active=True)
	serializer_class=UserSerializer
	@action(methods=["put"], detail=False, url_path='modif')
	def modif_cred(self,request,*args,**kwargs):
		user=self.request.user
		data=request.data
		id=data['id']
		code=int(data['code'])
		verif=PhoneVerificationCode.objects.get(id=id)
		if verif.code==code:
			user.nom=data['nom']
			user.phone=data['phone']
			user.prenom=data['prenom']
			user.save()
			return Response({'message':'donnee bien modifiee'})



		
		


		
	
		
	
		







		


	
		



	
		

		



	
		



	
		



		

		

		

