
from django.urls import path
from .views import RegisterView, LoginTokenView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginTokenView.as_view(), name='login'),
]
