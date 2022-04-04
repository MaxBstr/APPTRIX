from django.db.models.functions import ACos, Radians, Cos, Sin
from django.db.models import (
    QuerySet, F,
    ExpressionWrapper, FloatField
)

from django_filters import rest_framework as filters
from django_filters import FilterSet
from math import radians

from clients.models import Client


class ClientFilter(FilterSet):
    """
         Custom ClientFilter
    """

    distance = filters.NumberFilter(method='get_nearest_clients')

    def get_nearest_clients(self, queryset: QuerySet, name: str, dist_value: int):
        sender_id = self.request.user.id
        sender_la, sender_lo = map(radians, Client.objects.get_geo_coordinates(pk=sender_id))
        earth_radius = 6_400_000

        queryset = (
            queryset.exclude(pk=sender_id)
            .alias(
                rad_lat=Radians('latitude'),
                rad_long=Radians('longitude'),
                distance=ExpressionWrapper(
                    ACos(
                        Cos('rad_lat') * Cos(sender_la) * Cos(F('rad_long') - sender_lo)
                        + Sin('rad_lat') * Sin(sender_la)
                    ) * earth_radius,
                    output_field=FloatField()
                )
            )
            .exclude(distance__gte=dist_value)
            .order_by('distance')
        )

        return queryset

    class Meta:
        model = Client
        fields = ['gender', 'first_name', 'last_name', 'distance']
