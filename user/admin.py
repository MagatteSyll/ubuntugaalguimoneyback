from django.contrib import admin
from .models import*




class UserAdmin(admin.ModelAdmin):
	list_display=['prenom', 'nom', 'phone','solde', 'active', 'professionnel', 'business', 'is_staff', 'bureaucrate',]
	search_fields=['prenom','nom', 'phone']
	class Meta:
		model=User

class EnvoiAdmin(admin.ModelAdmin):
	list_display=['envoyeur','somme','phone_receveur']
	list_display_links =[  'envoyeur']
	search_fields=['envoyeur__prenom']
	class Meta:
		model=Envoi

class DepotAdmin(admin.ModelAdmin):
	list_display=['depositaire','somme',]
	list_display_links =[ 'depositaire']
	search_fields=['depositaire__prenom']
	class Meta:
		model=Depot

class RetraitAdmin(admin.ModelAdmin):
	list_display=['beneficiaire','somme',]
	list_display_links =['beneficiaire']
	search_fields=['beneficiaire__prenom' ]
	class Meta:
		model=Retrait

class ViaCodeAdmin(admin.ModelAdmin):
	list_display=['Nom_complet_du_receveur', 'somme','code']
	search_fields=['Nom_complet_du_receveur','code']
	class Meta:
		model=ViaCode

class ActionStaffAdmin(admin.ModelAdmin):
	list_display=['identifiant', 'created',]
	search_fields=['identifiant__prenom' ]
	list_display_links =['identifiant']
	class Meta:
		model=ActionStaff


class MessagesAdmin(admin.ModelAdmin):
	list_display=['user', 'nature_transaction',]
	search_fields=[ 'user__prenom' ]
	list_display_links =[ 'user']
	class Meta:
		model=Messages

class PhoneVerificationEnModifiantAdmin(admin.ModelAdmin):
	list_display=[ 'user','code','active']
	search_fields=['user__prenom' ]
	list_display_links =[ 'user']
	class Meta:
		model=PhoneVerificationCode

class PayementGaalguiShopAdmin(admin.ModelAdmin):
	list_display=['user','livraison']
	search_fields=['user__prenom' ]
	list_display_links =['user']
	class Meta:
		model=PhoneVerificationCode

class RegionAdmin(admin.ModelAdmin):
	list_display=['region']
	search_fields=['region' ]
	class Meta:
		model=Region

class PhoneConfirmationInscriptionAdmin(admin.ModelAdmin):
	list_display=['phone','code',]
	search_fields=['phone' ]
	class Meta:
		model=PhoneConfirmation

class NotificationStaffAdmin(admin.ModelAdmin):
	list_display=['user',]
	search_fields=['user__prenom' ]
	list_display_links =[ 'user']
	class Meta:
		model=NotificationStaff

class CompteProfessionnelAdmin(admin.ModelAdmin):
	list_display=['user','business','created']
	search_fields=['user__prenom' ]
	list_display_links =['user']
	class Meta:
		model=CompteProfessionnel

class RegionAdmin(admin.ModelAdmin):
	list_display=['region']
	search_fields=['region' ]
	class Meta:
		model=Region




admin.site.register(User,UserAdmin)
admin.site.register(Envoi,EnvoiAdmin)
admin.site.register(Depot,DepotAdmin)
admin.site.register(Retrait,RetraitAdmin)
admin.site.register(ViaCode,ViaCodeAdmin)
admin.site.register(ActionStaff,ActionStaffAdmin)
admin.site.register(Messages,MessagesAdmin)
admin.site.register(PhoneVerificationCode,PhoneVerificationEnModifiantAdmin)
admin.site.register(PayementGaalgui,PayementGaalguiShopAdmin)
admin.site.register(PhoneConfirmation,PhoneConfirmationInscriptionAdmin)
admin.site.register(NotificationStaff,NotificationStaffAdmin)
admin.site.register(CompteProfessionnel,CompteProfessionnelAdmin)
admin.site.register(Region,RegionAdmin)


	





		
	
		
	