from django.urls import path,include
from .views import*
from rest_framework.routers import SimpleRouter



router=SimpleRouter()
router.register('payement',PayementProfessionnel)




urlpatterns=[
    path('',include(router.urls)),
    path('isstaff/',IsStaff.as_view()),
    path('viacode/',EnvoiViaCodeAgence.as_view()),
    path('getclient/',GetClient.as_view()),
    path('depot/',Deposer.as_view()),
    path('verificationretrait/',VerificationCredentialsRetrait.as_view()),
    path('retrait/',Retirer.as_view()),
    path('verificationcode/',RetraitViaCode.as_view()),
    path('finalretraitcode/',CompletRetrait.as_view()),
    path('annulation/',AnnulationCommandeGaaalgui.as_view()),
    path('notifstaff/',NotifStaff.as_view()),
    path('isbureaucrate/',IsBureaucrate.as_view()),
    path('creationcompteprofessionnel/',ProfessionnelRegistrationView.as_view()),
    path('adress/',Adressage.as_view()),
    path('professionnel/',GetProfessionnels.as_view()),
    path('recudepot/',RecuDepot.as_view()),
    path('recuretrait/',RecuRetrait.as_view()),
    path('commissioncode/',CommissionEnvoiCode.as_view()),
    path('commissionincluse/',CommissionEnvoiCodeInclus.as_view()),
    path('recuviacode/',RecuViaCode.as_view()),
    path('recuretraitcode/',RecuRetraitCode.as_view()),
    path('dernierestransaction/',LastMessageStaf.as_view())

    

 





]