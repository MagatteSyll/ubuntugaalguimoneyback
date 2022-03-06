import os
import django
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import user.routing
from channels.security.websocket import AllowedHostsOriginValidator


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaalguimoney.settings')
django.setup()

application = ProtocolTypeRouter({
"http": get_asgi_application(),
  "websocket": 
        URLRouter(
            user.routing.websocket_urlpatterns
        )
    
})