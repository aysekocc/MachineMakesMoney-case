
from django.urls import path
from .views import TransactionListView, TransactionUploadView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
urlpatterns = [
    path('', TransactionListView.as_view(), name='transactions-list'),
    path('upload/', TransactionUploadView.as_view(), name='transactions-upload'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
