import json

import requests
from channels import Group
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import status, serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from rest_framework.views import APIView

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
        # request.data may be a dict (if JSON post) or an immutable multivalue QueryDict (if key-value post).
        # Coerce either to a regular mutable dictionary:
        data = {k:v for k, v in request.data.items()}

        room_name = data.pop('room_name', 'display')
        serializer = self.serializer_class(data={'data': data}, context={'request': request})

        if serializer.is_valid():
            # let's disable database saving:
            # serializer.save(created_by=request.user, room_name=room_name)
            Group('room-%s' % room_name).send({
                "text":json.dumps(serializer.data)
            })
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
def room(request, room_name):
    return render(request, 'show_events.html', {"room": room_name})
