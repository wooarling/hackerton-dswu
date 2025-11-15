from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('it_test.urls')),  
    path('accounts/', include('accounts.urls')), 
    path('events/', include('events.urls')), 
]
