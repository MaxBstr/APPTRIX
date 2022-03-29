from django.urls import path

from clients import views


urlpatterns = [
    path('list/', views.GetClientListAPIView.as_view(), name='client_list'),
    path('clients/create', views.CreateClientAPIView.as_view(), name='client_create'),
    path('clients/<int:pk>/match', views.CreateMatchAPIView.as_view(), name='create_match')
]
