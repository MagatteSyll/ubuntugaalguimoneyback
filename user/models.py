from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from datetime import datetime, timedelta
from autoslug import AutoSlugField
import random
import string 


def random_string_generator(request):
    return ''.join(random.choices(string.ascii_letters , k=20))

NATURE_TRANSACTION= (
    ("envoi direct", "envoi direct"),
    ("envoi via code", "envoi via code"),
    ("depot", "depot"),
    ("retrait", "retrait"),
    ("reception", "reception"),
    ("payement", "payement"),
    ("code","code")
    )


 
#Gestion utilisateur 
class UserManager(BaseUserManager):
	def create_user(self,nom,prenom,phone,password=None,is_staff=False,is_admin=False):
		if not phone:
			raise ValueError('phone obligatoire')
		if not password:
			raise ValueError('password obligatoire')
		if not nom:
			raise ValueError('entrez un nom')
		if not prenom:
			raise ValueError('entrez un prenom')
				
		self.phone=phone		
		user = self.model(phone=phone)	
		user.set_password(password)
		user.nom=nom
		user.prenom= prenom
		user.is_staff=is_staff
		user.is_admin=is_admin
		user.save(using=self._db)
		return user

	def create_superuser(self,nom,prenom,phone,password=None):
		user=self.create_user(
			phone=phone,
			password=password,
			nom=nom,
			prenom =prenom,
			is_staff=True,is_admin=True
			)
		return user

	def create_staff(self,nom,prenom,phone,password=None):
		user=self.create_user(
			phone=phone,
			password=password,
			nom=nom,
			prenom=prenom,
			is_staff=True,is_admin=False
			)
		return user	
#Utilisateur
class User(AbstractBaseUser):
	phone = PhoneNumberField(unique=True)
	active = models.BooleanField(default=True)
	prenom = models.CharField(max_length=100)
	nom =models.CharField(max_length=100)
	conform_phone=models.BooleanField(default=False)
	date_joined=models.DateTimeField(auto_now_add=True)
	solde=models.DecimalField(default=0, max_digits=19, decimal_places=2)
	is_staff =models.BooleanField(default=False)
	is_admin=models.BooleanField(default=False)
	professionnel=models.BooleanField(default=False)
	business=models.BooleanField(default=False)
	bureaucrate=models.BooleanField(default=False)
	room=AutoSlugField(populate_from=random_string_generator,unique=True)
	group=AutoSlugField(populate_from=random_string_generator,unique=True)
	channel=AutoSlugField(populate_from=random_string_generator,unique=True)
	
	REQUIRED_FIELDS= ['prenom','nom']
	USERNAME_FIELD ='phone'
	objects=UserManager()

	def get_prenom(self):
		return self.prenom
	def get_nom(self):
		return self.nom	

	def has_perm(self,perm,obj=None):
		return True

	def has_module_perms(self,app_label):
		return True
	def __str__(self):
		return str(self.phone)
	

#Envoi direct d un utilisateur a un autre
class Envoi(models.Model):
	envoyeur=models.ForeignKey(User,on_delete=models.PROTECT)
	phone_receveur=PhoneNumberField()
	somme=models.DecimalField( max_digits=12, decimal_places=2)
	created=models.DateTimeField(auto_now_add=True)


#Depot ,agence
class Depot(models.Model):
	depositaire=models.ForeignKey(User,on_delete=models.PROTECT)
	somme=models.DecimalField( max_digits=12, decimal_places=2)
	created=models.DateTimeField(auto_now_add=True)

	

#Retrait a partir d un  compte  
class Retrait(models.Model):
	beneficiaire=models.ForeignKey(User,on_delete=models.PROTECT)
	somme=models.DecimalField( max_digits=12, decimal_places=2)
	created=models.DateTimeField(auto_now_add=True)

	

#Envoi avec code 
class ViaCode(models.Model):
	code=models.PositiveIntegerField(unique=True)
	Nom_complet_du_receveur=models.CharField(max_length=255)
	Nom_complet_de_l_envoyeur=models.CharField(max_length=255,blank=True,null=True)
	client=models.ForeignKey(User,on_delete=models.PROTECT,blank=True,null=True)
	somme=models.DecimalField( max_digits=12, decimal_places=2)
	active=models.BooleanField(default=False)
	created=models.DateTimeField(auto_now_add=True)
	phone_beneficiaire=PhoneNumberField()



class ActionStaff(models.Model):
	identifiant=models.ForeignKey(User,on_delete=models.PROTECT)
	action=models.TextField()
	created=models.DateTimeField(auto_now_add=True)

	

#Historiques transactionss
class Messages(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	message=models.TextField()
	created=models.DateTimeField(auto_now_add=True)
	nature_transaction=models.CharField(max_length=100, choices=NATURE_TRANSACTION)
	montant=models.DecimalField( max_digits=12, decimal_places=2)
	commission=models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=True)
	beneficiaire=models.CharField(max_length=200,null=True,blank=True)
	code=models.PositiveIntegerField(null=True,blank=True)



class PhoneVerificationCode(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	code=models.PositiveIntegerField(unique=True)
	created=models.DateTimeField(auto_now_add=True)
	active=models.BooleanField(default=False)


class PayementGaalgui(models.Model):
	user=models.ForeignKey(User,on_delete=models.PROTECT)
	livraison=models.DecimalField(default=0, max_digits=19, decimal_places=2)
	commission=models.DecimalField(default=0, max_digits=19, decimal_places=2)
	total=models.DecimalField(default=0, max_digits=19, decimal_places=2)
	created=models.DateTimeField(auto_now_add=True)
	active=models.BooleanField(default=True)


	
	
class PhoneConfirmation(models.Model):
	phone=PhoneNumberField()
	code=models.PositiveIntegerField(unique=True)
	created=models.DateTimeField(auto_now_add=True)



class NotificationStaff(models.Model):
	user=models.ForeignKey(User,on_delete=models.PROTECT)
	notification=models.TextField()
	created=models.DateTimeField(auto_now_add=True)

class Region(models.Model):
	region=models.CharField(max_length=100)

	

class CompteProfessionnel(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	active=models.BooleanField(default=False)
	business=models.TextField()
	adress=models.ForeignKey(Region,on_delete=models.PROTECT)
	contact=PhoneNumberField()
	logo=models.ImageField(upload_to='static/images')
	created=models.DateTimeField(auto_now_add=True)



	


	


		
	
	
		

