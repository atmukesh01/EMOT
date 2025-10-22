from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_quality_view, name='predict_quality'),
    path('find-params/', views.find_best_parameters_view, name='find_params'),
    path('visualize/', views.visualize_view, name='visualize'),
    path('history/', views.prediction_history_view, name='prediction_history'),
    path('history/download/quality/', views.download_quality_report, name='download_quality_report'),
    path('history/download/image/', views.download_image_report, name='download_image_report'),
    
    # --- ADD THESE TWO NEW URLS ---
    path('history/remove/quality/<int:log_id>/', views.remove_quality_log, name='remove_quality_log'),
    path('history/remove/image/<int:log_id>/', views.remove_image_log, name='remove_image_log'),
]