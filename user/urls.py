from django.urls import path,include
from .views import*
from rest_framework.routers import SimpleRouter


router=SimpleRouter()
router.register('resetpassword',ResetPassword)
router.register('managecode',RemoveCode)
router.register('envoyerdirect',EnvoyerDirect)
router.register('envoyercode', EnvoiViaCodeDirect)
 




urlpatterns=[
    path('',include(router.urls)),
    path('verificationphoneinscription/',ValidNumber.as_view()),
    path('registration/',RegistrationView.as_view()),
    path('login/',MyTokenObtainPairView.as_view()),
    path('token/refresh/',MyTokenRefreshPairView.as_view()),
    path('verifenvoi/',VerificationCredentialsEnvoi.as_view()),
    path('verificationviacode/',VerificationSomme.as_view()),
    path('getuser/',GetUser.as_view()),
    path('islog/',Authent.as_view()),
    path('message/',UserMessages.as_view()),
    path('verificationpayement/',VerificationPhonePourPayement.as_view()),
    path('payementgaalguishop/',Payementgaalgui.as_view()),
    path('annulationcommandegaalguishop/',AnnulationCommandeGaalgui.as_view()),
    path('recherchemessage/',RechercheMessage.as_view()),
    path('lastmessage/',LastMessages.as_view()),
    path('resetconfirmation/',ResetVerification.as_view()),
    path('recudirect/',RecuDirect.as_view()),
    path('recucode/',RecuCode.as_view()),
    path('messagespecifique/',RecuDonne.as_view()),
    path('getnewuser/',GetNewUser.as_view()),
    path('getransaction/',GetRansactionEnvoiDirect.as_view()),
    path('getransactioncode/',GetRansactionCode.as_view()),
    path('getpub/',GetPub.as_view()),
    path('verificationcodeid/',VerificationIdReset.as_view()),
    path('codereset/',CodeReset.as_view())

    
    
    
    
    
    





]