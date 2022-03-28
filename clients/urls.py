from django.urls import path

from clients import views


urlpatterns = [
    path('clients/create', views.ClientCreateAPIView.as_view(), name='client_create'),
    path('clients/<int:pk>/match', views.MatchCreateAPIView.as_view(), name='match_view')
]
