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
from user.notification import depotNotif,RetraitNotif,ActivationClientNotif
from decimal import*
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
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		if request.user.is_authenticated:
			staf=request.user
			if staf.is_staff==True:
				return Response(True)
			else:
				return Response(False)
		return Response(False)

###1 Envoi via code
#Commission incluse
class CommissionEnvoiCodeInclus(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		#getcontext().prec=2
		somme=Decimal(data['somme'])
		commission=somme/Decimal(100)
		montant=somme-commission 
		commission_envoi=montant/Decimal(100)
		total=montant+commission_envoi
		reste=somme-total
		trans=VerificationTransaction.objects.create(
		nom_complet_destinataire=data['receveur'],nom_complet_client=data['envoyeur'],somme=montant,
		commission=commission_envoi,nature_transaction="envoi via code",
		phone_destinataire=data['phone'],commission_incluse=True,
		reste=reste,staf_id=request.user.id)
		return Response({'id':trans.id,'nature':trans.nature_transaction})

#Commission non incluse
class CommissionEnvoiCodeNonIncluse(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		#getcontext().prec=2
		somme=Decimal(data['somme'])
		commission=somme/Decimal(100)
		total=somme+commission
		trans=VerificationTransaction.objects.create(
		nom_complet_destinataire=data['receveur'],nom_complet_client=data['envoyeur'],somme=somme,
		commission=commission,nature_transaction="envoi via code",
		phone_destinataire=data['phone'],staf_id=request.user.id,total=total,commission_incluse=False)
		return Response({'id':trans.id,'nature':trans.nature_transaction})

#Recu envoi code
class RecuViaCode(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		id=data['id']
		viacode=ViaCode.objects.get(id=id,staf_id=request.user.id)
		serializer=ViaCodeSerializer(viacode)
		return Response(serializer.data)


###Depot
#Verification des donnees du client lors du depot
class GetClientDepot(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		phone=request.data.get('phone')
		client=User.objects.get(phone=phone,active=True,document_verif=True)
		if client is not None:
			getcontext().prec=2
			somme=Decimal(request.data.get('somme'))
			trans=VerificationTransaction.objects.create(user=client,somme=somme,commission=0,
		nature_transaction="depot",staf_id=request.user.id)
			return Response({'depot':trans.id,'nature':trans.nature_transaction})

#Recu Depot
class RecuDepot(APIView):
	permission_classes = [permissions.IsAdminUser] 
	def post(self,request):
		data=request.data
		id=data['id']
		depot=Depot.objects.get(id=id,staf_id=request.user.id)
		serializer=DepotSerializer(depot)
		return Response(serializer.data)

## 3 Retrait simple 
#Identification du client lors du retrait
class GetClientRetrait(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		phone=request.data.get('phone')
		somme=Decimal(request.data.get('somme'))
		client=User.objects.get(phone=phone,active=True,document_verif=True)
		if client.solde>=somme:
			trans=VerificationTransaction.objects.create(user=client,somme=somme,
				commission=0,staf_id=request.user.id,nature_transaction="retrait")
			return Response({'retrait':trans.id,'nature':trans.nature_transaction})
#Recu Retrait
class RecuRetrait(APIView):
	permission_classes = [permissions.IsAdminUser] 
	def post(self,request):
		data=request.data
		id=data['id']
		retrait=Retrait.objects.get(id=id,staf_id=request.user.id)
		serializer=RetraitSerializer(retrait)
		return Response(serializer.data)

###4 Retrait avec code
#Verification code lors du retrait
class RetraitViaCode(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		code=int(data['code'])
		transfert=ViaCode.objects.get(code=code,active=True)
		if transfert is not None:
			trans=VerificationTransaction.objects.create(
	nom_complet_destinataire=transfert.Nom_complet_du_receveur,
	nom_complet_client=transfert.Nom_complet_de_l_envoyeur,somme=transfert.somme,
	commission=0,staf_id=request.user.id,nature_transaction="retrait par code",code=transfert.code)
		return Response({'id':trans.id,'nature':trans.nature_transaction})


#Recu retrait avec code
class RecuRetraitCode(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		data=request.data
		id=data['id']
		viacode=ViaCode.objects.get(id=id,active=False)
		serializer=ViaCodeSerializer(viacode)
		return Response(serializer.data)

#GetTransaction donnee
class GetRansaction(APIView):
	permission_classes = [permissions.IsAdminUser]
	def post(self,request):
		id=request.data.get('id')
		trans=VerificationTransaction.objects.get(id=id,staf_id=request.user.id)
		serializer=VerificationTransactionSerializer(trans)
		return Response(serializer.data)


class LesTransactions(ModelViewSet):
	permission_classes = [permissions.IsAdminUser]
	queryset=VerificationTransaction.objects.all()
	serializer_class=VerificationTransactionSerializer
	@action(methods=["put"], detail=False, url_path='deposer')
	def depot(self,request,*args,**kwargs):
		id=request.data.get('id')
		trans=VerificationTransaction.objects.get(id=id,staf_id=request.user.id)
		if trans is not None:
			user=trans.user
			if user.active==True and user.document_verif==True:
				user.solde+=trans.somme
				user.save()
				dep=Depot.objects.create(depositaire=user,somme=trans.somme,staf_id=request.user.id)
				action='Depot de ' +" "+ str(trans.somme) +" "+ "sur le compte numero"+ " "+ str(user.id)
				identifiant=request.user
				ActionStaff.objects.create(action=action,identifiant=identifiant)
				depotNotif(user,trans.somme)
				trans.delete()
				return Response({'id':dep.id,'nature':"depot"})
	@action(methods=["put"], detail=False, url_path='retirer')
	def retirer(self,request,*args,**kwargs):
		id=request.data.get('id')
		trans=VerificationTransaction.objects.get(id=id,staf_id=request.user.id)
		if trans is not None:
			user=trans.user
			if user.active==True and user.document_verif==True:
				user.solde-=trans.somme
				user.save()
				retait=Retrait.objects.create(beneficiaire=user,somme=trans.somme,staf_id=request.user.id)
				action='Retrait de ' +" "+ str(trans.somme) +" "+ "sur le compte numero"+ " "+ str(user.id)
				identifiant=request.user
				ActionStaff.objects.create(action=action,identifiant=identifiant)
				RetraitNotif(user,trans.somme)
				trans.delete()
				return Response({'id':retait.id,'nature':"retrait"})

	@action(methods=["put"], detail=False, url_path='retirercode')
	def retirer_code(self,request,*args,**kwargs):
		code=request.data.get('code')
		id=request.data.get('id')
		transfert=ViaCode.objects.get(code=code,active=True)
		trans=VerificationTransaction.objects.get(id=id,staf_id=request.user.id)
		transfert.active=False
		transfert.save()
		trans.delete()
		return Response({"id":transfert.id,"nature":"retrait par code"})

	@action(methods=["put"], detail=False, url_path='envoyerviacode')
	def envoyercode(self,request,*args,**kwargs):
		id=request.data.get('id')
		trans=VerificationTransaction.objects.get(id=id,staf_id=request.user.id)
		if trans is not None:
			code=randint(100000000,999999999)
			vicode=ViaCode.objects.create(Nom_complet_du_receveur=trans.nom_complet_destinataire
				,Nom_complet_de_l_envoyeur=trans.nom_complet_client,somme=trans.somme,
	staf_id=request.user.id,phone_beneficiaire=trans.phone_destinataire,commission=trans.commission,
	active=True,code=code)
			action='Envoi via code de  ' +" "+ str(trans.somme) +" "+ "code"+ " "+ str(code)
			identifiant=request.user
			ActionStaff.objects.create(action=action,identifiant=identifiant)
			admina=User.objects.get(phone="+79649642176")
			NotificationAdmina.objects.create(user=admina,somme=trans.commission,nature="envoi via code")
			admina.solde+=trans.commission
			admina.save()
			trans.delete()
			return Response({'id':vicode.id,'nature':"envoi via code"})
	
####Activation d un client 
class VerificationPourActivation(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		phone=request.data.get('phone')
		user=User.objects.get(phone=phone,active=True,document_verif=False)
		if user is not None:
			return Response({'polza':user.id,'prenom':user.prenom,'nom':user.nom})

class GetPolza(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		id=request.data.get('id')
		user=User.objects.get(id=id,active=True,document_verif=False)
		if user is not None:
			serializer=UserSerializer(user)
			return Response(serializer.data)

class ActivationDuClient(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		id=request.data.get('id')
		user=User.objects.get(id=id,active=True,document_verif=False)
		nature=request.data.get('nature')
		numero=request.data.get('numero')
		user.nature_document=nature
		user.numero_document=numero
		user.document_verif=True
		user.save()
		action='Activation de l utilisateur numero '+ " "+ str(user.id)
		identifiant=request.user
		ActionStaff.objects.create(action=action,identifiant=identifiant)
		ActivationClientNotif(user)
		return Response({'success':'activation'})


class GetClientDesactivation(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		if request.user.bureaucrate:
			phone=request.data.get('phone')
			user=User.objects.get(phone=phone,active=True)
			if user is not None:
				return Response({'polza':user.id,'prenom':user.prenom,'nom':user.nom})

class ConfirmationDesactivation(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		if request.user.bureaucrate:
			id=request.data.get('id')
			user=User.objects.get(id=id,active=True)
			serializer=UserSerializer(user)
			return Response(serializer.data)


class DesactivationDuClient(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		if request.user.bureaucrate:
			id=request.data.get('id')
			user=User.objects.get(id=id,active=True)
			user.active=False
			user.save()
			motif=request.data.get('motif')
			action="desactivation du compte numero"+" "+ str(user.id) +" "+ "pour motif"+ " "+ motif 
			identifiant=request.user
			ActionStaff.objects.create(action=action,identifiant=identifiant)
			return Response({'success':'desactivation'})

class VerifyClientReactivation(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		if request.user.bureaucrate:
			phone=request.data.get('phone')
			user=User.objects.get(phone=phone,active=False)
			if user is not None:
				return Response({'polza':user.id,'prenom':user.prenom,'nom':user.nom})

class GetClientReactivation(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		if request.user.bureaucrate:
			id=request.data.get('id')
			user=User.objects.get(id=id,active=False)
			serializer=UserSerializer(user)
			return Response(serializer.data)

class ConfirmationReactivation(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		if request.user.bureaucrate:
			id=request.data.get('id')
			user=User.objects.get(id=id,active=False)
			user.active=True
			user.save()
			action="Reactivation du compte  numero "+" "+ str(user.id) 
			identifiant=request.user
			ActionStaff.objects.create(action=action,identifiant=identifiant)
			return Response({'success':'reactivation'})

class VerificationNouvelMembreStaf(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		if request.user.bureaucrate and request.user.manager:
			phone=request.data.get('phone')
			user=User.objects.get(phone=phone,active=True,is_staff=False)
			if user is not None:
				return Response({'polza':user.id,'prenom':user.prenom,'nom':user.nom})

class GetClientNouvelMembreStaf(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		if request.user.bureaucrate and request.user.manager:
			id=request.data.get('id')
			user=User.objects.get(id=id,active=True,is_staff=False)
			if user is not None:
				serializer=UserSerializer(user)
				return Response(serializer.data)

class ConfirmationStaffSimple(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		if request.user.bureaucrate and request.user.manager:
			id=request.data.get('id')
			user=User.objects.get(id=id,active=True,is_staff=False)
			user.is_staff=True
			user.save()
			action="Ajout au staff simple de l utilisateur  "+" "+ str(user.id) 
			identifiant=request.user
			ActionStaff.objects.create(action=action,identifiant=identifiant)
			return Response({'success':'ajout staff'})


class ConfirmationStaffBureau(APIView):
	permission_classes=[permissions.IsAdminUser]
	def post(self,request):
		if request.user.bureaucrate and request.user.manager:
			id=request.data.get('id')
			user=User.objects.get(id=id,active=True,is_staff=False)
			user.is_staff=True
			user.bureaucrate=True
			user.save()
			action="Ajout au staff simple bureau de l utilisateur  "+" "+ str(user.id) 
			identifiant=request.user
			ActionStaff.objects.create(action=action,identifiant=identifiant)
			return Response({'success':'ajout staff'})










#Dernieres operations staff
class LastMessageStaf(APIView):
	def get(self,request):
		messages=NotificationStaff.objects.filter(user=request.user).order_by('-id')[:5]
		serializer=NotificationStaffSerializer(messages,many=True)
		return Response(serializer.data)

#Historique des transactions du personnel
class NotifStaff(APIView):
	permission_classes = [permissions.IsAdminUser]
	def get(self,request):
		user=request.user
		notif=NotificationStaff.objects.filter(user=user).order_by('-id')
		serializer=NotificationStaffSerializer(notif,many=True)
		return Response(serializer.data)


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




		
	
		

	





