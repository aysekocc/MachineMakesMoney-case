
from django.contrib import admin
from django.urls import path, include
#from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView  # <- bunu ekle
)

def home(request):
    return HttpResponse("Merhaba! Django projen çalışıyor 🚀")


schema_view = get_schema_view(
    openapi.Info(
        title="Banka Ekstre API",
        default_version="v1",
        description="Kullanıcıların banka ekstrelerini yükleyip KPI raporlarını görüntüleyebileceği API",
        contact=openapi.Contact(email="destek@bankaproje.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/transactions/', include('transactions.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
