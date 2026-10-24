from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include

urlpatterns = [
    path('supperAdmin/', admin.site.urls),
    path("__reload__/",include("django_browser_reload.urls")),
    path("account/", include("accounts.urls")),
    path("",include("FeaturesApp.urls")),
    path('admin/', include('AdminPanal.urls')),
    path('delivery/', include('DeliveryPartner.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
