from django.urls import path

from clients.views import ClientCreateAPIView, DetailClientAPIView


urlpatterns = [
    path('clients/create', ClientCreateAPIView.as_view(), name='client_create'),
    path('clients/detail/<int:pk>', DetailClientAPIView.as_view(), name='detail_view'),
]
