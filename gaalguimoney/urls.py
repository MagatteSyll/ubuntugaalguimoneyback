
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve 
from user.views import index

urlpatterns = [
    path('gaalguimoney_sylladmin/', admin.site.urls),
    path('api/client/',include('user.urls')),
    path('api/staff/',include('staff.urls')),
    path('',index),
    re_path(r'"media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT})
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
