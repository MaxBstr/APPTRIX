from django.db.models import QuerySet, F

from django_filters import rest_framework as filters
from django_filters import FilterSet

from clients.utils import get_great_circle_distance
from clients.models import Client


class ClientFilter(FilterSet):
    """
         Custom ClientFilter
    """

    distance = filters.NumberFilter(method='get_nearest_clients')

    def get_nearest_clients(self, queryset: QuerySet, name: str, dist_value: int):
        sender_id = self.request.user.id
        sender_la, sender_lo = Client.objects.get_geo_coordinates(pk=sender_id)

        queryset = queryset.exclude(pk=sender_id).alias(
            lat=F('latitude'), long=F('longitude'),
            distance=get_great_circle_distance(F('lat'), F('long'), sender_la, sender_lo)
        ).exculde(distance__lte=dist_value).order_by('distance')

        return queryset

    class Meta:
        model = Client
        fields = ['gender', 'first_name', 'last_name', 'distance']
