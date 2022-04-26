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
from decimal import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
#from .payement import foo
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
#from celery import shared_task
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


 




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

class MyTokenRefreshPairView(TokenRefreshView):
	serializer_class=MyTokenObtainPairSerializer




#Verifiation du numero avant inscription
class ValidNumber(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		id=data['id']
		user=User.objects.get(id=id)
		code_id=data['code_id']
		code=int(data['code'])
		verif=PhoneVerificationCode.objects.get(id=code_id,active=True)
		if verif.code==code:
			user.active=True
			user.save()
			verif.active=False
			verif.save()
			return Response({'succes':'registration'})

	

#Inscription
class RegistrationView(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self, request):
		data=request.data
		serializer =UserSerializer(data=data)
		if serializer.is_valid():
			user=serializer.save(active=False,document_verif=False)
			code=randint(100000,999999)
			verif=PhoneVerificationCode.objects.create(user=user,code=code,active=True)
			#Envoi de code au numero
			return Response({'id':user.id,'code_id':verif.id,'prenom':user.prenom,'nom':user.nom})
		#return Response(serializer.errors)

class GetNewUser(APIView):
	permission_classes=[permissions.AllowAny]
	def post(self,request):
		id=request.data.get('id')
		user=User.objects.get(id=id,active=False)
		serializer=UserSerializer(user)
		return Response(serializer.data)



#Verification du numero de telephone en cas d oubli du mot de passe
class ResetVerification(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		phone=request.data['phone']
		client=User.objects.get(phone=phone,active=True,document_verif=True,is_staff=False)
		if client is not None:
			code=randint(100000,999999)
			verif=PhoneVerificationCode.objects.create(user=client,code=code,active=True)
			id=verif.id
			#SMS send a phone
			return Response({'id':id})

#Verification de l activite du code
class VerificationIdReset(APIView):
	permission_classes=[permissions.AllowAny]
	def post(self,request):
		id=request.data.get('id')
		verif=PhoneVerificationCode.objects.get(id=id)
		if verif.active==True:
			return Response(True)
		return Response(False)

#Verification du code
class CodeReset(APIView):
	permission_classes=[permissions.AllowAny]
	def post(self,request):
		id=request.data.get('id')
		code=int(request.data.get('code'))
		verif=PhoneVerificationCode.objects.get(id=id,active=True)
		if verif.code==code:
			return Response({'succes':'confirmation phone'})


#Changement du mot de passe
class ResetPassword(ModelViewSet):
	permission_classes = [permissions.AllowAny]
	queryset = User.objects.filter(active=True)
	serializer_class=UserSerializer
	@action(methods=["put"], detail=False, url_path='reseter')
	def modif_password(self,request,*args,**kwargs):
		data=request.data
		id=data['id']
		verif=PhoneVerificationCode.objects.get(id=id,active=True)
		if verif is not None:
			password=data['password']
			user=verif.user
			user.set_password(password)
			user.save()
			verif.active=False
			verif.save()
			return Response({'message':'donnee bien modifiee'})

	

class Authent(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		if self.request.user.is_authenticated: 
			return Response(True)
		else:
			return Response(False)

#Identifier l utilisateur connecte
class GetUser(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		if request.user.is_authenticated:
			serializer=UserSerializer(request.user)
			return Response(serializer.data)
		return Response(False)
		
#Verification de l existence du beneficiaire lors de l envoi
class VerificationCredentialsEnvoi(APIView):
	def post(self,request):
		envoyeur=request.user
		if envoyeur.active==True and envoyeur.document_verif==True:
			data=request.data
			phone_receveur=data['phone']
			getcontext().prec=2 
			somme=Decimal(data['somme'])
			frais=somme/Decimal(100)
			debit=somme+frais
			if phone_receveur!=envoyeur.phone:
				if envoyeur.solde>=debit:
					receveur=User.objects.get(phone=phone_receveur,active=True,document_verif=True)
					if receveur is not None:
						trans=VerificationTransaction.objects.create(user=envoyeur,somme=somme,
		commission=frais,phone_destinataire=phone_receveur,nature_transaction="envoi direct",total=debit)
						return Response({'id':trans.id,'nom':receveur.nom,'prenom':receveur.prenom})

#Transaction 
class GetRansactionEnvoiDirect(APIView):
	def post(self,request):
		id=request.data.get('id')
		trans=VerificationTransaction.objects.get(id=id,nature_transaction="envoi direct")
		if trans.user==request.user:
			receveur=User.objects.get(phone=trans.phone_destinataire)
			userserial=UserSerializer(receveur)
			transserial=VerificationTransactionSerializer(trans)
			return Response({'receveur':userserial.data,'transaction':transserial.data})


		
#L envoi direct en lui meme			
class EnvoyerDirect(ModelViewSet):
	queryset =VerificationTransaction.objects.all()
	serializer_class=VerificationTransactionSerializer
	@action(methods=["put"], detail=False, url_path='envoyerdirectement')
	def envoi_direct(self,request,*args,**kwargs):
		envoyeur=request.user
		if envoyeur.active==True and envoyeur.document_verif==True:
			id=request.data.get('id')
			admina=User.objects.get(phone='+79649642176')
			trans=VerificationTransaction.objects.get(id=id,nature_transaction="envoi direct")
			if trans.user==envoyeur:
				receveur=User.objects.get(phone=trans.phone_destinataire,active=True,document_verif=True)
				if receveur is not None:
					if envoyeur.solde>=trans.total:
						envoyeur.solde-=trans.total
						envoyeur.save()
						receveur.solde+=trans.somme
						receveur.save()
						admina.solde+=trans.commission
						admina.save()
						EnvoiDirectNotif(envoyeur,receveur,trans.somme,trans.commission,admina,trans.total)
						env=Envoi.objects.create(envoyeur=envoyeur,phone_receveur=receveur.phone,somme=trans.somme
						,commission=trans.commission)
						trans.delete()
						return Response({'id':env.id,'nature':"envoi direct"})
	@action(methods=["put"], detail=False, url_path='annulationenvoi')
	def anunuler_direct(self,request,*args,**kwargs):
		id=request.data.get('id')
		trans=VerificationTransaction.objects.get(id=id)
		trans.delete()
		return Response({'success':'annulation'})

							

#Recu d envoi direct 
class RecuDirect(APIView):
	def post(self,request):
		data=request.data 
		id=data['id']
		envoi=Envoi.objects.get(id=id)
		receveur=User.objects.get(phone=envoi.phone_receveur)
		receveurserializer=UserSerializer(receveur)
		if request.user==envoi.envoyeur:
			serializer=EnvoirSerializer(envoi)
			return Response({'envoi':serializer.data,'receveur':receveurserializer.data})



#Verification somme lors de l envoi par code
class VerificationSomme(APIView):
	def post(self,request):
		envoyeur=request.user
		data=request.data
		if envoyeur.active==True and envoyeur.document_verif==True:
			getcontext().prec=2
			somme=Decimal(data['somme'])
			frais=somme/Decimal(100)
			debit=somme+frais
			phone_receveur=data['phone']
			nom=data['nom']
			if envoyeur.solde>=debit:
				trans=VerificationTransaction.objects.create(user=envoyeur,somme=somme,
					commission=frais,phone_destinataire=phone_receveur,
					nature_transaction="envoi via code",
			nom_complet_destinataire=nom,total=debit)
				return Response({'id':trans.id,'nom':trans.nom_complet_destinataire})

class GetRansactionCode(APIView):
	def post(self,request):
		id=request.data.get('id')
		trans=VerificationTransaction.objects.get(id=id,nature_transaction="envoi via code")
		if trans.user==request.user:
			serializer=VerificationTransactionSerializer(trans)
			return Response(serializer.data)


#Envoi avec code directement a partir de son compte			
class EnvoiViaCodeDirect(ModelViewSet):
	queryset =VerificationTransaction.objects.all()
	serializer_class=VerificationTransactionSerializer

	@action(methods=["put"], detail=False, url_path='envoyerviacodedirectement')
	def envoi_code(self,request,*args,**kwargs):
		data=request.data
		client=request.user
		if client.active==True and client.document_verif==True:
			id=data['id']
			trans=VerificationTransaction.objects.get(id=id,nature_transaction="envoi via code")
			if trans.user==client:
				code=randint(100000000,999999999)
				admina=User.objects.get(phone='+79649642176')
				if client.solde>=trans.total:
					viacod=ViaCode.objects.create(code=code,
			Nom_complet_du_receveur=trans.nom_complet_destinataire ,client=client
			,somme=trans.somme,commission=trans.commission)
					client.solde-=trans.total
					client.save()
					admina.solde+=trans.commission
					admina.save()
					EnvoiViaCodeNotif(client,trans.somme,code,trans.commission,trans.nom_complet_destinataire,admina,trans.total)
					trans.delete()
					return Response({'id':viacod.id,'nature':"envoi via code"})

#Recu envoi par code
class RecuCode(APIView):
	def post(self,request):
		data=request.data
		id=data['id']
		envoicode=ViaCode.objects.get(id=id)
		if request.user==envoicode.client:
			serializer=ViaCodeSerializer(envoicode)
			return Response(serializer.data)

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
		messages=Messages.objects.filter(user=request.user,is_trans=True).order_by('-id')
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
		somme=Decimal(data['total'])
		client=User.objects.get(phone=phone,active=True)
		if client is not None:
			if client.solde>=somme:
				code=randint(10000,99999)
				verif=PhoneVerificationCode.objects.create(user=client,code=code,active=True)
				id=verif.id
				#CodePayementEGaalgui(client,code) 
				return Response({'id':id})


#Suppression de code en cas d annulation
class RemoveCode(ModelViewSet):
	permission_classes = [permissions.AllowAny]
	queryset = User.objects.filter(active=True)
	serializer_class=UserSerializer
	@action(methods=["put"], detail=False, url_path='coderemove')
	def remove_code(self,request,*args,**kwargs):
		id=self.request.data.get('id')
		verif=PhoneVerificationCode.objects.get(id=id)
		if verif is not None:
			verif.delete()
			return Response({'suppression':'success'})
	




#Payement gaalguishop		
class Payementgaalgui(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		code=int(request.data.get('code'))
		id=request.data.get('id')
		verif=PhoneVerificationCode.objects.get(id=id)
		if verif.code==code:
			phone=request.data.get('phone')
			user=User.objects.get(phone=phone,active=True)
			getcontext().prec=2
			to=request.data.get('total')
			total=Decimal(to)
			co=request.data.get('commission')
			commission=Decimal(co)
			li=request.data.get('livraison')
			livraison=Decimal(li)
			serializer=PayementGaalguiSerializer(data=data)
			if serializer.is_valid():
				serializer.save(user=user,active=False,total=total,commission=commission,livraison=livraison)
				pay_id=serializer.data['id']
				pay=PayementGaalgui.objects.get(id=pay_id)
				if user.solde>=pay.total:
					user.solde-=pay.total
					user.save()
					admina=User.objects.get(phone='+79649642176')
					admina.solde+=(pay.livraison+pay.commission)
					admina.save()
					pay.active=True
					pay.save()
					verif.active=False
					verif.save()
					return Response({'payement':'payement succes'})
		    #return Response(serializer.errors)




#Annulation d une commande GaalguiShop
class AnnulationCommandeGaalgui(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request):
		data=request.data
		phone=data['phone']
		getcontext().prec=2
		montant=Decimal(data['montant'])
		nom=data['nom']
		livraison=Decimal(data['livraison'])
		commission=Decimal(data['commission'])
		client=User.objects.get(phone=phone)
		client.solde+=montant
		client.save()
		admina=User.objects.get(phone='+79649642176')
		admina.solde-=(livraison+commission)
		admina.save()
		AnnulationCommandeGaalguiShopNotif(client,somme,nom)
		return Response({'message':'Annulation a succes'})


#Les dernieres transactions 
class LastMessages(APIView):
	def get(self,request): 
		messages=Messages.objects.filter(user=request.user,is_trans=True).order_by('-id')[:5]
		serializer=MessageSerializer(messages,many=True)
		return Response(serializer.data)


class GetPub(APIView):
	permission_classes=[permissions.AllowAny]
	def get(self,request):
		pub=TendancePub.objects.filter(active=True).order_by('-id')
		serializer=TendancePubSerializer(pub,many=True)
		return Response(serializer.data)





		
		


		
	
		
	
		







		


	
		



	
		

		



	
		



	
		



		

		

		

