# File: manufacturing_dashboard_django/urls.py

from django.contrib import admin
from django.urls import path, include # Add 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('predictor.urls')), # Add this line
]