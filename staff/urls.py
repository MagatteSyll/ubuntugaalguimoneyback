from django.urls import path,include
from .views import*
from rest_framework.routers import SimpleRouter



router=SimpleRouter()
router.register('payement',PayementProfessionnel)
router.register('lestransactions',LesTransactions)




urlpatterns=[
    path('',include(router.urls)),
    path('isstaff/',IsStaff.as_view()),
    path('getclientdepot/',GetClientDepot.as_view()),
    path('getclientretrait/',GetClientRetrait.as_view()),
    path('verificationcode/',RetraitViaCode.as_view()),
    path('notifstaff/',NotifStaff.as_view()),
    path('creationcompteprofessionnel/',ProfessionnelRegistrationView.as_view()),
    path('adress/',Adressage.as_view()),
    path('professionnel/',GetProfessionnels.as_view()),
    path('recudepot/',RecuDepot.as_view()),
    path('recuretrait/',RecuRetrait.as_view()),
    path('commissionincluse/',CommissionEnvoiCodeInclus.as_view()),
    path('commissionnonincluse/',CommissionEnvoiCodeNonIncluse.as_view()),
    path('recuviacode/',RecuViaCode.as_view()),
    path('recuretraitcode/',RecuRetraitCode.as_view()),
    path('dernierestransaction/',LastMessageStaf.as_view()),
    path('gettransaction/',GetRansaction.as_view()),
    path('getuseractivation/',VerificationPourActivation.as_view()),
    path('getpolza/',GetPolza.as_view()),
    path('activationduclient/',ActivationDuClient.as_view()),
    path('getclientdesactivation/',GetClientDesactivation.as_view()),
    path('getpolzadesactivation/', ConfirmationDesactivation.as_view()),
    path('confirmationdesactivation/',DesactivationDuClient.as_view()),
    path('verificationclientreactivation/',VerifyClientReactivation.as_view()),
    path('getpolzareactivation/',GetClientReactivation.as_view()),
    path('confirmationreactivationclient/',ConfirmationReactivation.as_view()),
    path('verificationnouvelmembre/',VerificationNouvelMembreStaf.as_view()),
    path('getpolzanouvelmembre/',GetClientNouvelMembreStaf.as_view()),
    path('confirmationstaffsimple/',ConfirmationStaffSimple.as_view()),
    path('confirmationstaffbureau/',ConfirmationStaffBureau.as_view()),



    

    

 





]