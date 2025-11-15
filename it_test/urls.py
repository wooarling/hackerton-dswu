# it_test/urls.py

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_questions, name='get_questions'),  # /questions/
    path('submit/', views.submit_test, name='submit_test'),  # /questions/submit/

    
    path('events/', include('events.urls')),  # events 앱의 URL들을 포함
]
