from django.urls import path

from clients import views


urlpatterns = [
    path(
        'list/',
        views.ClientModelViewSet.as_view({'get': 'list'}),
        name='client_list'
    ),
    path(
        'clients/create',
        views.ClientModelViewSet.as_view({'post': 'create'}),
        name='client_create'
    ),
    path(
        'clients/<int:pk>/match',
        views.MatchCreateAPIView.as_view(),
        name='match_view'
    )
]
