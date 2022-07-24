from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),

    # Urls Monifinance
    path('', include('base.urls')),
    path('', include('users.urls')),
    path('', include('django.contrib.auth.urls')),
   

]



#STATIC
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)