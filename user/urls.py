from django.urls import path,include
from .views import*
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import SimpleRouter


router=SimpleRouter()
router.register('modifcred',ModificationCredential)
router.register('resetpassword',ResetPassword)




urlpatterns=[
    path('',include(router.urls)),
    path('verificationphoneinsription/',ValidNumber.as_view()),
    path('registration/',RegistrationView.as_view()),
    path('login/',MyTokenObtainPairView.as_view()),
    path('token/refresh/',TokenRefreshView.as_view()),
    path('blacklist/',BlacklistTokenUpdateView.as_view()),
    path('verifenvoi/',VerificationCredentialsEnvoi.as_view()),
    path('envoi/',EnvoyerDirect.as_view()),
    path('envoicodedirect/',EnvoiViaCodeDirect.as_view()),
    path('verificationviacode/',VerificationSomme.as_view()),
    path('getuser/',GetUser.as_view()),
    path('islog/',Authent.as_view()),
    path('message/',UserMessages.as_view()),
    path('verificationpayement/',VerificationPhonePourPayement.as_view()),
    path('payementgaalguishop/',Payementgaalgui.as_view()),
    path('annulationcommandegaalguishop/',AnnulationCommandeGaalgui.as_view()),
    path('recherchemessage/',RechercheMessage.as_view()),
    path('lastmessage/',LastMessages.as_view()),
    path('historyenvoidirect/',HistoryEnvoiDirect.as_view()),
    path('historyenvoicode/',HistoryEnvoiCode.as_view()),
    path('historyreception/',HistoryReception.as_view()),
    path('historypayement/',HistoryPayement.as_view()),
    path('historydepot/',HistoryDepot.as_view()),
    path('historyretrait/',HistoryRetrait.as_view()),
    path('verifphone/',VerificationPhone.as_view()),
    path('resetconfirmation/',ResetVerification.as_view()),
    path('verifcode/',VerificationCodeReset.as_view()),
    path('recudirect/',RecuDirect.as_view()),
    path('recucode/',RecuCode.as_view()),
    path('messagespecifique/',RecuDonne.as_view()),
    
    
    
    
    





]