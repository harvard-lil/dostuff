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

    # path('reset_events', views.ResetEventView.as_view()),
    # path('process_events', views.ProcessEventView.as_view()),

    path('display', TemplateView.as_view(template_name='show_events.html')),

    path('', root_view)
]