from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_quality_view, name='predict_quality'),
    path('find-params/', views.find_best_parameters_view, name='find_params'),
    path('requirements/', views.requirements_view, name='requirements'),
    path('processes/', views.processes_view, name='processes'),
    path('visualize/', views.visualize_view, name='visualize'),
]