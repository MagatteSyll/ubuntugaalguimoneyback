from rest_framework import serializers
from .models import*
from phonenumber_field.serializerfields import PhoneNumberField
from random import randint
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer






class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		if user.active==True:
			token = super().get_token(user)
			token['name'] = user.room
			return token

class UserSerializer(serializers.ModelSerializer):
	phone = PhoneNumberField()
	prenom= serializers.CharField()
	nom= serializers.CharField()
	password = serializers.CharField()
	class Meta:
		model=User
		fields='__all__'
		extra_kwargs = {'password': {'write_only': True}}


	def create(self, validated_data):
		password = validated_data.pop('password', None)
		instance = self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance

	def update(self, instance, validated_data):
		instance.set_password(validated_data['password'])
		instance.save()
		return instance



class EnvoirSerializer(serializers.ModelSerializer):
	envoyeur=serializers.SerializerMethodField()
	class Meta:
		model=Envoi
		fields='__all__'

	def get_envoyeur(self,obj):
		return UserSerializer(obj.envoyeur).data
		

class RetraitSerializer(serializers.ModelSerializer):
	beneficiaire=serializers.SerializerMethodField()
	class Meta:
		model=Retrait
		fields='__all__'

	def get_beneficiaire(self,obj):
		return UserSerializer(obj.beneficiaire).data


class DepotSerializer(serializers.ModelSerializer):
	depositaire=serializers.SerializerMethodField()
	class Meta:
		model=Depot
		fields='__all__'

	def get_depositaire(self,obj):
		return UserSerializer(obj.depositaire).data

		

class ViaCodeSerializer(serializers.ModelSerializer):
	code=serializers.ReadOnlyField()
	client=serializers.SerializerMethodField()
	class Meta:
		model=ViaCode
		fields='__all__'
	def get_client(self,obj):
		return UserSerializer(obj.client).data


class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model=Messages
		fields="__all__"

class PhoneVerificationCodeSerializer(serializers.ModelSerializer):
	class Meta:
		model=PhoneVerificationCode
		fields="__all__"

class PhoneConfirmationSerializer(serializers.ModelSerializer):
	class Meta:
		model=PhoneConfirmation
		fields="__all__"


class NotificationStaffSerializer(serializers.ModelSerializer):
	user=serializers.SerializerMethodField()
	class Meta:
		model=NotificationStaff
		fields="__all__"

	def get_user(self,obj):
		return UserSerializer(obj.user).data

class RegionSerializer(serializers.ModelSerializer):
	class Meta:
		model=Region
		fields="__all__"

class ActionStaffSerializer(serializers.ModelSerializer):
	class Meta:
		model=ActionStaff
		fields="__all__"

		

class CompteProfessionnelSerializer(serializers.ModelSerializer):
	user=serializers.SerializerMethodField()
	adress=serializers.SerializerMethodField()
	class Meta:
		model=CompteProfessionnel
		fields="__all__"
	def get_user(self,obj):
		return UserSerializer(obj.user).data

	def get_adress(self,obj):
		return RegionSerializer(obj.adress).data

class PayementGaalguiSerializer(serializers.ModelSerializer):
	user=serializers.SerializerMethodField()
	livraison=serializers.ReadOnlyField()
	commission=serializers.ReadOnlyField()
	class Meta:
		model=PayementGaalgui
		fields='__all__'

	def get_user(self,obj):
		return UserSerializer(obj.user).data


class VerificationTransactionSerializer(serializers.ModelSerializer):
	user=serializers.SerializerMethodField()
	class Meta:
		model=VerificationTransaction
		fields='__all__'

	def get_user(self,obj):
		return UserSerializer(obj.user).data


class TendancePubSerializer(serializers.ModelSerializer):
	class Meta:
		model=TendancePub
		fields='__all__'





	
		

	
	
		


		


		
	
	



		
