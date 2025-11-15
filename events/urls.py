from django.urls import path
from . import views

urlpatterns = [
    path('api/events/', views.events_list, name='events_list'),
    path('api/events/create/', views.event_create, name='event_create'),
    path('api/events/<int:pk>/', views.event_detail, name='event_detail'),
    path('api/events/<int:pk>/update/', views.event_update, name='event_update'),
    path('api/events/<int:pk>/delete/', views.event_delete, name='event_delete'),
]
