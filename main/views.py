import json

from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import status, serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    data = serializers.JSONField()
    room_name = serializers.CharField(required=False)

    class Meta:
        model = Event
        fields = ('id', 'data', 'room_name')


class EventView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def post(self, request, format=None):
        # request.data may be a dict (if JSON post) or an
        # immutable multivalue QueryDict (if key-value post).
        # Coerce either to a regular mutable dictionary:
        data = {k: v for k, v in request.data.items()}

        room_name = data.pop('room_name', 'display')
        serializer = self.serializer_class(
            data={'data': data},
            context={'request': request}
        )

        # this wrapper is required to handle a runtime error,
        # "Event loop is closed":
        # https://github.com/django/channels_redis/issues/332
        async def closing_send(channel_layer, channel, message):
            await channel_layer.group_send(channel, message)
            await channel_layer.close_pools()

        if serializer.is_valid():
            # let's disable database saving:
            # serializer.save(created_by=request.user, room_name=room_name)
            channel_layer = get_channel_layer()
            async_to_sync(closing_send)(
                channel_layer,
                f'room-{room_name}',
                {
                    "text": json.dumps(serializer.data),
                    "type": "websocket_receive"
                }
            )
            return Response("OK", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListEventsView(APIView):

    def get(self, request, format=None):
        events = Event.objects.all()

        paginator = LimitOffsetPagination()
        items = paginator.paginate_queryset(events, request)

        serializer = EventSerializer(items, many=True)
        return paginator.get_paginated_response(serializer.data)


@xframe_options_exempt
def room(request, room_name, em=8, color='white'):
    return render(
        request, 'show_events.html', {
            "room": room_name,
            "em": em,
            "color": color
        }
    )
