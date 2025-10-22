from django.contrib import admin
from .models import QualityPredictionLog, ImagePredictionLog

# Customizing the display for Quality Logs
@admin.register(QualityPredictionLog)
class QualityPredictionLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'predicted_quality', 'temperature_c', 'pressure_psi')
    list_filter = ('timestamp',)

# Customizing the display for Image Logs
@admin.register(ImagePredictionLog)
class ImagePredictionLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'identified_plastic', 'confidence_score')
    list_filter = ('identified_plastic', 'timestamp')