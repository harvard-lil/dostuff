from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import APIRootView

from . import views

# list views that should appear in the HTML version of the API root
root_view = APIRootView.as_view(api_root_dict={
    'event': 'event',
    'events': 'events'
})

urlpatterns = [
    path('new_event', views.EventView.as_view(), name='event'),
    path('events', views.ListEventsView.as_view(), name='events'),
    path('endpoints', root_view),
    path('rooms/<room_name>', views.room),
    path('rooms/<room_name>/<int:em>', views.room),
    path('rooms/<room_name>/<int:em>/<str:color>', views.room),
    path('', views.room, kwargs={"room_name": "display"}),
]
