from datetime import datetime

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from events.api.permissions import UnpublishedEventPermissions
from events.api.serializers import (
    EventCalenderJSSerializer,
    UnpublishedEventSerializer,
    EventRetrieveSerializer,
    EventListSerializer,
    EventRegistrationSerializer)
from events.models import Event, Registration


def _extract_date_range(request):
    try:
        start = timezone.make_aware(
            datetime.strptime(request.query_params['start'], '%Y-%m-%d')
        )
        end = timezone.make_aware(
            datetime.strptime(request.query_params['end'], '%Y-%m-%d')
        )
    except:
        raise ParseError(detail='start or end query parameters invalid')
    return end, start


class EventViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.filter(
        end__gte=timezone.datetime.now(), published=True)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        if self.action == 'retrieve':
            return EventRetrieveSerializer
        return EventCalenderJSSerializer

    @detail_route()
    def registrations(self, request, pk):
        event = Event.objects.get(pk=pk)
        queryset = Registration.objects.filter(
            event=pk, date_cancelled=None)[:event.max_participants]
        serializer = EventRegistrationSerializer(queryset, many=True,
                                                 context={'request': request})

        return Response(serializer.data)

    @list_route(permission_classes=[])
    def calendarjs(self, request):
        end, start = _extract_date_range(request)

        queryset = Event.objects.filter(
            end__gte=start,
            start__lte=end,
            published=True
        )

        serializer = EventCalenderJSSerializer(queryset, many=True,
                                               context={'user': request.user})
        return Response(serializer.data)

    @list_route(permission_classes=(IsAdminUser, UnpublishedEventPermissions,))
    def unpublished(self, request):
        end, start = _extract_date_range(request)

        queryset = Event.objects.filter(
            end__gte=start,
            start__lte=end,
            published=False
        )

        serializer = UnpublishedEventSerializer(queryset, many=True,
                                                context={'user': request.user})
        return Response(serializer.data)
