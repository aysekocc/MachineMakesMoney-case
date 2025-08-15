
from django.urls import path
from .views import SummaryReportView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
urlpatterns = [
    path('summary/', SummaryReportView.as_view(), name='reports-summary'),
    path('summary/swagger-ui/', SpectacularSwaggerView.as_view(), name='swagger-ui'),

]

