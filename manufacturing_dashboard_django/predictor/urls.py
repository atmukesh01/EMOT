# File: predictor/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # The homepage (http://127.0.0.1:8000/)
    path('', views.home, name='home'),
    
    # The Predict Quality page
    path('predict/', views.predict_quality_view, name='predict_quality'),
    
    # The Find Best Parameters page
    path('find-params/', views.find_best_parameters_view, name='find_params'),
    
    # The Visualize page
    path('visualize/', views.visualize_view, name='visualize'),
]