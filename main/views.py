import json

import requests
from channels import Group
from django.conf import settings
from django.shortcuts import render
from rest_framework import status, serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from rest_framework.views import APIView

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    data = serializers.JSONField()
    event_type = serializers.CharField(read_only=True)
    room_name = serializers.CharField(required=False)

    class Meta:
        model = Event
        fields = ('id', 'event_type', 'data', 'room_name')

class EventView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def post(self, request, format=None):
        data = request.data.dict()

        # find event type
        event_types = ('color', 'message')
        for event_type in event_types:
            if event_type in data:
                break
        else:
            return Response({'error': 'Events must include one of %s' % (event_types,)}, status=status.HTTP_400_BAD_REQUEST)

        room_name = data.pop('room_name', 'display')
        serializer = self.serializer_class(data={'data': data}, context={'request': request})

        if serializer.is_valid():
            serializer.save(created_by=request.user, event_type=event_type, room_name=room_name)
            Group('room-%s' % serializer.instance.room_name).send({
                "text":json.dumps(serializer.data)
            })
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListEventsView(APIView):

    def get(self, request, format=None):
        events = Event.objects.filter(status='submitted')
        if request.GET.get('event_type'):
            events = events.filter(event_type=request.GET['event_type'])

        paginator = LimitOffsetPagination()
        items = paginator.paginate_queryset(events, request)

        serializer = EventSerializer(items, many=True)
        return paginator.get_paginated_response(serializer.data)


def room(request, room_name):
    return render(request, 'show_events.html', {"room": room_name})

# class ResetEventView(APIView):
#     permission_classes = (IsAdminUser,)
#
#     def post(self, request, format=None):
#         Event.objects.filter(status='submitted').update(status='ignored')
#         return Response({'result': 'OK'})


# def display_events(request):
#     requests.post(settings.UPSTREAM_URL+'reset_events', headers={"Authorization": "Token "+})

# class ProcessEventView(APIView):
#     def get(self, request, format=):
#
#     def post(self, request, format=None):
#         Event.objects.filter(status='submitted').update(status='ignored')
#         return Response({'result': 'OK'})